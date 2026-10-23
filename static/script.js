/* Frontend logic for the NLP Chatbot */
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("chat-form");
  const input = document.getElementById("user-input");
  const messagesContainer = document.getElementById("messages-container");
  const typingIndicator = document.getElementById("typing-indicator");
  const clearBtn = document.getElementById("clear-btn");
  const suggestionsContainer = document.getElementById("suggestions-container");

  let isProcessing = false;

  // Auto-scroll messages container to bottom
  function scrollToBottom() {
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }

  // Create message element safely
  function createMessageElement(text, role, metadata = null) {
    const article = document.createElement("article");
    article.className = `message ${role}-message animate-in`;

    const avatar = document.createElement("div");
    avatar.className = "msg-avatar";

    if (role === "bot") {
      avatar.innerHTML = `
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <rect x="3" y="11" width="18" height="10" rx="2"></rect>
          <circle cx="12" cy="5" r="2"></circle>
          <path d="M12 7v4"></path>
        </svg>`;
    } else {
      avatar.innerHTML = `
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
          <circle cx="12" cy="7" r="4"></circle>
        </svg>`;
    }

    const contentDiv = document.createElement("div");
    contentDiv.className = "msg-content";

    const bubble = document.createElement("div");
    bubble.className = "bubble";
    bubble.textContent = text;
    contentDiv.appendChild(bubble);

    // If bot returned NLP metadata, render badges
    if (role === "bot" && metadata) {
      const metaTag = document.createElement("div");
      metaTag.className = "meta-tag";

      if (metadata.intent) {
        const intentBadge = document.createElement("span");
        intentBadge.className = "badge intent-badge";
        intentBadge.textContent = `Intent: ${metadata.intent}`;
        metaTag.appendChild(intentBadge);
      }

      if (metadata.confidence !== undefined) {
        const confPercent = Math.round(metadata.confidence * 100);
        const confBadge = document.createElement("span");
        confBadge.className = "badge confidence-badge";
        confBadge.textContent = `Confidence: ${confPercent}%`;
        metaTag.appendChild(confBadge);
      }

      if (metadata.tokens && metadata.tokens.length > 0) {
        const tokenBadge = document.createElement("span");
        tokenBadge.className = "badge tokens-badge";
        tokenBadge.title = "Preprocessed tokens analyzed by TF-IDF";
        tokenBadge.textContent = `Tokens: [${metadata.tokens.slice(0, 4).join(", ")}${metadata.tokens.length > 4 ? "..." : ""}]`;
        metaTag.appendChild(tokenBadge);
      }

      contentDiv.appendChild(metaTag);
    }

    article.appendChild(avatar);
    article.appendChild(contentDiv);
    return article;
  }

  // Handle sending a message
  async function sendMessage(text) {
    const trimmed = text.trim();
    if (!trimmed || isProcessing) return;

    isProcessing = true;
    input.value = "";
    input.focus();

    // Render user message
    const userMsg = createMessageElement(trimmed, "user");
    messagesContainer.appendChild(userMsg);
    scrollToBottom();

    // Show typing indicator
    typingIndicator.classList.remove("hidden");
    scrollToBottom();

    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: trimmed }),
      });

      const data = await response.json();
      typingIndicator.classList.add("hidden");

      if (response.ok) {
        const botMsg = createMessageElement(data.response, "bot", {
          intent: data.intent,
          confidence: data.confidence,
          tokens: data.tokens,
        });
        messagesContainer.appendChild(botMsg);
      } else {
        const errorMsg = createMessageElement(
          data.response || data.error || "An error occurred while processing your request.",
          "bot",
          { intent: "error", confidence: 0 }
        );
        messagesContainer.appendChild(errorMsg);
      }
    } catch (err) {
      typingIndicator.classList.add("hidden");
      const networkMsg = createMessageElement(
        "Unable to reach the chatbot server. Please verify that the Flask server is running.",
        "bot",
        { intent: "network_error", confidence: 0 }
      );
      messagesContainer.appendChild(networkMsg);
    } finally {
      isProcessing = false;
      scrollToBottom();
    }
  }

  // Event listener for form submission
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    sendMessage(input.value);
  });

  // Suggestion chips click handler
  if (suggestionsContainer) {
    suggestionsContainer.addEventListener("click", (e) => {
      const chip = e.target.closest(".chip");
      if (chip && chip.dataset.query) {
        sendMessage(chip.dataset.query);
      }
    });
  }

  // Clear conversation handler
  if (clearBtn) {
    clearBtn.addEventListener("click", () => {
      messagesContainer.innerHTML = "";
      const welcome = createMessageElement(
        "Conversation reset. Ask me anything about Natural Language Processing (Tokenization, TF-IDF, Stop Words, etc.)!",
        "bot",
        { intent: "reset", confidence: 1.0 }
      );
      messagesContainer.appendChild(welcome);
      scrollToBottom();
    });
  }
});
