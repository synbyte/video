
// Updated by EL, tested on my end..working 
// 9/26/24
// Take parts you need, forgo other parts you don't need 


import '@livekit/components-styles';
import { useEffect, useState, useRef } from "react";
import { useVoiceAssistant,BarVisualizer,useRoomContext, useRemoteParticipants, useParticipants, useTracks, GridLayout, ParticipantTile, ParticipantName, ConnectionStateToast, RoomAudioRenderer } from "@livekit/components-react";
import { Track } from "livekit-client";
import ControlBar from "./ControlBar";
import { useRouter } from "next/navigation";
import { addVoiceAssistant, startRecording, speakMessage } from "./VoiceAssistantUtils"; // Import your functions

export default function MyVideoConference(props: any) {
  const remoteParticipants = useRemoteParticipants();
  const allParticipants = useParticipants(); // This returns an object or map
  const maxParticipants = props.participantLimit;
  const room = useRoomContext();
  const participantCountRef = useRef<Set<string>>(new Set());
  const [localID, setLocalID] = useState<string>("null");
  const r = useRouter();
  const hasRun = useRef(false);
  
  const sessionDuration = props.sessionDuration || 20; // default 20-minute session
  const [timeLeft, setTimeLeft] = useState(sessionDuration); 

  // New audio element for the cough sound
  const coughSound = new Audio('https://cdn.freesound.org/previews/436/436107_729251-lq.mp3'); // Adjust path accordingly

  // Add local participant to the list
  useEffect(() => {
    const all = allParticipants.filter(p => !p.isAgent);
    
    if (all <= maxParticipants) {
      const localParticipant = allParticipants[0];
      setLocalID(localParticipant.identity);
      if (!participantCountRef.current.has(localParticipant.identity)) {
        participantCountRef.current.add(localParticipant.identity);
      }
    }
  }, [allParticipants]);

  //remove participant from list when they disconnect
  useEffect(() => {
    room.on("participantDisconnected", (participant) => {
      participantCountRef.current.delete(participant.identity);
    });
  }, [remoteParticipants]);

  const participantCount = allParticipants.filter(p => !p.isAgent).length; // All participants not including agent
 
  const isLocalInList = localID
    ? participantCountRef.current.has(localID)
    : false;
  const tracks = useTracks(
    [
      { source: Track.Source.Camera, withPlaceholder: true },
      { source: Track.Source.ScreenShare, withPlaceholder: false },
    ],
    { onlySubscribed: false }
  );
  let participantTracks = tracks.filter(track => !track.participant.isAgent)
  let agentTrack = tracks.filter(track => track.participant.isAgent)
  
  // Logic to send to another page when room is full
  useEffect(() => {
    if (participantCount > maxParticipants && !isLocalInList) {
      r.push("/full");
    }
  });

  // Introduce the voice assistant and start recording
  useEffect(() => {
    if (participantCount > 1) { 
     
      if(!hasRun.current){
      addVoiceAssistant(allParticipants); // Pass all participants to the function

      // Play the cough sound, then speak the message after it finishes
      coughSound.play().then(() => {
        setTimeout(() => {
        speakMessage(
          "Hi Guys, welcome to your Figbox session. My name is Ifa. Please introduce yourself and start your session. In the meantime, I will take a back seat and learn from both of you."
        );
      },1000);
      });
      hasRun.current = true;
    }
    }
  }, [participantCount]); // Run this effect when the participants change

  // Timer logic for 5-minute reminder
  useEffect(() => {
    if (timeLeft > 0) {
      const timer = setTimeout(() => {
        if (participantCount > 1){ 
        setTimeLeft(timeLeft - 1);
        console.log("TIME LEFT:", timeLeft)
        }
      }, 1000);

      if (timeLeft === 5 * 60) {
        // Play cough sound before the reminder message
        coughSound.play().then(() => {
          setTimeout(() => {
            speakMessage(
              "Hey, sorry to interrupt, but you have 5 minutes left in this session. This really sounds like an interesting conversation. You can always book another Figbox session. Please note, once the 5 minutes is up, I will stop the session."
            );
          }, 1000);
        });
      }

      return () => clearTimeout(timer);
    }
  });

  return (
    <>
      <GridLayout tracks={participantTracks} style={{ height: "calc(100vh)" }}>
        <>
          <ParticipantTile className='border-2 border-slate-600'>
            <ParticipantName style={{ }} className='text-white bg-black bg-opacity-50 px-3  rounded-lg font-bold absolute top-5 left-1/4' />
          </ParticipantTile>
        </>
      </GridLayout>
  
      {agentTrack.length > 0 && (
        <GridLayout className='rounded-full left-1/2 -translate-x-1/2' style={{ position: 'absolute', top: 0, zIndex: 100, height: 150, width: 150 }} tracks={agentTrack}>
          <>
            <ParticipantTile className='flex mx-auto align-middle justify-center border-2 border-white'><div className='shadow-[0_0_15px_0px_-5px] shadow-violet-600 rounded-full m-4 p-4 bg-gradient-radial from-white to-slate-400'><svg width="42" height="42" viewBox="0 0 56 57" fill="#201C5A" xmlns="http://www.w3.org/2000/svg"><path clipRule="evenodd" d="M9.874 7.078 2 11.77l.086 15.645c.132 15.413.132 15.644 1.125 17.115 1.383 2.069 15.84 10.995 16.92 10.446 2.771-1.428 15.105-9.202 14.973-9.433-.086-.14-3.157-2.069-6.795-4.326-3.633-2.209-7.1-4.51-7.616-5.016-2.21-2.068-2.25-2.392-2.25-18.677 0-8.329-.132-15.181-.304-15.181-.213-.006-3.891 2.111-8.265 4.735Z"></path><path clipRule="evenodd" d="M28.434 6.65c-4.24 2.574-7.616 4.783-7.484 4.966.086.183 3.157 2.16 6.795 4.418 3.633 2.208 7.1 4.509 7.662 5.015 2.118 1.977 2.21 2.855 2.21 18.91 0 8.236.131 14.954.344 14.906.172 0 3.81-2.117 8.092-4.693l7.789-4.692.086-15.181c.132-19.184.993-17.115-9.39-23.558C40.383 4.117 36.79 2 36.532 2c-.223.005-3.902 2.123-8.098 4.65Z"></path></svg></div></ParticipantTile>
          </>
        </GridLayout>
      )}
  
      <ConnectionStateToast />
      <RoomAudioRenderer />
      <ControlBar />
    </>
  );
}
function SimpleVoiceAssistant() {
  const { state, audioTrack } = useVoiceAssistant();
  return (
    <BarVisualizer
      state={state}
      barCount={7}
      trackRef={audioTrack}
      style={{ width: '40px', height: '40px' }}
    />
  );
}