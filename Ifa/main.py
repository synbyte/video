import logging
import wave
import asyncio
from dotenv import load_dotenv
from livekit import rtc
from livekit.agents import JobContext, WorkerOptions, WorkerType, cli

load_dotenv()

logger = logging.getLogger("my-worker")
logger.setLevel(logging.INFO)

async def entrypoint(ctx: JobContext):
    room = ctx.room

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

    @room.on("track_subscribed")
    def track_subscribed_handler(track: rtc.Track, publication: rtc.TrackPublication, participant: rtc.Participant):
        asyncio.create_task(on_track_subscribed(track, publication, participant))

    await ctx.connect()

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, worker_type=WorkerType.ROOM))