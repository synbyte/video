"use client"
import { useState } from "react"

export default function Page() {
    const [room, setRoom] = useState("");
    const [msg, setMsg] = useState("");

    const deleteRoom = () => {
        console.log("deleting room: ", room);
        fetch(`/api/delete-room?room=${room}`);
        setMsg("Room deleted: "+ room);
      };

  return <div className="flex w-screen">
    <div className="flex flex-col justify-center mx-auto items-center bg-slate-400 p-10 rounded-md space-y-2">
    <select value={room} onChange={(e) => setRoom(e.target.value)} className="bg-slate-900 p-1 mx-2 ring-2 ring-purple-900 rounded-md text-slate-100" name="" id=""><option value="room1">room1</option>
        <option value="room2" className="bg-slate-900 p-1 mx-2 ring-2 ring-purple-900 rounded-md text-slate-100">room2</option>
        <option value="room3">room3</option>
        <option value="room4">room4</option>
        <option value="room5">room5</option>
        <option value="room6">room6</option>
        </select>
        <button onClick={deleteRoom} className="border border-black rounded-md p-1">KILL ROOM</button>
        <p className="bg-slate-800 p-3 border border-black text-xs tracking-wide uppercase">{msg}</p></div></div>
}