import asyncio
import logging
import wave
from dotenv import load_dotenv
from livekit import rtc
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli
from livekit.plugins import openai, cartesia

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
        if len(room.remote_participants) > 1:
            for p in room.remote_participants:
                await asyncio.sleep(1)
                async for output in tts.synthesize(f"Hello {p}!"):
                    await source.capture_frame(output.frame)
        async for output in tts.synthesize("My name is Eefa, your figbox A.I! Welcome to your figbox session. I have a good feeling about this match! Please introduce yourselves. In the meantime, I'll start building a cognitive profile for both of you to learn about your needs. This will help me better match you with other problem solvers in future sessions  who may provide additional insights and solutions. I'm also here to make the conversation fun, relaxed, and insightful. Let me know if you need anything!"):
            await source.capture_frame(output.frame)
        await asyncio.sleep(7) # Warning after 15 minutes
        async for output in tts.synthesize("Wow, this silence is so loud, I can almost hear the Wi-Fi thinking."):
            await source.capture_frame(output.frame)
        await asyncio.sleep(420) # Interrupt after 7 minutes
        async for output in tts.synthesize("Hmmm..Hey guys,Sorry to interrupt. I noticed you're all talking about how to build a successful startup. According to an analysis by Bill Gross, who has invested in a number of startups, he found that the success of a startup is determined by 6 key factors: Luck, Timing, A dynamic team that can execute, A very good idea, a scalable business model, Funding And more importantly, having a technical founder who can also do other things, like sell the product and motivate his team—kind of like you, Emmanuel."):
            await source.capture_frame(output.frame)
        await asyncio.sleep(420) # Warning after 15 minutes
        async for output in tts.synthesize("Hey guys, I just want to let you know that I've been tracking the time, and you have 5 minutes left before the session ends. You might want to add each other to your list of collaborators on figbox and continue the conversation afterwards."):
            await source.capture_frame(output.frame)

    @room.on("track_subscribed")
    def track_subscribed_handler(track: rtc.Track, publication: rtc.TrackPublication, participant: rtc.Participant):
        asyncio.create_task(on_track_subscribed(track, publication, participant))
    
    @room.on("participant_connected")
    def participant_connected_handler(participant:rtc.Participant):
        asyncio.create_task(on_participant_connected(participant))

    logger.info("starting tts example  agent")

    """ tts = openai.TTS(
        model="tts-1",
        voice="alloy",
        api_key="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"
    ) """

    tts = cartesia.TTS(
        speed="slow",
        emotion=["positivity"],
        #voice="5619d38c-cf51-4d8e-9575-48f61a280413"
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