/**
 * Kisan AI - Agricultural ChatGPT Engine (Frontend)
 * Features:
 * - Multi-conversation history stored in localStorage (New Chat, Switch, Delete)
 * - Real-time word-by-word streaming typewriter effect with cursor
 * - Stop generation button
 * - Voice Input (Speech-to-Text with SpeechRecognition)
 * - Text-to-Speech Voice Output (Read Aloud)
 * - One-click Copy to clipboard
 * - Regenerate response
 * - Auto-expanding multiline textarea with Enter to send
 */

const STORAGE_KEY = "kisan_ai_conversations_v4";
let conversations = [];
let currentChatId = null;
let isStreaming = false;
let stopStreamingRequested = false;
let recognition = null;
let isRecordingVoice = false;
let currentUtterance = null;

// Initialize on DOM ready
document.addEventListener("DOMContentLoaded", () => {
  loadConversationsFromStorage();

  const chatInput = document.getElementById("chat-input");
  if (chatInput) {
    // Auto-expanding textarea
    chatInput.addEventListener("input", function () {
      this.style.height = "auto";
      this.style.height = Math.min(this.scrollHeight, 160) + "px";
      updateSendButtonState();
    });

    // Enter to send, Shift+Enter for new line
    chatInput.addEventListener("keydown", function (e) {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        handleSendClick();
      }
    });
  }

  // Setup Web Speech API for voice input if supported
  initSpeechRecognition();

  // If no chat selected, start new chat or load the most recent
  if (conversations.length > 0) {
    switchChat(conversations[0].id);
  } else {
    startNewChat();
  }
});

/* ==========================================================================
   💬 Conversation Session Management (localStorage)
   ========================================================================== */

function loadConversationsFromStorage() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    conversations = raw ? JSON.parse(raw) : [];
  } catch (err) {
    console.error("Error loading chat history:", err);
    conversations = [];
  }
  renderSidebarList();
}

function saveConversationsToStorage() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(conversations));
  } catch (err) {
    console.error("Error saving chat history:", err);
  }
  renderSidebarList();
}

function getCurrentConversation() {
  return conversations.find((c) => c.id === currentChatId);
}

function startNewChat() {
  if (isStreaming) stopGenerating();

  const newId = "chat_" + Date.now();
  currentChatId = newId;

  // Clear messages area & show welcome screen
  const messagesContainer = document.getElementById("chat-messages");
  if (messagesContainer) {
    messagesContainer.innerHTML = `
      <div class="chatgpt-welcome" id="chatgpt-welcome">
        <div class="welcome-avatar-glow">🌾</div>
        <h2 class="welcome-title">What would you like to cultivate today?</h2>
        <p class="welcome-subtitle">
          Ask any farming question: crop diseases, optimal sowing dates, fertilizer balance, pest control, or government welfare subsidies.
        </p>
        <div class="prompt-cards-grid">
          <div class="prompt-card" onclick="sendSuggestion('When is the optimal time to sow wheat in Punjab and UP?')">
            <div class="card-icon">🌾</div>
            <div class="card-title">Wheat Sowing Schedule</div>
            <div class="card-desc">Optimal sowing dates, varieties & seed rates</div>
          </div>
          <div class="prompt-card" onclick="sendSuggestion('What is the balanced N-P-K fertilizer dose for paddy?')">
            <div class="card-icon">🧪</div>
            <div class="card-title">Fertilizer Regimen</div>
            <div class="card-desc">Balanced Urea, DAP, Potash & Zinc dosing</div>
          </div>
          <div class="prompt-card" onclick="sendSuggestion('How to control bollworm in cotton?')">
            <div class="card-icon">🐛</div>
            <div class="card-title">Pest & Disease Control</div>
            <div class="card-desc">IPM, pheromone traps & organic remedies</div>
          </div>
          <div class="prompt-card" onclick="sendSuggestion('Government schemes for farmers')">
            <div class="card-icon">🏛️</div>
            <div class="card-title">Agricultural Subsidies</div>
            <div class="card-desc">PM-KISAN ₹6,000, PMFBY insurance & KCC</div>
          </div>
        </div>
      </div>
    `;
  }

  hideSuggestionBar();
  renderSidebarList();

  const chatInput = document.getElementById("chat-input");
  if (chatInput) {
    chatInput.value = "";
    chatInput.style.height = "auto";
    chatInput.focus();
  }

  // Close mobile sidebar if open
  closeSidebarOnMobile();
}

function switchChat(chatId) {
  if (isStreaming) stopGenerating();

  currentChatId = chatId;
  const conv = getCurrentConversation();
  if (!conv) {
    startNewChat();
    return;
  }

  const messagesContainer = document.getElementById("chat-messages");
  if (!messagesContainer) return;

  if (conv.messages.length === 0) {
    startNewChat();
    return;
  }

  messagesContainer.innerHTML = "";
  conv.messages.forEach((msg) => {
    if (msg.role === "user") {
      renderUserMessage(msg.content, false);
    } else {
      renderAiMessage(msg.content, false);
    }
  });

  // Load suggestions from last AI turn if available
  const lastMsg = conv.messages[conv.messages.length - 1];
  if (lastMsg && lastMsg.role === "assistant" && lastMsg.suggestions) {
    updateSuggestionChips(lastMsg.suggestions);
  } else {
    hideSuggestionBar();
  }

  scrollToBottom();
  renderSidebarList();
  closeSidebarOnMobile();
}

function deleteChat(chatId, event) {
  if (event) event.stopPropagation();
  conversations = conversations.filter((c) => c.id !== chatId);
  saveConversationsToStorage();

  if (currentChatId === chatId) {
    if (conversations.length > 0) {
      switchChat(conversations[0].id);
    } else {
      startNewChat();
    }
  }
}

function clearAllChats() {
  if (confirm("Are you sure you want to delete all saved conversations?")) {
    conversations = [];
    saveConversationsToStorage();
    startNewChat();
  }
}

function renderSidebarList() {
  const container = document.getElementById("sidebar-history-list");
  if (!container) return;

  if (conversations.length === 0) {
    container.innerHTML = `
      <div style="font-size: 0.78rem; color: #6b7280; padding: 12px 6px; text-align: center;">
        No saved chats yet.<br>Start a conversation!
      </div>
    `;
    return;
  }

  container.innerHTML = conversations
    .map(
      (c) => `
      <div class="history-item ${c.id === currentChatId ? "active" : ""}" onclick="switchChat('${c.id}')">
        <div class="history-title">
          <span>🌾</span>
          <span>${escapeHtml(c.title || "Farming Conversation")}</span>
        </div>
        <button type="button" class="history-delete-btn" onclick="deleteChat('${c.id}', event)" title="Delete chat">
          ✕
        </button>
      </div>
    `
    )
    .join("");
}

/* ==========================================================================
   🚀 Message Submission & Streaming Typewriter Effect
   ========================================================================== */

function sendSuggestion(text) {
  const chatInput = document.getElementById("chat-input");
  if (chatInput) {
    chatInput.value = text;
    handleSendClick();
  }
}

function handleSendClick() {
  if (isStreaming) {
    stopGenerating();
    return;
  }

  const chatInput = document.getElementById("chat-input");
  if (!chatInput) return;
  const message = chatInput.value.trim();
  if (!message) return;

  chatInput.value = "";
  chatInput.style.height = "auto";
  updateSendButtonState();

  submitUserMessage(message);
}

async function submitUserMessage(message) {
  // Remove welcome screen if visible
  const welcome = document.getElementById("chatgpt-welcome");
  if (welcome) welcome.remove();

  // Find or create current conversation
  let conv = getCurrentConversation();
  if (!conv) {
    conv = {
      id: currentChatId || "chat_" + Date.now(),
      title: message.length > 28 ? message.slice(0, 28) + "..." : message,
      timestamp: Date.now(),
      messages: [],
    };
    currentChatId = conv.id;
    conversations.unshift(conv);
  }

  // Add user message to state & render
  conv.messages.push({ role: "user", content: message });
  renderUserMessage(message, true);
  scrollToBottom();
  hideSuggestionBar();

  // Switch send button to Stop mode
  setStreamingState(true);

  // Render typing bubble container for AI
  const aiBubbleId = "ai-stream-" + Date.now();
  const aiTextEl = createStreamingAiBubble(aiBubbleId);
  scrollToBottom();

  // Prepare conversation history payload for multi-turn context
  const historyPayload = conv.messages.slice(0, -1).map((m) => ({
    role: m.role,
    content: m.content,
  }));

  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message: message,
        history: historyPayload,
      }),
    });

    const data = await res.json();

    if (data.success && data.reply) {
      // Perform word-by-word streaming typewriter effect
      await streamTextToElement(aiTextEl, data.reply);

      // Save complete reply to conversation state
      conv.messages.push({
        role: "assistant",
        content: data.reply,
        suggestions: data.suggestions || [],
      });
      saveConversationsToStorage();

      // Render action buttons (Copy, Read aloud, Regenerate)
      attachActionButtons(aiBubbleId, data.reply);

      // Render follow-up suggestions if available
      if (data.suggestions && data.suggestions.length > 0) {
        updateSuggestionChips(data.suggestions);
      }
    } else {
      aiTextEl.innerHTML = "I apologize, but I could not process your query. Please try asking again.";
    }
  } catch (err) {
    console.error("Chat API Error:", err);
    aiTextEl.innerHTML = "⚠️ Network error. Please check your connection and try again.";
  } finally {
    setStreamingState(false);
    scrollToBottom();
  }
}

/**
 * Word-by-word typewriter streaming effect
 */
async function streamTextToElement(element, fullText) {
  const words = fullText.split(" ");
  let accumulated = "";

  for (let i = 0; i < words.length; i++) {
    if (stopStreamingRequested) {
      break;
    }
    accumulated += (i === 0 ? "" : " ") + words[i];
    element.innerHTML = formatMarkdown(accumulated) + '<span class="blinking-cursor"></span>';
    scrollToBottom();

    // Natural typing delay (15ms - 25ms per word)
    const delay = words[i].includes("\n") ? 35 : 18;
    await new Promise((r) => setTimeout(r, delay));
  }

  // Remove blinking cursor at the end
  element.innerHTML = formatMarkdown(accumulated);
}

function stopGenerating() {
  stopStreamingRequested = true;
}

function setStreamingState(streaming) {
  isStreaming = streaming;
  stopStreamingRequested = false;
  const btn = document.getElementById("btn-input-send");
  if (!btn) return;

  if (streaming) {
    btn.classList.add("stop-mode");
    btn.setAttribute("title", "Stop generating");
    btn.innerHTML = `
      <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
        <rect x="4" y="4" width="16" height="16" rx="2"></rect>
      </svg>
    `;
  } else {
    btn.classList.remove("stop-mode");
    btn.setAttribute("title", "Send message");
    btn.innerHTML = `
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <line x1="12" y1="19" x2="12" y2="5"></line>
        <polyline points="5 12 12 5 19 12"></polyline>
      </svg>
    `;
  }
}

function updateSendButtonState() {
  const chatInput = document.getElementById("chat-input");
  const btn = document.getElementById("btn-input-send");
  if (!chatInput || !btn) return;

  if (!isStreaming) {
    btn.style.opacity = chatInput.value.trim() ? "1" : "0.7";
  }
}

/* ==========================================================================
   🖼️ Rendering Chat Messages
   ========================================================================== */

function renderUserMessage(text, animate) {
  const container = document.getElementById("chat-messages");
  if (!container) return;

  const row = document.createElement("div");
  row.className = "gpt-message-row gpt-user-row";
  row.innerHTML = `
    <div class="gpt-content-wrapper" style="align-items: flex-end;">
      <div class="gpt-user-content">${escapeHtml(text)}</div>
    </div>
    <div class="gpt-avatar gpt-user-avatar">🧑‍🌾</div>
  `;
  container.appendChild(row);
}

function createStreamingAiBubble(bubbleId) {
  const container = document.getElementById("chat-messages");
  const row = document.createElement("div");
  row.className = "gpt-message-row";
  row.id = bubbleId;

  row.innerHTML = `
    <div class="gpt-avatar gpt-ai-avatar">🌾</div>
    <div class="gpt-content-wrapper" style="flex: 1;">
      <div class="gpt-ai-content" id="${bubbleId}-text">
        <span class="blinking-cursor"></span>
      </div>
      <div class="gpt-action-bar" id="${bubbleId}-actions" style="display: none;"></div>
    </div>
  `;
  container.appendChild(row);
  return document.getElementById(`${bubbleId}-text`);
}

function renderAiMessage(fullText, animate) {
  const container = document.getElementById("chat-messages");
  if (!container) return;

  const bubbleId = "ai-msg-" + Math.random().toString(36).substr(2, 9);
  const row = document.createElement("div");
  row.className = "gpt-message-row";
  row.id = bubbleId;

  row.innerHTML = `
    <div class="gpt-avatar gpt-ai-avatar">🌾</div>
    <div class="gpt-content-wrapper" style="flex: 1;">
      <div class="gpt-ai-content">${formatMarkdown(fullText)}</div>
      <div class="gpt-action-bar">
        <button type="button" class="gpt-action-btn" onclick="copyReplyText(this, '${escapeForAttribute(fullText)}')">
          📋 Copy
        </button>
        <button type="button" class="gpt-action-btn" onclick="toggleReadAloud(this, '${escapeForAttribute(fullText)}')">
          🔊 Read Aloud
        </button>
        <button type="button" class="gpt-action-btn" onclick="regenerateLastMessage()">
          🔄 Regenerate
        </button>
      </div>
    </div>
  `;
  container.appendChild(row);
}

function attachActionButtons(bubbleId, fullText) {
  const actionsContainer = document.getElementById(`${bubbleId}-actions`);
  if (!actionsContainer) return;

  actionsContainer.style.display = "flex";
  actionsContainer.innerHTML = `
    <button type="button" class="gpt-action-btn" onclick="copyReplyText(this, '${escapeForAttribute(fullText)}')">
      📋 Copy
    </button>
    <button type="button" class="gpt-action-btn" onclick="toggleReadAloud(this, '${escapeForAttribute(fullText)}')">
      🔊 Read Aloud
    </button>
    <button type="button" class="gpt-action-btn" onclick="regenerateLastMessage()">
      🔄 Regenerate
    </button>
  `;
}

/* ==========================================================================
   📋 Actions: Copy, Read Aloud, Regenerate
   ========================================================================== */

function copyReplyText(button, text) {
  navigator.clipboard.writeText(text).then(() => {
    const originalText = button.innerHTML;
    button.innerHTML = "✓ Copied!";
    button.style.color = "#16a34a";
    setTimeout(() => {
      button.innerHTML = originalText;
      button.style.color = "";
    }, 2000);
  });
}

function toggleReadAloud(button, text) {
  if (!window.speechSynthesis) {
    alert("Text-to-speech is not supported in this browser.");
    return;
  }

  if (window.speechSynthesis.speaking) {
    window.speechSynthesis.cancel();
    button.innerHTML = "🔊 Read Aloud";
    button.style.color = "";
    return;
  }

  // Strip markdown formatting for cleaner audio reading
  const cleanSpeechText = text
    .replace(/[#*•\-_`]/g, "")
    .replace(/\n+/g, ". ");

  currentUtterance = new SpeechSynthesisUtterance(cleanSpeechText);
  currentUtterance.rate = 1.0;
  currentUtterance.pitch = 1.0;

  button.innerHTML = "⏹️ Stop Reading";
  button.style.color = "#15803d";

  currentUtterance.onend = () => {
    button.innerHTML = "🔊 Read Aloud";
    button.style.color = "";
  };

  currentUtterance.onerror = () => {
    button.innerHTML = "🔊 Read Aloud";
    button.style.color = "";
  };

  window.speechSynthesis.speak(currentUtterance);
}

function regenerateLastMessage() {
  const conv = getCurrentConversation();
  if (!conv || conv.messages.length === 0) return;

  // Find the last user message
  let lastUserMsg = null;
  for (let i = conv.messages.length - 1; i >= 0; i--) {
    if (conv.messages[i].role === "user") {
      lastUserMsg = conv.messages[i].content;
      // Remove trailing assistant message if present
      conv.messages.splice(i + 1);
      break;
    }
  }

  if (lastUserMsg) {
    // Re-render conversation up to that point
    switchChat(conv.id);
    submitUserMessage(lastUserMsg);
  }
}

/* ==========================================================================
   🎤 Voice Input (Speech-to-Text via Web Speech API)
   ========================================================================== */

function initSpeechRecognition() {
  const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRec) {
    const micBtn = document.getElementById("btn-input-mic");
    if (micBtn) micBtn.style.display = "none";
    return;
  }

  recognition = new SpeechRec();
  recognition.continuous = false;
  recognition.interimResults = true;
  recognition.lang = "en-IN"; // Supports English (India) with regional recognition

  recognition.onstart = () => {
    isRecordingVoice = true;
    const micBtn = document.getElementById("btn-input-mic");
    if (micBtn) micBtn.classList.add("mic-recording");
  };

  recognition.onresult = (event) => {
    let transcript = "";
    for (let i = event.resultIndex; i < event.results.length; ++i) {
      transcript += event.results[i][0].transcript;
    }
    const chatInput = document.getElementById("chat-input");
    if (chatInput && transcript) {
      chatInput.value = transcript;
      chatInput.style.height = "auto";
      chatInput.style.height = Math.min(chatInput.scrollHeight, 160) + "px";
      updateSendButtonState();
    }
  };

  recognition.onerror = (event) => {
    console.warn("Speech recognition error:", event.error);
    stopVoiceInput();
  };

  recognition.onend = () => {
    stopVoiceInput();
  };
}

function toggleVoiceInput() {
  if (!recognition) {
    alert("Voice microphone input is not supported in this browser. Please try Google Chrome or Edge.");
    return;
  }

  if (isRecordingVoice) {
    recognition.stop();
    stopVoiceInput();
  } else {
    try {
      recognition.start();
    } catch (err) {
      console.warn("Could not start recognition:", err);
    }
  }
}

function stopVoiceInput() {
  isRecordingVoice = false;
  const micBtn = document.getElementById("btn-input-mic");
  if (micBtn) micBtn.classList.remove("mic-recording");
}

/* ==========================================================================
   🛠️ UI Utilities & Markdown Parser
   ========================================================================== */

function toggleSidebar() {
  const sidebar = document.getElementById("chatgpt-sidebar");
  const overlay = document.getElementById("sidebar-overlay");
  if (sidebar) sidebar.classList.toggle("open");
  if (overlay) overlay.classList.toggle("active");
}

function closeSidebarOnMobile() {
  const sidebar = document.getElementById("chatgpt-sidebar");
  const overlay = document.getElementById("sidebar-overlay");
  if (sidebar) sidebar.classList.remove("open");
  if (overlay) overlay.classList.remove("active");
}

function updateSuggestionChips(suggestions) {
  const bar = document.getElementById("suggestion-bar");
  const container = document.getElementById("suggestion-chips");
  if (!bar || !container) return;

  container.innerHTML = suggestions
    .map(
      (s) =>
        `<button type="button" class="chip-btn" onclick="sendSuggestion('${escapeForAttribute(s)}')">${escapeHtml(s)}</button>`
    )
    .join("");
  bar.style.display = "block";
}

function hideSuggestionBar() {
  const bar = document.getElementById("suggestion-bar");
  if (bar) bar.style.display = "none";
}

function scrollToBottom() {
  const messages = document.getElementById("chat-messages");
  if (messages) {
    messages.scrollTop = messages.scrollHeight;
  }
}

function formatMarkdown(text) {
  let html = escapeHtml(text);
  // Headers
  html = html.replace(/^### (.*$)/gim, '<h4 style="margin: 10px 0 4px 0; color: #166534; font-weight: 700;">$1</h4>');
  html = html.replace(/^## (.*$)/gim, '<h3 style="margin: 12px 0 6px 0; color: #15803d; font-weight: 800;">$1</h3>');
  // Bold
  html = html.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
  // Italics
  html = html.replace(/\*(.*?)\*/g, "<em>$1</em>");
  // Bullet points
  html = html.replace(/^[•\-] (.*$)/gim, '<li style="margin-left: 20px; list-style-type: disc;">$1</li>');
  // Numbered points
  html = html.replace(/^(\d+)\. (.*$)/gim, '<li style="margin-left: 20px; list-style-type: decimal;">$2</li>');
  // Double Linebreaks
  html = html.replace(/\n\n/g, '<div style="margin-top: 8px;"></div>');
  // Single Linebreaks
  html = html.replace(/\n/g, "<br>");
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

function escapeForAttribute(string) {
  return String(string)
    .replace(/'/g, "\\'")
    .replace(/"/g, "&quot;")
    .replace(/\n/g, " ");
}
