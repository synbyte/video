// Uses useRemoteParticipants hook to count participants and decide what to render
"use client";
import { useEffect, useState, useRef } from "react";
import { LiveKitRoom } from "@livekit/components-react";
import { useSearchParams } from "next/navigation"
import "@livekit/components-styles";
import ConferenceRoom from "../ConferenceRoom";
import Countdown from "../Countdown";


export default function Page() {
  const [token, setToken] = useState("");
  const [roomDuration, setRoomDuration] = useState(20 * 60); // 20
  const [maxParticipants, setMaxParticipants] = useState(4); // Max number of participants allowed
  const roomRef = useRef<HTMLDivElement | null>(null);
  const searchParams = useSearchParams();
  

  useEffect(() => {
    const token = searchParams.get("token");
    if (token) {
      setToken(token);
    }
  }, [searchParams]);
  

  if (token === "") {
    return <div>Getting token...</div>;
  }

  return (
    <LiveKitRoom
      video={true}
      audio={true}
      token={token}
      serverUrl={process.env.NEXT_PUBLIC_LIVEKIT_URL}
      data-lk-theme="default"
      style={{ height: "100dvh" }}
      ref={roomRef}
    ><Countdown  duration={roomDuration} />
      <ConferenceRoom participantLimit={maxParticipants} />
     
    </LiveKitRoom>
  );
}
