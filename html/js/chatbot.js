/**
 * HispeedCity AI Assistant - Website Floating Chatbot JavaScript Widget
 */

(function () {
  // Configuration
  const API_CHAT_URL = "http://localhost:8001/api/chat";
  const SESSION_ID = "web_session_" + Math.random().toString(36).substring(2, 9);

  // Initialize Widget on DOM load
  document.addEventListener("DOMContentLoaded", initChatbot);

  function initChatbot() {
    createChatElements();
    attachEventListeners();
    addWelcomeMessage();
  }

  function createChatElements() {
    if (document.getElementById("hsc-chat-launcher")) return;

    // Launcher Button
    const launcher = document.createElement("button");
    launcher.id = "hsc-chat-launcher";
    launcher.setAttribute("aria-label", "Open Chatbot");
    launcher.innerHTML = `<i class="bi bi-chat-dots-fill"></i>`;
    document.body.appendChild(launcher);

    // Chat Window Container
    const container = document.createElement("div");
    container.id = "hsc-chat-container";
    container.innerHTML = `
      <div class="hsc-chat-header">
        <div class="hsc-chat-header-info">
          <div class="hsc-chat-avatar"><i class="bi bi-robot"></i></div>
          <div>
            <h4 class="hsc-chat-title">HispeedCity AI</h4>
            <div class="hsc-chat-status"><span class="hsc-status-dot"></span> Online Assistant</div>
          </div>
        </div>
        <button class="hsc-chat-close-btn" id="hsc-close-btn">&times;</button>
      </div>

      <div class="hsc-chat-body" id="hsc-chat-body"></div>

      <div class="hsc-quick-actions">
        <button class="hsc-quick-btn" data-query="Check my parking status">Check Status</button>
        <button class="hsc-quick-btn" data-query="My barrier won't open">Barrier Problem</button>
        <button class="hsc-quick-btn" data-query="How do I register for season parking?">Registration</button>
        <button class="hsc-quick-btn" data-query="How do I renew season parking?">Renewal</button>
      </div>

      <div class="hsc-chat-footer">
        <input type="text" class="hsc-chat-input" id="hsc-chat-input" placeholder="Type a message or plate number..." />
        <button class="hsc-send-btn" id="hsc-send-btn"><i class="bi bi-send-fill"></i></button>
      </div>
    `;
    document.body.appendChild(container);
  }

  function attachEventListeners() {
    const launcher = document.getElementById("hsc-chat-launcher");
    const closeBtn = document.getElementById("hsc-close-btn");
    const container = document.getElementById("hsc-chat-container");
    const sendBtn = document.getElementById("hsc-send-btn");
    const input = document.getElementById("hsc-chat-input");

    launcher.addEventListener("click", () => {
      container.classList.toggle("active");
      if (container.classList.contains("active")) {
        input.focus();
      }
    });

    closeBtn.addEventListener("click", () => {
      container.classList.remove("active");
    });

    sendBtn.addEventListener("click", sendMessage);

    input.addEventListener("keydown", (e) => {
      if (e.key === "Enter") {
        e.preventDefault();
        sendMessage();
      }
    });

    // Quick Actions
    document.querySelectorAll(".hsc-quick-btn").forEach((btn) => {
      btn.addEventListener("click", () => {
        const query = btn.getAttribute("data-query");
        if (query) {
          sendUserQuery(query);
        }
      });
    });
  }

  function addWelcomeMessage() {
    appendBotBubble("Hello! Welcome to HispeedCity AI Support 👋\nHow can I help you with your season parking or barrier access today?");
  }

  function sendMessage() {
    const input = document.getElementById("hsc-chat-input");
    const text = input.value.trim();
    if (!text) return;
    input.value = "";
    sendUserQuery(text);
  }

  function sendUserQuery(userText) {
    appendUserBubble(userText);
    showTypingIndicator();

    fetch(API_CHAT_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: userText, session_id: SESSION_ID }),
    })
      .then((res) => res.json())
      .then((data) => {
        removeTypingIndicator();
        if (data && data.answer) {
          appendBotBubble(data.answer);
        } else {
          appendBotBubble("Sorry, I could not fetch a response right now. Please try again or contact customer support.");
        }
      })
      .catch((err) => {
        removeTypingIndicator();
        console.error("Chatbot API Error:", err);
        appendBotBubble("Connection issue. Please verify the AI Assistant backend server is running.");
      });
  }

  function appendUserBubble(text) {
    const body = document.getElementById("hsc-chat-body");
    const wrap = document.createElement("div");
    wrap.className = "hsc-msg-wrap hsc-msg-user";
    wrap.innerHTML = `<div class="hsc-bubble">${escapeHtml(text)}</div>`;
    body.appendChild(wrap);
    body.scrollTop = body.scrollHeight;
  }

  function appendBotBubble(text) {
    const body = document.getElementById("hsc-chat-body");
    const wrap = document.createElement("div");
    wrap.className = "hsc-msg-wrap hsc-msg-bot";

    // Format URLs into clickable anchor tags
    let formatted = escapeHtml(text).replace(
      /(https?:\/\/[^\s]+)/g,
      '<a href="$1" target="_blank" rel="noopener">$1</a>'
    );

    wrap.innerHTML = `<div class="hsc-bubble">${formatted}</div>`;
    body.appendChild(wrap);
    body.scrollTop = body.scrollHeight;
  }

  function showTypingIndicator() {
    const body = document.getElementById("hsc-chat-body");
    const wrap = document.createElement("div");
    wrap.id = "hsc-typing";
    wrap.className = "hsc-msg-wrap hsc-msg-bot";
    wrap.innerHTML = `<div class="hsc-bubble" style="font-style:italic; color:#6B7280;">Thinking...</div>`;
    body.appendChild(wrap);
    body.scrollTop = body.scrollHeight;
  }

  function removeTypingIndicator() {
    const typing = document.getElementById("hsc-typing");
    if (typing) typing.remove();
  }

  function escapeHtml(str) {
    return str
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }
})();
