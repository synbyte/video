'use client'
import { useState } from "react"
import { useRouter } from "next/navigation"

export default function Page() {
  const [userName, setUserName] = useState('');
  const [room, setRoom] = useState()
  const router = useRouter();

  const handleSubmit = async () => {
    if (!userName) return;
    //fetch(`/api/create-room?room=newroom&participantLimit=4`)
    console.log('created room')
    const res = await fetch(`/api/get-participant-token?room=${room}&username=${userName}`)
    const data = await res.json()
    const token = data.token
    if (token) {
      router.push(`/room?token=${token}`)
    } else {
      alert('Error getting token');
    }
  }
  return (
    <div className="h-screen w-screen flex justify-center items-center">
      <div className="bg-slate-400  align-middle justify-evenly flex flex-col border-slate-700 border-2 p-5 rounded-md space-y-3">
        <div className='mx-auto'><svg width="42" height="42" viewBox="0 0 56 57" fill="#201C5A" xmlns="http://www.w3.org/2000/svg"><path clipRule="evenodd" d="M9.874 7.078 2 11.77l.086 15.645c.132 15.413.132 15.644 1.125 17.115 1.383 2.069 15.84 10.995 16.92 10.446 2.771-1.428 15.105-9.202 14.973-9.433-.086-.14-3.157-2.069-6.795-4.326-3.633-2.209-7.1-4.51-7.616-5.016-2.21-2.068-2.25-2.392-2.25-18.677 0-8.329-.132-15.181-.304-15.181-.213-.006-3.891 2.111-8.265 4.735Z"></path><path clipRule="evenodd" d="M28.434 6.65c-4.24 2.574-7.616 4.783-7.484 4.966.086.183 3.157 2.16 6.795 4.418 3.633 2.208 7.1 4.509 7.662 5.015 2.118 1.977 2.21 2.855 2.21 18.91 0 8.236.131 14.954.344 14.906.172 0 3.81-2.117 8.092-4.693l7.789-4.692.086-15.181c.132-19.184.993-17.115-9.39-23.558C40.383 4.117 36.79 2 36.532 2c-.223.005-3.902 2.123-8.098 4.65Z"></path></svg>
        </div>
        
        <input id="name" onChange={(e) => setUserName(e.target.value)} placeholder="Enter your name" type="text" className="bg-slate-900 p-1 mx-2 ring-2 ring-purple-900 rounded-md text-slate-100" />
        <select value={room} onChange={(e) => setRoom(e.target.value)} className="bg-slate-900 p-1 mx-2 ring-2 ring-purple-900 rounded-md text-slate-100" name="" id=""><option value="room1">room1</option>
        <option value="room2">room2</option>
        <option value="room3">room3</option>
        <option value="room4">room4</option>
        <option value="room5">room5</option>
        <option value="room6">room6</option>
        </select>
       <button onClick={handleSubmit} className='bg-slate-800 rounded-md ring-2 ring-purple-900 w-1/2 mx-auto'>Enter</button>
      </div>
    </div>
  )
}