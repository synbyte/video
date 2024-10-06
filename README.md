[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/synbyte/video)

  

# Getting Started

## Requirements

- **Cartesia API key** - Sign up and get at https://play.cartesia.ai/keys

- **LiveKit API key, secret, and URL** - Get from https://cloud.livekit.io -> Settings -> Keys

  

# Set Environment Variables

## In the root directory (/video) create 2 files: ".env.local" and ".env"

Get your **LiveKit** API **key**, API **secret**, and **URL**, then place them inside "**.env.local**" like this :

  

```bash

LIVEKIT_API_KEY=

LIVEKIT_API_SECRET=

NEXT_PUBLIC_LIVEKIT_URL=

```

  

Then add them PLUS your **Cartesia** API key to "**.env**" like this:

  

```bash

LIVEKIT_API_KEY=

LIVEKIT_API_SECRET=

LIVEKIT_URL=

CARTESIA_API_KEY=

```

## *Notice that in ".env.local" its "**NEXT_PLUBLIC**_LIVEKIT_URL" and in ".env" its just "LIVEKIT_URL"*

  

# Install Dependencies

## **STEP 1) In the terminal make sure you are in the root directory (/video)**

Install the **node** dependencies by typing:

    npm install


## **STEP 2) Then, move into the Ifa  directory (/video/Ifa) by typing:**

    cd Ifa

Install the **python** dependencies by typing:

    pip install -r requirements.txt

# Run Platform and Agent
 

## STEP 1) Start the agent

In your **terminal** you should be in the **Ifa** directory (/video/Ifa). 

When you start the agent, it waits for a room to **startup** and automatically connects to it.


To start agent type:

    python main.py dev

Sometimes when testing, when you disconnect from a room and join again, the agent won't join because the room hasn't had a chance to **shutdown** and **startup** again. This is when you can choose a different room to connect to, OR stop the agent **(CTRL-C)** and use the this command to tell the agent which room to connect to, for example "room1":

    python main.dev connect --room room1

## STEP 2) Start the platform
Open a **new** **terminal** by pressing **(CTRL+SHIFT+~)**, the other terminal should be busy running the agent.  Make sure you are in the **root** directory (/video), and run:

    npm run dev


## TODO

  

- [x] ~~ConferenceRoom.tsx - When room is full, the participant trying to join gets the 'Room is full' message, but his tracks still get published to the room. Stop tracks from publishing~~

- [ ] Countdown.tsx - ~~Timer starts when at least 2 ppl are in room, if 3rd participant joins later, or someone leaves and rejoins, their timer restarts~~. **Find a way to sync all timers.**

- [x] ~~ControlBar.tsx - Build out buttons with correct hooks.~~
- [x] ~~Add agent to record participant audio~~
- [x] ~~Add agent to room in custom tile~~
- [ ] Have agent save audio transcription