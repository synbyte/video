import random

ifa_jokes = [
    "Wow, this silence is so loud, I can almost hear the Wi-Fi thinking.",
    "This silence is so thick, it needs a GPS to find its way out.",
    "This silence is so quiet, even the crickets are holding their breath.",
    "Wow, this silence is so heavy, I think I just pulled a muscle.",
    "This silence is so profound, I could swear it has its own philosophy degree.",
    "This silence is so awkward, it’s like an elephant trying to tiptoe.",
    "This silence is so loud, I can hear my thoughts filing for a noise complaint.",
    "Wow, this silence is so deafening, I can hear my heart whispering.",
    "This silence is so chilling, I feel like I’m in a horror movie without the popcorn.",
    "This silence is so pregnant, it’s about to give birth to a thousand conversations.",
    "Wow, this silence is so thick, it could use a chainsaw to break through.",
    "This silence is so quiet, I can hear my own hair growing.",
    "This silence is so echoey, even my thoughts are echoing back.",
    "Wow, this silence is so loud, I think my ears just filed for divorce.",
    "This silence is so heavy, it feels like I’m carrying a mountain on my shoulders.",
    "This silence is so intense, it feels like a 4D movie without the sound!",
    "Wow, this silence is so loud, I think it just joined a rock band.",
    "This silence is so thick, I need a shovel to get through it.",
    "This silence is so silent, I’m starting to question my hearing.",
    "Wow, this silence is so awkward, it could make a mime blush.",
    "This silence is so loud, I think my neighbors are planning a surprise party.",
    "This silence is so heavy, it should come with a warning label.",
    "Wow, this silence is so eerie, even ghosts are afraid to break it.",
    "This silence is so loud, I can hear my wallet crying.",
    "This silence is so still, I feel like I’m in a meditation retreat without the chanting.",
    "Wow, this silence is so silent, it needs a megaphone to express itself.",
    "This silence is so loud, I think my neighbors are throwing a rave.",
    "This silence is so thick, it needs its own air freshener.",
    "Wow, this silence is so profound, I can hear the universe contemplating its existence.",
    "This silence is so heavy, it should probably have a life coach.",
    "Wow, this silence is so loud, I can hear my past mistakes echoing back.",
    "This silence is so quiet, even the mice are too scared to squeak.",
    "Wow, this silence is so thick, it could be used as a blanket.",
    "This silence is so heavy, I feel like I’m swimming in molasses.",
    "Wow, this silence is so loud, I can hear the grass growing.",
    "This silence is so deafening, it deserves a Grammy.",
    "Wow, this silence is so quiet, even my phone is afraid to ring.",
    "This silence is so still, it could be a meditation guide.",
    "Wow, this silence is so awkward, it should come with an exit strategy.",
    "This silence is so loud, I think my ears are planning a protest.",
    "Wow, this silence is so thick, I need a pair of scissors to cut through it.",
    "This silence is so heavy, it’s practically a weightlifting competition.",
    "Wow, this silence is so profound, I’m starting to question my existence.",
    "This silence is so loud, it’s drowning out my own thoughts.",
    "Wow, this silence is so quiet, it’s like a ninja in a library.",
    "This silence is so intense, I can feel it weighing down on my shoulders.",
    "Wow, this silence is so heavy, it should probably have a life coach.",
    "This silence is so loud, I can hear my neighbors' thoughts.",
    "Wow, this silence is so thick, it should be studied in a science class.",
    "This silence is so quiet, it feels like walking through a graveyard at midnight.",
    "Wow, this silence is so deafening, I think I just broke my own eardrums.",
    "This silence is so heavy, it could make a boulder feel light.",
    "Wow, this silence is so profound, it’s giving me existential dread.",
    "This silence is so loud, I can hear my conscience whispering.",
    "Wow, this silence is so thick, it could be used as soundproofing.",
    "This silence is so quiet, I’m considering charging it rent.",
    "Wow, this silence is so heavy, I think it just gave me a hernia.",
    "This silence is so awkward, it feels like an elephant in a room full of mice.",
    "Wow, this silence is so loud, I can almost hear the universe plotting.",
    "This silence is so profound, it’s practically a philosophical debate.",
    "Wow, this silence is so thick, it needs a chainsaw to get through.",
    "This silence is so heavy, it could cause an earthquake.",
    "Wow, this silence is so deafening, even my ears are asking for a break.",
    "This silence is so quiet, I could hear a pin drop in the next galaxy.",
    "Wow, this silence is so awkward, it could be a sitcom waiting to happen.",
    "This silence is so thick, I could use it to make a smoothie.",
    "Wow, this silence is so loud, it’s got its own echo chamber.",
    "This silence is so profound, it could write a bestselling novel.",
    "Wow, this silence is so heavy, it needs its own transportation service.",
    "This silence is so quiet, even the dust bunnies are being respectful.",
    "Wow, this silence is so intense, it could be a plot twist in a thriller.",
    "This silence is so loud, it could make a rock concert sound like a whisper.",
    "Wow, this silence is so heavy, it’s practically begging for a lifeguard.",
    "This silence is so deafening, I think I just heard my future.",
    "Wow, this silence is so awkward, it could be a first date gone wrong.",
    "This silence is so thick, I feel like I’m wading through molasses.",
    "Wow, this silence is so loud, it’s giving the vacuum cleaner a run for its money.",
    "This silence is so quiet, it feels like the calm before a storm.",
    "Wow, this silence is so profound, I think it just invented a new philosophy.",
    "This silence is so heavy, it’s got its own gravitational pull.",
    "Wow, this silence is so loud, it could wake the neighbors' dog.",
    "This silence is so thick, it needs a bulldozer to clear it out.",
    "Wow, this silence is so loud, I can hear my own heartbeat echoing.",
    "This silence is so quiet, it feels like the universe is holding its breath.",
    "Wow, this silence is so heavy, it should come with a gym membership.",
    "This silence is so profound, it’s about to start a TED Talk.",
    "Wow, this silence is so thick, it could fill a library with unspoken words.",
    "This silence is so loud, it’s drowning out my thoughts of what to have for lunch.",
    "Wow, this silence is so silent, it could win an Oscar for Best Performance.",
    "This silence is so heavy, I think it just gave my brain a workout.",
    "Wow, this silence is so loud, even my thoughts are trying to sneak out.",
    "This silence is so awkward, it could make a mime look talkative.",
    "Wow, this silence is so thick, it could use a drill to break through.",
    "This silence is so deafening, I’m considering hiring a sound engineer.",
    "Wow, this silence is so quiet, even my imagination is on vacation.",
    "This silence is so heavy, it’s causing tectonic shifts in my mind.",
    "Wow, this silence is so loud, I think I can hear the thoughts of the cat next door.",
    "This silence is so profound, it’s creating a ripple effect of introspection.",
    "Wow, this silence is so thick, it needs its own theme music.",
    "This silence is so loud, it feels like the start of a superhero movie.",
    "Wow, this silence is so silent, I could hear a butterfly flapping its wings.",
    "This silence is so heavy, it’s a workout for my ears just to listen to it.",
    "Wow, this silence is so awkward, it should come with a manual.",
    "This silence is so loud, I think the walls are gossiping.",
    "Wow, this silence is so thick, it’s practically a fog.",
    "This silence is so quiet, even my dog is confused.",
    "Wow, this silence is so profound, it should have its own Instagram account.",
    "This silence is so heavy, it should probably take a break.",
    "Wow, this silence is so loud, I’m starting to hear the sound of my own anxiety."]

# FUNCTION FOR RANDOM JOKE
def random_joke():
    return random.choice(ifa_jokes)

# FUNCTION TO GENERATE GREETING VARIATION
def generate_greeting_variation():
    intros = [
        "Welcome to your figbox session!",
        "Hello and welcome to figbox!",
        "Great to see you in this figbox session!",
        "Welcome aboard your figbox experience!"
    ]
    
    feelings = [
        "I have a good feeling about this match!",
        "I'm excited about the potential of this pairing!",
        "This match looks promising!",
        "I think you two will hit it off!"
    ]
    
    instructions = [
        "Please introduce yourselves.",
        "Why don't you start by introducing yourselves?",
        "Let's begin with some introductions.",
        "How about we kick things off with some introductions?"
    ]
    
    profile_building = [
        "In the meantime, I'll start building a cognitive profile for both of you to learn about your needs.",
        "While you chat, I'll be creating a cognitive profile to understand your needs better.",
        "As you talk, I'll be working on cognitive profiles to get to know you both.",
        "During your conversation, I'll be developing cognitive profiles to better understand you."
    ]
    
    matching = [
        "This will help me find better matches.",
        "This information will be useful for future matching.",
        "These insights will improve our matching process.",
        "Your profiles will enhance our ability to create great matches."
    ]
    
    purpose = [
        "I'm also here to make the conversation fun, relaxed, and insightful.",
        "My goal is to ensure your conversation is enjoyable, comfortable, and meaningful.",
        "I'm here to facilitate a fun, easygoing, and enlightening discussion.",
        "Count on me to keep things entertaining, laid-back, and thought-provoking."
    ]
    
    closing = [
        "Let me know if you need anything!",
        "Don't hesitate to ask if you need assistance!",
        "I'm here if you need any help!",
        "Feel free to reach out if you need support!"
    ]
    
    variation = (
        f"{random.choice(intros)} {random.choice(feelings)} {random.choice(instructions)} "
        f"{random.choice(profile_building)} {random.choice(matching)} {random.choice(purpose)} "
        f"{random.choice(closing)}"
    )
    
    return variation

# FUNCTION TO GENERATE CLOSING VARIATION
def generate_closing_variation():
    intros = [
        "Hey guys, I just want to let you know that",
        "Just a heads up,",
        "Time flies when you're having a great discussion!",
        "Quick time check:",
        "Attention all!",
        "Friendly reminder:",
        "Time update:",
        "We're nearing the finish line with",
        "Tick tock!"
    ]
    
    time_statements = [
        "I've been tracking the time, and you have 5 minutes left before the session ends.",
        "we're approaching the end of our session. There are 5 minutes remaining.",
        "We've got 5 minutes left in this session.",
        "5 minutes left on the clock.",
        "We're in the home stretch with just 5 minutes to go.",
        "Our session wraps up in 5 minutes.",
        "5 minutes remaining in our session.",
        "5 minutes left.",
        "Only 5 minutes remain in our session."
    ]
    
    suggestions = [
        "You might want to add each other to your list of collaborators on figbox and continue the conversation afterward.",
        "Don't forget to add each other as collaborators on figbox if you'd like to continue your conversation later.",
        "Remember, you can add each other as figbox collaborators to keep the conversation going.",
        "If you're enjoying the chat, why not add each other as collaborators on figbox to pick up where you leave off?",
        "Consider exchanging figbox collaborator invites to continue your fascinating discussion after the session.",
        "To keep the momentum going, you might want to become figbox collaborators and carry on your conversation post-session.",
        "If you're keen to continue this engaging dialogue, don't forget the option to add each other as figbox collaborators.",
        "To ensure you don't lose touch, consider adding each other to your figbox collaborator list for future conversations.",
        "Want to keep chatting? Remember you can add each other as collaborators on figbox to continue later."
    ]
    
    reminder = f"{random.choice(intros)} {random.choice(time_statements)} {random.choice(suggestions)}"
    return reminder