// Updated by EL, tested on my end..working 
// 9/26/24
// Take parts you need, forgo other parts you don't need 
// might not compile correctly, will have to debug 


export function addVoiceAssistant(participants) {
    const assistantID = "VoiceAssistant";
  
    // Check if the participants object is available
    if (!participants || participants.length === 0) {
      console.error("Participants list is undefined or empty");
      return;
    }
  
    // Convert participants to an array if it's not already
    const participantsArray = Array.isArray(participants) ? participants : Array.from(participants.values());
  
    // Check if the assistant is already in the participants list by ID
    const assistantAlreadyInRoom = participantsArray.some(
      (participant) => participant.identity === assistantID
    );
  
    if (!assistantAlreadyInRoom) {
      // Log a message indicating the assistant has joined
      console.log("Voice Assistant has joined the room!");
      // Simulate adding the voice assistant (actual implementation may vary)
    } else {
      console.log("Voice Assistant is already in the room.");
    }
  }
  
  export function startRecording() {
    // Use MediaRecorder to record audio
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      console.error("Media devices not supported in this browser.");
      return;
    }
    console.log('getting media')
    navigator.mediaDevices.getUserMedia({ audio: true })
      .then(function (stream) {
        const mediaRecorder = new MediaRecorder(stream);
        console.log('got media')
        mediaRecorder.ondataavailable = function (event) {
          if (event.data.size > 0) {
            saveRecording(event.data);
            console.log('recording saved')
          }
        };
  
        mediaRecorder.start();
      })
      .catch(function (err) {
        console.error("Failed to access microphone", err);
      });
  }
  
  function saveRecording(blob) {
    console.log('saving recording')
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.style.display = "none";
    a.href = url;
    a.download = `recording_${Date.now()}.wav`;
    document.body.appendChild(a);
    a.click();
    URL.revokeObjectURL(url);
  }
  
  export function speakMessage(message) {
    const synth = window.speechSynthesis;
    const utterance = new SpeechSynthesisUtterance(message);
    utterance.voice = synth.getVoices().find(voice => voice.lang === 'en-US');
    utterance.rate = 1;
    synth.speak(utterance);
  }
  
  