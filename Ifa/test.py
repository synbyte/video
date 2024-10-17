##########################################################
# Updated 10-16-24 by Yuriy
# Uses Cartesia or OpenAI for TTS, comment out the one not using
##########################################################

import asyncio
import logging
import wave
from dotenv import load_dotenv
from livekit import rtc
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli
from livekit.plugins import openai, cartesia
from greetings import generate_greeting_variation, random_joke, generate_closing_variation

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
        
        
        # UNCOMMENT FOR HARDCODED GREETING 
        #async for output in tts.synthesize("My name is Eefa, your figbox A.I! Welcome to your figbox session. I have a good feeling about this match! Please introduce yourselves. In the meantime, I'll start building a cognitive profile for both of you to learn about your needs. This will help me better match you with other problem solvers in future sessions  who may provide additional insights and solutions. I'm also here to make the conversation fun, relaxed, and insightful. Let me know if you need anything!"):
        async for output in tts.synthesize(generate_greeting_variation()):
            await source.capture_frame(output.frame)
        
        await asyncio.sleep(7) # Joke after 7 seconds
        async for output in tts.synthesize(random_joke()):
            await source.capture_frame(output.frame)
        
        # UNCOMMENT FOR SUGGESTION
        """ await asyncio.sleep(420) # Interrupt after 7 minutes
        async for output in tts.synthesize("Hmmm..Hey guys,Sorry to interrupt. I noticed you're all talking about how to build a successful startup. According to an analysis by Bill Gross, who has invested in a number of startups, he found that the success of a startup is determined by 6 key factors: Luck, Timing, A dynamic team that can execute, A very good idea, a scalable business model, Funding And more importantly, having a technical founder who can also do other things, like sell the product and motivate his team—kind of like you, Emmanuel."):
            await source.capture_frame(output.frame) """
        
        await asyncio.sleep(900) # Warning after 15 minutes 
        async for output in tts.synthesize(generate_closing_variation()):
            await source.capture_frame(output.frame)

    @room.on("track_subscribed")
    def track_subscribed_handler(track: rtc.Track, publication: rtc.TrackPublication, participant: rtc.Participant):
        asyncio.create_task(on_track_subscribed(track, publication, participant))
    
    @room.on("participant_connected")
    def participant_connected_handler(participant:rtc.Participant):
        asyncio.create_task(on_participant_connected(participant))

    logger.info("starting tts example  agent")

    tts = openai.TTS(
        model="tts-1",
        voice="alloy",
        api_key="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"
    )

    """ tts = cartesia.TTS(
        speed="slow",
        emotion=["positivity"],
        #voice="5619d38c-cf51-4d8e-9575-48f61a280413"
    ) """

    source = rtc.AudioSource(tts.sample_rate, tts.num_channels)
    track = rtc.LocalAudioTrack.create_audio_track("agent-mic", source)
    options = rtc.TrackPublishOptions()
    options.source = rtc.TrackSource.SOURCE_MICROPHONE

    await job.connect()
    publication = await job.room.local_participant.publish_track(track, options)
    await publication.wait_for_subscription()


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))