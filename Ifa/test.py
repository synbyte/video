import asyncio
import logging

from dotenv import load_dotenv
from livekit import rtc
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli
from livekit.plugins import cartesia

load_dotenv()

logger = logging.getLogger("cartesia-tts-demo")
logger.setLevel(logging.INFO)


async def entrypoint(job: JobContext):
    logger.info("starting tts example agent")

    tts = cartesia.TTS(
        speed="fastest",
        emotion=["surprise:highest"],
        voice="820a3788-2b37-4d21-847a-b65d8a68c99a"
    )

    source = rtc.AudioSource(tts.sample_rate, tts.num_channels)
    track = rtc.LocalAudioTrack.create_audio_track("agent-mic", source)
    options = rtc.TrackPublishOptions()
    options.source = rtc.TrackSource.SOURCE_MICROPHONE

    await job.connect(auto_subscribe=AutoSubscribe.SUBSCRIBE_NONE)
    publication = await job.room.local_participant.publish_track(track, options)
    await publication.wait_for_subscription()

    logger.info('Saying "Hello!"')
    async for output in tts.synthesize("Welcome to your Figbox session! My name is eefa A.I.. Please introduce yourself and start your session. In the meantime, I will keep time and start upload both of your thoughts to the cloud in order to learn your cognitive habits. Let me know if you need anything!"):
        await source.capture_frame(output.frame)

    await asyncio.sleep(4)
    logger.info('Saying "Goodbye."')
    async for output in tts.synthesize("Goodbye I hope to see you again soon."):
        await source.capture_frame(output.frame)


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))