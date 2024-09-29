import logging
import wave
import asyncio
from dotenv import load_dotenv
from livekit import rtc
from livekit.agents import JobContext, WorkerOptions, WorkerType, cli
import io
import pyttsx3
import numpy as np
import tempfile
import os
load_dotenv()

logger = logging.getLogger("my-worker")
logger.setLevel(logging.INFO)

SAMPLE_RATE = 48000
NUM_CHANNELS = 1 # mono audio
AMPLITUDE = 2 ** 8 - 1
SAMPLES_PER_CHANNEL = 480 # 10ms at 48kHz

# Initialize pyttsx3
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed of speech

# Function to generate speech from text
def generate_speech(text):
    with io.BytesIO() as buf:
        engine.save_to_file(text, buf)
        engine.runAndWait()
        buf.seek(0)
        with wave.open(buf, 'rb') as wf:
            frames = wf.readframes(wf.getnframes())
    return np.frombuffer(frames, dtype=np.int16)
  
hello_audio = generate_speech("hello")

# Function to handle track subscription and record audio
async def on_track_subscribed(track: rtc.Track, publication: rtc.TrackPublication, participant: rtc.Participant):
        if track.kind == rtc.TrackKind.KIND_AUDIO:
            logger.info(f'Audio track subscribed: {track.sid}')
            
            # Open a wave file for writing
            with wave.open(f'output_{participant.name}.wav', 'wb') as wave_file:
                wave_file.setnchannels(1)  # Mono audio
                wave_file.setsampwidth(2)  # 16-bit audio
                wave_file.setframerate(48000)  # Assuming 48kHz sample rate
                
                async for audio_frame in rtc.AudioStream(track):
                    # Write the raw audio data to the wave file
                    wave_file.writeframes(audio_frame.frame.data)

            logger.info(f'Finished writing audio for track: {track.sid}')

# Function to play hello audio
async def play_hello():
        for i in range(0, len(hello_audio), SAMPLES_PER_CHANNEL):
            chunk = hello_audio[i:i+SAMPLES_PER_CHANNEL]
            if len(chunk) < SAMPLES_PER_CHANNEL:
                chunk = np.pad(chunk, (0, SAMPLES_PER_CHANNEL - len(chunk)), 'constant')
            audio_frame = rtc.AudioFrame.create(SAMPLE_RATE, NUM_CHANNELS, SAMPLES_PER_CHANNEL)
            np.copyto(np.frombuffer(audio_frame.data, dtype=np.int16), chunk)
            await source.capture_frame(audio_frame)
            await asyncio.sleep(0.01)  # 10ms delay between frames

async def entrypoint(ctx: JobContext):
    room = ctx.room
    await ctx.connect()
    source = rtc.AudioSource(SAMPLE_RATE, NUM_CHANNELS)
    track = rtc.LocalAudioTrack.create_audio_track("example-track", source)
    # since the agent is a participant, our audio I/O is its "microphone"
    options = rtc.TrackPublishOptions(source=rtc.TrackSource.SOURCE_MICROPHONE)
    # ctx.agent is an alias for ctx.room.local_participant
    publication = await ctx.agent.publish_track(track, options)
    
    

    @room.on("track_subscribed")
    def track_subscribed_handler(track: rtc.Track, publication: rtc.TrackPublication, participant: rtc.Participant):
        asyncio.create_task(on_track_subscribed(track, publication, participant))

    @room.on("participant_connected")
    def participant_connected_handler(participant: rtc.Participant):
        asyncio.create_task(play_hello())

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, worker_type=WorkerType.ROOM))