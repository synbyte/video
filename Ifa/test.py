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
from livekit.plugins import cartesia
from generations import generate_greeting_variation, random_joke, generate_closing_variation

load_dotenv()

logger = logging.getLogger("cartesia-tts-demo")
logger.setLevel(logging.INFO)


async def entrypoint(job: JobContext):
    room = job.room
    waiting_for_second_participant = False
    initial_wait_complete = False
    extended_wait_complete = False
    
    async def on_track_subscribed(track: rtc.Track, publication: rtc.TrackPublication, participant: rtc.Participant):
        if track.kind == rtc.TrackKind.KIND_AUDIO:
            logger.info(f'Audio track subscribed: {track.sid}')
            
            with wave.open(f'output_{participant.identity}.wav', 'wb') as wave_file:
                wave_file.setnchannels(1)
                wave_file.setsampwidth(2)
                wave_file.setframerate(48000)
                
                async for audio_frame in rtc.AudioStream(track):
                    wave_file.writeframes(audio_frame.frame.data)

            logger.info(f'Finished writing audio for track: {track.sid}')

    async def single_participant_flow(participant_name: str):
        nonlocal waiting_for_second_participant, initial_wait_complete, extended_wait_complete
        
        # Initial greeting
        async for output in tts.synthesize(f"Hi {participant_name}, my name is ida, your figbox ai. glad to have you on board!"):
            await source.capture_frame(output.frame)
        
        waiting_for_second_participant = True
        await asyncio.sleep(120)  # Wait 2 minutes
        
        if len(room.remote_participants) == 1 and not initial_wait_complete:
            initial_wait_complete = True
            async for output in tts.synthesize(f"Hey {participant_name}, you are still the only one in the room. Hmm! Let me quickly check if Red got my email reminder about this session. Ill be right back!"):
                await source.capture_frame(output.frame)
            
            await asyncio.sleep(300)  # Wait 5 minutes
            
            if len(room.remote_participants) == 1 and not extended_wait_complete:
                extended_wait_complete = True
                async for output in tts.synthesize("Looks like Red still isnt here. Lets wait a couple of minutes, maybe an emergency came up. In the meantime, I'll play some classical tunes to keep you entertained."):
                    await source.capture_frame(output.frame)
                
                async for output in tts.synthesize("Hmm, it looks like Red wont be attending the session. Ill send an email to let them know you were present. To create a better experience, Ill find another user who matches your needs and has a high attendance score. Sorry for the inconvinience, and I look forward to seeing you in future sessions!"):
                    await source.capture_frame(output.frame)

    async def handle_participants():
        logger.info(f"Checking participants. Current count: {len(room.remote_participants)}")
        
        if len(room.remote_participants) == 1:
            # Start single participant flow
            participant = next(iter(room.remote_participants))
            await single_participant_flow(participant.identity)
        elif len(room.remote_participants) > 1 and not extended_wait_complete:
            # Both participants are here, proceed with original flow
            logger.info("Starting multi-participant flow")
            for p in room.remote_participants:
                await asyncio.sleep(1)
                async for output in tts.synthesize(f"Hello {p.identity}!"):
                    await source.capture_frame(output.frame)
            
            async for output in tts.synthesize(generate_greeting_variation()):
                await source.capture_frame(output.frame)
            
            await asyncio.sleep(7)
            async for output in tts.synthesize(random_joke()):
                await source.capture_frame(output.frame)
            
            await asyncio.sleep(900)
            async for output in tts.synthesize(generate_closing_variation()):
                await source.capture_frame(output.frame)

    async def on_participant_connected(participant: rtc.Participant):
        logger.info(f"Participant connected: {participant.identity}")
        await asyncio.sleep(2)  # Small delay to ensure room state is updated
        await handle_participants()

    @room.on("track_subscribed")
    def track_subscribed_handler(track: rtc.Track, publication: rtc.TrackPublication, participant: rtc.Participant):
        asyncio.create_task(on_track_subscribed(track, publication, participant))
    
    @room.on("participant_connected")
    def participant_connected_handler(participant: rtc.Participant):
        asyncio.create_task(on_participant_connected(participant))

    logger.info("starting tts example agent")

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
    
    # Check for existing participants after connecting
    await handle_participants()

    # Keep the agent running
    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))