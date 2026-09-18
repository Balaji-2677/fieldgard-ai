/**
 * Kisan AI Assistant Chat Logic
 */

document.addEventListener("DOMContentLoaded", () => {
  const chatForm = document.getElementById("chat-form");
  const chatInput = document.getElementById("chat-input");

  if (chatForm) {
    chatForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const message = chatInput.value.trim();
      if (!message) return;
      chatInput.value = "";
      await sendChatMessage(message);
    });
  }
});

function sendSuggestion(text) {
  const chatInput = document.getElementById("chat-input");
  if (chatInput) {
    chatInput.value = text;
    sendChatMessage(text);
  }
}

async function sendChatMessage(message) {
  const chatMessages = document.getElementById("chat-messages");
  const sendBtn = document.getElementById("chat-send-btn");
  if (!chatMessages) return;

  // Append User Bubble
  appendUserMessage(message);

  // Append Typing Indicator
  const typingId = "typing-" + Date.now();
  appendTypingIndicator(typingId);
  scrollToBottom();

  if (sendBtn) sendBtn.disabled = true;

  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: message }),
    });

    const data = await res.json();
    removeTypingIndicator(typingId);

    if (data.success && data.reply) {
      appendAiMessage(data.reply);
      if (data.suggestions && data.suggestions.length > 0) {
        updateSuggestionChips(data.suggestions);
      }
    } else {
      appendAiMessage("I apologize, but I could not process your query. Please try asking again or contact the Kisan Call Center at 1800-180-1551.");
    }
  } catch (err) {
    removeTypingIndicator(typingId);
    appendAiMessage("Network connection error. Please check your internet connection.");
    console.error(err);
  } finally {
    if (sendBtn) sendBtn.disabled = false;
    scrollToBottom();
  }
}

function appendUserMessage(text) {
  const chatMessages = document.getElementById("chat-messages");
  const bubble = document.createElement("div");
  bubble.className = "chat-bubble user-bubble";
  bubble.innerHTML = `
    <div class="chat-text">${escapeHtml(text)}</div>
    <div class="chat-avatar">🧑‍🌾</div>
  `;
  chatMessages.appendChild(bubble);
}

function appendAiMessage(rawText) {
  const chatMessages = document.getElementById("chat-messages");
  const bubble = document.createElement("div");
  bubble.className = "chat-bubble ai-bubble";
  bubble.innerHTML = `
    <div class="chat-avatar">🌾</div>
    <div class="chat-text">${formatMarkdown(rawText)}</div>
  `;
  chatMessages.appendChild(bubble);
}

function appendTypingIndicator(id) {
  const chatMessages = document.getElementById("chat-messages");
  const indicator = document.createElement("div");
  indicator.id = id;
  indicator.className = "chat-bubble ai-bubble";
  indicator.innerHTML = `
    <div class="chat-avatar">🌾</div>
    <div class="chat-text" style="font-style: italic; color: #6b7280;">
      <span>Kisan AI is analyzing your farming query...</span>
    </div>
  `;
  chatMessages.appendChild(indicator);
}

function removeTypingIndicator(id) {
  const el = document.getElementById(id);
  if (el) el.remove();
}

function updateSuggestionChips(suggestions) {
  const container = document.getElementById("suggestion-chips");
  if (!container) return;
  container.innerHTML = suggestions
    .map(
      (s) =>
        `<button type="button" class="chip-btn" onclick="sendSuggestion(this.innerText)">${escapeHtml(s)}</button>`
    )
    .join("");
}

function scrollToBottom() {
  const chatMessages = document.getElementById("chat-messages");
  if (chatMessages) {
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }
}

function formatMarkdown(text) {
  let html = escapeHtml(text);
  // Headers
  html = html.replace(/^### (.*$)/gim, '<h4 style="margin: 6px 0; color: #1e7e34;">$1</h4>');
  // Bold
  html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
  // Italics
  html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');
  // Bullet points
  html = html.replace(/^[•\-] (.*$)/gim, '<li style="margin-left: 18px;">$1</li>');
  // Newlines
  html = html.replace(/\n\n/g, '<div style="margin-top: 8px;"></div>');
  html = html.replace(/\n/g, '<br>');
  return html;
}

function escapeHtml(string) {
  const entityMap = {
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;",
  };
  return String(string).replace(/[&<>"']/g, (s) => entityMap[s]);
}
