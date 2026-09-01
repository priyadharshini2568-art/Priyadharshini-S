 const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");

// Mood keywords
const moods = {
  sad: ["sad", "depressed", "unhappy", "angry", "tired"],
  happy: ["happy", "good", "excited", "great", "joy", "awesome"],
  stressed: ["stressed", "anxious", "worried", "overwhelmed"]
};

// Tips per mood
const tips = {
  sad: [
    "Take a deep breath 🌬",
    "Listen to calming music 🎵",
    "Write down your thoughts ✍"
  ],
  happy: [
    "Keep smiling 😄",
    "Celebrate your small wins 🏆",
    "Do something fun today 🎉"
  ],
  stressed: [
    "Try a 5-minute meditation 🧘",
    "Stretch your body and relax 🖐",
    "Listen to relaxing music 🎧"
  ],
  neutral: [
    "Take a short walk 🚶‍♂",
    "Focus on small positive moments 🌸",
    "Try deep breathing exercises 🧘"
  ]
};

// Detect mood
function detectMood(message) {
  const msg = message.toLowerCase();
  for (let word of moods.sad) if (msg.includes(word)) return "sad";
  for (let word of moods.happy) if (msg.includes(word)) return "happy";
  for (let word of moods.stressed) if (msg.includes(word)) return "stressed";
  return "neutral";
}

// Generate response
function generateResponse(mood) {
  const tipList = tips[mood];
  const tip = tipList[Math.floor(Math.random() * tipList.length)];
  if (mood === "sad") return "I'm here for you 💛.";
  if (mood === "happy") return "Yay! 😄 ";
  if (mood === "stressed") return "Don't worry 😰. ";
  return "Thanks for sharing 🙂. ";
}

// Display bot response with typing effect and optional breathing card
function displayBotResponse(response, mood) {
  const botMsgDiv = document.createElement("div");
  botMsgDiv.textContent = "Bot is typing...";
  botMsgDiv.classList.add("bot-msg");
  chatBox.appendChild(botMsgDiv);
  chatBox.scrollTop = chatBox.scrollHeight;

  setTimeout(() => {
    botMsgDiv.textContent = "Bot: " + response;
    botMsgDiv.classList.add(mood);

    // If mood is sad or stressed, add breathing card
    if (mood === "sad" || mood === "stressed") {
      const card = document.createElement("div");
      card.classList.add("breathing-card");
      card.textContent = "💡 Tip: Try 4-7-8 breathing: Inhale 4s, Hold 7s, Exhale 8s.";
      chatBox.appendChild(card);
    }

    chatBox.scrollTop = chatBox.scrollHeight;
  }, 800);
}

// Send message
sendBtn.addEventListener("click", () => {
  const message = userInput.value.trim();
  if (!message) return;

  const userMsgDiv = document.createElement("div");
  userMsgDiv.textContent = "You: " + message;
  userMsgDiv.classList.add("user-msg");
  chatBox.appendChild(userMsgDiv);

  userInput.value = "";

  const mood = detectMood(message);
  const response = generateResponse(mood);
  displayBotResponse(response, mood);
});

// Enter key to send
userInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") sendBtn.click();
});