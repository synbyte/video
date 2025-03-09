##########################################################
# Updated 2-16-25 by Yuriy
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

logger = logging.getLogger("### IFA AI ###")
logger.setLevel(logging.INFO)


async def entrypoint(job: JobContext):
    room = job.room
    waiting_for_second_participant = False
    initial_wait_complete = False
    extended_wait_complete = False
    music_task = None
    
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

    async def play_classical_music():
        try:
            # Use the existing source that we use for TTS
            with wave.open('music.wav', 'rb') as wave_file:
                # Verify file properties
                if wave_file.getframerate() != 24000 or wave_file.getnchannels() != 1:
                    logger.error("Audio file must be 24kHz mono")
                    return
                
                while True:
                    # Check if task is cancelled at the start of each iteration
                    if asyncio.current_task().cancelled():
                        logger.info("Music playback cancelled - breaking loop")
                        return

                    chunk_size = 240  # 10ms at 24kHz
                    frames = wave_file.readframes(chunk_size)
                    if not frames:
                        wave_file.rewind()  # Loop the music
                        continue
                    
                    source_sr = source.sample_rate
                    source_ch = source.num_channels
                    audio_frame = rtc.AudioFrame(
                        data=frames,
                        samples_per_channel=chunk_size,
                        sample_rate=source_sr,
                        num_channels=source_ch,
                    )
                    await source.capture_frame(audio_frame)
                    await asyncio.sleep(0.01)
                    
        except asyncio.CancelledError:
            logger.info("Music playback cancelled via CancelledError")
            return
        except Exception as e:
            logger.error(f"Error playing classical music: {e}")
            return

    async def single_participant_flow(participant: rtc.Participant):
        nonlocal waiting_for_second_participant, initial_wait_complete, extended_wait_complete, music_task
        logger.info(f"Starting single participant flow for {participant.identity}")
        
        # Initial greeting
        async for output in tts.synthesize(f"Hi {participant.identity}, my name is Eefa, your figbox A.I. . Glad to have you on board!"):
            await source.capture_frame(output.frame)
        
        waiting_for_second_participant = True
        await asyncio.sleep(5)  # Wait 2 minutes 120
        
        # Check for second participant
        if len(room.remote_participants) > 1:
            return
        
        if not initial_wait_complete:
            initial_wait_complete = True
            async for output in tts.synthesize(f"Hey {participant.identity}, you are still the only one in the room. Hmm! Let me quickly check if Red got my email reminder about this session. I'll be right back!"):
                await source.capture_frame(output.frame)
            
            await asyncio.sleep(5)  # Wait 5 minutes 300
            
            # Check for second participant again
            if len(room.remote_participants) > 1:
                return
            
            if not extended_wait_complete:
                extended_wait_complete = True
                # First message
                async for output in tts.synthesize("Looks like Red still isnt here. Lets wait a couple of minutes, maybe an emergency came up. In the meantime, I'll play some classical tunes to keep you entertained."):
                    await source.capture_frame(output.frame)
                
                # Play classical music
                await asyncio.sleep(1)  # Small pause before music
                music_task = asyncio.create_task(play_classical_music())
                
                try:
                    await music_task
                except asyncio.CancelledError:
                    logger.info("Music playback cancelled due to second participant")
                    return  # Exit immediately when music is cancelled
                
                # Only continue with closing message if still single participant
                if len(room.remote_participants) == 1:
                    # Second message
                    async for output in tts.synthesize("Hmm, it looks like Red wont be attending the session. I'll send an email to let them know you were present. To create a better experience, I'll find another user who matches your needs and has a high attendance score. Sorry for the inconvinience, and I look forward to seeing you in future sessions!"):
                        await source.capture_frame(output.frame)

    async def handle_participants():
        nonlocal music_task
        logger.info(f"Checking participants. Current count: {len(room.remote_participants)}")
        
        if len(room.remote_participants) > 1:
            # Stop music if it's playing
            if music_task and not music_task.done():
                logger.info("Cancelling music task due to second participant")
                music_task.cancel()
                try:
                    await music_task
                except asyncio.CancelledError:
                    pass
                music_task = None
                
            # Both participants are here, proceed with original flow
            logger.info("Starting multi-participant flow")
            for p in room.remote_participants.values():
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
        elif len(room.remote_participants) == 1:
            participants = list(room.remote_participants.values())
            participant = participants[0]
            logger.info(f"Found single participant: {participant.identity}")
            await single_participant_flow(participant)

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

    logger.info("Starting Ifa AI...")

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