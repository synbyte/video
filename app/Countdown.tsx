import { CountdownCircleTimer } from "react-countdown-circle-timer";
import { useRemoteParticipants } from "@livekit/components-react";
import { useState, useEffect } from "react";

const deleteRoom = () => {
  console.log("deleting room");
  fetch(`/api/delete-room?room=newroom7`);
};

const children = ({ remainingTime }: any) => {
  const minutes = Math.floor(remainingTime / 60);
  const seconds = remainingTime % 60;

  return `${minutes}:${seconds}`;
};

export default function Countdown(props: any) {
  const remoteParticipants = useRemoteParticipants();
  const [shouldStart, setShouldStart] = useState(false);
  const [roomDuration, setRoomDuration] = useState(props.duration);

  useEffect(() => {
    const all = remoteParticipants.filter(p => !p.isAgent).length;
    if (all >= 1) { 
      setShouldStart(true);
    } else {
      setShouldStart(false);
    }
  });

  useEffect(() => {
    setRoomDuration(props.duration);
  }, [props.duration]);
  
  return (
    <span className="font-bold rounded-full bg-gradient-radial from-slate-900  to-transparent text-3xl absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 z-50">
      <CountdownCircleTimer
        size={120}
        trailStrokeWidth={6}
        isPlaying={shouldStart}
        duration={roomDuration}
        colors={["#004777", "#F7B801", "#A30000", "#A30000"]}
        colorsTime={[7, 5, 2, 0]}
        onComplete={deleteRoom}
      >
        {children}
      </CountdownCircleTimer>
    </span>
  );
}
