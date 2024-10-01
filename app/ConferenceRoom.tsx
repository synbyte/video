
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

  const participantCount = allParticipants.filter(p => !p.isAgent).length;
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
  

  useEffect(() => {
    if (participantCount > maxParticipants && !isLocalInList) {
      r.push("/full");
    }
  });

  // Introduce the voice assistant and start recording
  useEffect(() => {
    if (participantCount > 1) { // 2 because we need to include the agent
     
      if(!hasRun.current){
      addVoiceAssistant(allParticipants); // Pass all participants to the function
      startRecording(); // Start recording audio

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
        if (participantCount > 1){ // 2 because we need to include the agent
        setTimeLeft(timeLeft - 1);
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
  }, [timeLeft]);

  return (
    <>
      <GridLayout tracks={participantTracks} style={{ height: "calc(100vh)" }}>
        <>
        <ParticipantTile  data-lk-theme="defaul" className='border-2 border-slate-600'>       
        <ParticipantName style={{fontSize: "1.2rem", fontWeight: "bold"}} className='text-white bg-slate-500 px-3 ring-4 ring-slate-800  rounded-lg font-bold absolute top-5 left-1/4' />
        </ParticipantTile>
        
        </>
      </GridLayout>
      <GridLayout className='border-2 rounded-full border-slate-600 left-1/2 -translate-x-1/2' style={{position:'absolute', top:0, zIndex:100, height:150, width:150}} tracks={agentTrack}>
      <>
      <ParticipantTile/>
      </>
      </GridLayout>
 
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
      style={{ width: '75vw', height: '300px' }}
    />
  );
}