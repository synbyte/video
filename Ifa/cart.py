import asyncio
import logging
import wave
from dotenv import load_dotenv
from livekit import rtc
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli
from livekit.plugins import cartesia

load_dotenv()

logger = logging.getLogger("cartesia-tts-demo")
logger.setLevel(logging.INFO)


async def entrypoint(job: JobContext):
    room = job.room
    
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
    async def on_participant_connected(participant:rtc.Participant):
        if len(room.remote_participants) == 2:
            for p in room.remote_participants:
                async for output in tts.synthesize(f"Welcome in {p}!"):
                    await source.capture_frame(output.frame)
        async for output in tts.synthesize("Welcome to your Figbox session! My name is Ifa. Please introduce yourself and start your session. In the meantime, I will take a back seat and learn from both of you."):
            await source.capture_frame(output.frame)
        await asyncio.sleep(900) # Warning after 15 minutes
        async for output in tts.synthesize("Hey, sorry to interrupt, but you have 5 minutes left in this session. This really sounds like an interesting conversation. You can always book another Figbox session. Please note, once the 5 minutes is up, I will stop the session."):
            await source.capture_frame(output.frame)

    @room.on("track_subscribed")
    def track_subscribed_handler(track: rtc.Track, publication: rtc.TrackPublication, participant: rtc.Participant):
        asyncio.create_task(on_track_subscribed(track, publication, participant))
    
    @room.on("participant_connected")
    def participant_connected_handler(participant:rtc.Participant):
        asyncio.create_task(on_participant_connected(participant))

    logger.info("starting tts example  agent")

    tts = cartesia.TTS(
        speed="normal",
        emotion=["surprise:highest"]
    )

    source = rtc.AudioSource(tts.sample_rate, tts.num_channels)
    track = rtc.LocalAudioTrack.create_audio_track("agent-mic", source)
    options = rtc.TrackPublishOptions()
    options.source = rtc.TrackSource.SOURCE_MICROPHONE

    await job.connect()
    publication = await job.room.local_participant.publish_track(track, options)
    await publication.wait_for_subscription()

    #logger.info('Saying "Hello!"')
    #async for output in tts.synthesize("Hello I hope you are having a great day."):
    #    await source.capture_frame(output.frame)

    #await asyncio.sleep(4)
    #logger.info('Saying "Goodbye."')
    #async for output in tts.synthesize("Goodbye I hope to see you again soon."):
    #    await source.capture_frame(output.frame)


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))