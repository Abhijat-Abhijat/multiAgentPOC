function copyOutput() {
  const text = document.getElementById("finalText").textContent;
  navigator.clipboard.writeText(text).then(() => {
    const btn = document.querySelector(".copy-btn");
    btn.textContent = "✅";
    setTimeout(() => (btn.textContent = "📋"), 1500);
  });
}
document.getElementById("inputText").addEventListener("keydown", function (e) {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault(); // prevent newline
    runSystem(); // send the message
  }
});

async function runSystem() {
  const inputField = document.getElementById("inputText");
  const userInput = inputField.value.trim();
  if (!userInput) return;

  appendMessage(userInput, "user");
  inputField.value = "";

  appendMessage("⏳ Running agents...", "bot");

  try {
    const res = await fetch("/run", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ input: userInput }),
    });

    const data = await res.json();

    // Remove the loading message
    removeLastBotMessageIf("⏳ Running agents...");

    // Log agent messages
    data.log.forEach((msg) => {
      const content = `🔄 ${msg.sender} ➝ ${msg.receiver}\n\n${JSON.stringify(
        msg.content,
        null,
        2
      )}`;
      appendMessage(content, "bot");
    });

    // Final output
    const final = data.final;
    const maybeCode = final.code || final.result || final;
    const finalText =
      typeof maybeCode === "string"
        ? maybeCode
        : JSON.stringify(maybeCode, null, 2);

    appendMessage(`✅ Final Output:\n${finalText}`, "bot");
    document.getElementById("finalText").textContent = finalText;
  } catch (err) {
    appendMessage("❌ Error running agents. Please try again.", "bot");
    console.error(err);
  }
}

function appendMessage(content, sender = "bot") {
  const chatWindow = document.getElementById("chatWindow");
  const message = document.createElement("div");
  message.className = `chat-message ${sender}`;
  message.textContent = content;
  chatWindow.appendChild(message);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

function removeLastBotMessageIf(textMatch) {
  const chatWindow = document.getElementById("chatWindow");
  const messages = Array.from(chatWindow.querySelectorAll(".chat-message.bot"));
  const last = messages[messages.length - 1];
  if (last && last.textContent.trim() === textMatch) {
    last.remove();
  }
}
