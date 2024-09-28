'use client'
import { useState } from "react"
import { useRouter } from "next/navigation"

export default function Page() {
  const [userName, setUserName] = useState('');
  const router = useRouter();

  const handleSubmit = async () => {
    if (!userName) return;
    fetch(`/api/create-room?room=newroom&participantLimit=4`)
    console.log('created room')
    const res = await fetch(`/api/get-participant-token?room=newroom&username=${userName}`)
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
      <div className="bg-slate-800 h-1/5 align-middle justify-evenly flex flex-col border-slate-700 border-2 p-5 rounded-md space-y-3">
        <p className="mx-auto">Enter name and press enter</p>
        <input onChange={(e) => setUserName(e.target.value)} placeholder="Enter your name" type="text" className="bg-slate-900 ring-2 rounded-md text-slate-100" />
        <button onClick={handleSubmit} className='bg-slate-500 rounded-md w-1/2 mx-auto'>Enter</button>
      </div>
    </div>
  )
}