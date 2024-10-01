import logging
import wave
import asyncio
from dotenv import load_dotenv
from livekit import rtc
from livekit.agents import JobContext, WorkerOptions, WorkerPermissions, WorkerType, cli
from gtts import gTTS
import io
import soundfile as sf
import numpy as np
load_dotenv()

logger = logging.getLogger("my-worker")
logger.setLevel(logging.INFO)
SAMPLE_RATE = 48000
NUM_CHANNELS = 1
SAMPLES_PER_CHANNEL = 960
AMPLITUDE = 32767
async def entrypoint(ctx: JobContext):
    room = ctx.room
    
    logger.info("----------CONNECTED TO ROOM-----")
    async def on_track_subscribed(track: rtc.Track, publication: rtc.TrackPublication, participant: rtc.Participant):
        if track.kind == rtc.TrackKind.KIND_AUDIO:
            logger.info(f'Audio track subscribed: {track.sid}')
            
            # Open a wave file for writing
            with wave.open(f'output_{participant.identity}.wav', 'wb') as wave_file:
                wave_file.setnchannels(1)  # Mono audio
                wave_file.setsampwidth(2)  # 16-bit audio
                wave_file.setframerate(48000)  # Assuming 48kHz sample rate
                
                async for audio_frame in rtc.AudioStream(track):
                    # Write the raw audio data to the wave file
                    wave_file.writeframes(audio_frame.frame.data)

            logger.info(f'Finished writing audio for track: {track.sid}')

    async def on_participant_connected(participant: rtc.Participant):
       
        logger.info(f"Participant connected: {participant.identity}")
        
            # Both participants are in the room, say hello using TTS
        greeting = "Hello, welcome to your Figbox session. I'm Ifa, your AI assistant."
        tts = gTTS(text=greeting, lang='en')
        logger.info("set GTTS")    
            # Save the speech to a BytesIO object
        mp3_fp = io.BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        logger.info("Generating speech...")
            
            # Convert MP3 to WAV
        data, samplerate = sf.read(mp3_fp)
        wav_fp = io.BytesIO()
        sf.write(wav_fp, data, samplerate, format='WAV')
        wav_fp.seek(0)
        logger.info("Converted speech to WAV.")

            # Create audio source and track
        source = rtc.AudioSource(SAMPLE_RATE, NUM_CHANNELS)
        track = rtc.LocalAudioTrack.create_audio_track("greeting-track", source)
            
            # Publish the track
        options = rtc.TrackPublishOptions(source=rtc.TrackSource.SOURCE_MICROPHONE)
        publication = await ctx.agent.publish_track(track, options)
        logger.info("publishing tracks")    
            # Send the audio data
        audio_frame = rtc.AudioFrame.create(SAMPLE_RATE, NUM_CHANNELS, SAMPLES_PER_CHANNEL)
        audio_data = np.frombuffer(audio_frame.data, dtype=np.int16)
        logger.inf("SENDING AUDIO")    
        while True:
            chunk = wav_fp.read(SAMPLES_PER_CHANNEL * 2)  # 2 bytes per sample for 16-bit audio
            if not chunk:
                break
            np.copyto(audio_data, np.frombuffer(chunk, dtype=np.int16))
            await source.capture_frame(audio_frame)
            
        await publication.stop()

    
    @room.on("track_subscribed")
    def track_subscribed_handler(track: rtc.Track, publication: rtc.TrackPublication, participant: rtc.Participant):
        asyncio.create_task(on_track_subscribed(track, publication, participant))

    #@room.on("participant_connected")
    #def participant_connected_handler(participant: rtc.Participant):
        #asyncio.create_task(on_participant_connected(participant))

    await ctx.connect()
    await room.local_participant.set_name("Ifa")
if __name__ == "__main__":
    opts = WorkerOptions(
        entrypoint_fnc=entrypoint,
        permissions=WorkerPermissions(hidden=False),
        worker_type=WorkerType.ROOM,
    )
    cli.run_app(opts)