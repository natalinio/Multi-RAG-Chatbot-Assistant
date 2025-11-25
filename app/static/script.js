/**
 * ETL Assistant Frontend JavaScript
 * Handles chat interactions, form submissions, and UI updates
 */

// Global variables for application state
let isLoading = false;
let currentSessionId = 'default';

// DOM elements
let chatWindow, messageInput, chatForm, clearChatBtn, sendButton, charCounter;
let statusIndicator, statusText, welcomeMessage;

/**
 * Initialize the application when DOM is loaded
 */
document.addEventListener('DOMContentLoaded', function() {
    initializeElements();
    setupEventListeners();
    updateCharacterCounter();
    checkApiHealth();
    
    console.log('ETL Assistant frontend initialized');
});

/**
 * Initialize DOM element references
 */
function initializeElements() {
    chatWindow = document.getElementById('chat-window');
    messageInput = document.getElementById('message-input');
    chatForm = document.getElementById('chat-form');
    clearChatBtn = document.getElementById('clear-chat-btn');
    sendButton = document.getElementById('send-button');
    charCounter = document.getElementById('char-counter');
    statusIndicator = document.getElementById('status-indicator');
    statusText = document.getElementById('status-text');
    welcomeMessage = document.getElementById('welcome-message');
}

/**
 * Set up event listeners for user interactions
 */
function setupEventListeners() {
    // Form submission
    chatForm.addEventListener('submit', handleFormSubmit);
    
    // Clear chat button
    clearChatBtn.addEventListener('click', clearChat);
    
    // Character counter for input
    messageInput.addEventListener('input', updateCharacterCounter);
    
    // Quick action buttons
    const quickActionBtns = document.querySelectorAll('.quick-action-btn');
    quickActionBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const message = this.getAttribute('data-message');
            messageInput.value = message;
            messageInput.focus();
        });
    });
    
    // Enter key handling (Shift+Enter for new line, Enter to send)
    messageInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            if (!isLoading && this.value.trim()) {
                chatForm.dispatchEvent(new Event('submit'));
            }
        }
    });
}

/**
 * Handle form submission for chat messages
 * @param {Event} e - Form submit event
 */
async function handleFormSubmit(e) {
    e.preventDefault();
    
    const message = messageInput.value.trim();
    if (!message || isLoading) {
        return;
    }
    
    try {
        // Hide welcome message on first interaction
        if (welcomeMessage && !welcomeMessage.classList.contains('hidden')) {
            welcomeMessage.style.display = 'none';
        }
        
        // Add user message to chat window
        addMessageToChatWindow('user', message);
        
        // Clear input and update UI state
        messageInput.value = '';
        updateCharacterCounter();
        setLoadingState(true);
        
        // Show loading indicator
        const loadingId = addLoadingIndicator();
        
        // Send message to API
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                session_id: currentSessionId
            })
        });
        
        // Remove loading indicator
        removeLoadingIndicator(loadingId);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.success) {
            // Add bot response to chat window
            addMessageToChatWindow('bot', data.response);
        } else {
            // Handle API error
            addMessageToChatWindow('bot', data.response || 'Sorry, I encountered an error processing your request.');
            console.error('API Error:', data.error);
        }
        
    } catch (error) {
        console.error('Error sending message:', error);
        
        // Remove loading indicator if still present
        const loadingElements = document.querySelectorAll('.loading-message');
        loadingElements.forEach(el => el.remove());
        
        // Show error message
        addMessageToChatWindow('bot', 'Sorry, I\'m having trouble connecting to the server. Please check your connection and try again.');
        
        // Update status indicator
        updateConnectionStatus(false);
    } finally {
        setLoadingState(false);
        messageInput.focus();
    }
}

/**
 * Add a message to the chat window
 * @param {string} sender - 'user' or 'bot'
 * @param {string} message - Message content
 */
function addMessageToChatWindow(sender, message) {
    const container = document.createElement('div');
    container.className = `message-container ${sender} message-fade-in`;
    
    const timestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    
    const bubble = document.createElement('div');
    bubble.className = `message-bubble ${sender}`;
    
    if (sender === 'user') {
        bubble.innerHTML = `
            <div class="user-message-content text-sm sm:text-base">${escapeHtml(message)}</div>
            <div class="message-time">${timestamp}</div>
        `;
    } else {
        bubble.innerHTML = `
            <div class="flex items-start gap-2">
                <div class="w-6 h-6 bg-blue-600 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                    <span class="text-white text-xs font-bold">AI</span>
                </div>
                <div class="flex-1 min-w-0">
                    <div class="bot-message-content text-sm sm:text-base">${formatBotMessage(message)}</div>
                    <div class="message-time">${timestamp}</div>
                </div>
            </div>
        `;
    }
    
    container.appendChild(bubble);
    chatWindow.appendChild(container);
    
    // Add event listeners to copy buttons after insertion
    if (sender === 'bot') {
        container.querySelectorAll('.copy-btn').forEach(button => {
            button.addEventListener('click', function() {
                const codeId = this.getAttribute('data-copy-target');
                const codeElement = container.querySelector(`code[data-code="${codeId}"]`);
                if (codeElement) {
                    const textToCopy = codeElement.textContent;
                    copyToClipboard(this, textToCopy);
                }
            });
        });
        
        // Initialize Mermaid diagrams
        if (window.mermaid && container.querySelectorAll('.mermaid').length > 0) {
            console.log('🔍 Found Mermaid elements:', container.querySelectorAll('.mermaid').length);
            setTimeout(() => {
                // Run Mermaid only on new elements in this container
                const mermaidElements = container.querySelectorAll('.mermaid');
                console.log('🎨 Initializing Mermaid for', mermaidElements.length, 'diagrams');
                mermaidElements.forEach((element, index) => {
                    // Give each element a unique ID if it doesn't have one
                    if (!element.id) {
                        element.id = 'mermaid-diagram-' + Date.now() + '-' + index;
                    }
                    console.log('  - Element', index, ':', element.id, 'Content length:', element.textContent.length);
                });
                
                window.mermaid.run({
                    querySelector: '.mermaid',
                    suppressErrors: false
                }).then(() => {
                    console.log('✅ Mermaid rendering completed successfully');
                }).catch(err => {
                    console.error('❌ Mermaid rendering error:', err);
                    // Show error in the diagram container
                    mermaidElements.forEach(el => {
                        if (!el.getAttribute('data-processed')) {
                            el.innerHTML = '<div style="color: #ff6b6b; padding: 20px;">Failed to render diagram. Check console for details.</div>';
                        }
                    });
                });
            }, 100);
        } else {
            if (!window.mermaid) {
                console.warn('⚠️ Mermaid library not loaded');
            }
        }
    }
    
    scrollToBottom();
}

/**
 * Add loading indicator to chat window
 * @returns {string} Loading element ID
 */
function addLoadingIndicator() {
    const loadingId = `loading-${Date.now()}`;
    const container = document.createElement('div');
    container.className = 'message-container bot message-fade-in';
    
    const bubble = document.createElement('div');
    bubble.id = loadingId;
    bubble.className = 'message-bubble bot loading-message';
    bubble.innerHTML = `
        <div class="flex items-center gap-2">
            <div class="w-6 h-6 bg-blue-600 rounded-full flex items-center justify-center flex-shrink-0">
                <span class="text-white text-xs font-bold">AI</span>
            </div>
            <div class="flex items-center gap-1">
                <span class="text-sm">Thinking</span>
                <span class="loading-dots text-sm"></span>
            </div>
        </div>
    `;
    
    container.appendChild(bubble);
    chatWindow.appendChild(container);
    scrollToBottom();
    
    return loadingId;
}

/**
 * Remove loading indicator from chat window
 * @param {string} loadingId - Loading element ID
 */
function removeLoadingIndicator(loadingId) {
    const loadingElement = document.getElementById(loadingId);
    if (loadingElement) {
        loadingElement.remove();
    }
}

/**
 * Clear chat history
 */
async function clearChat() {
    try {
        // Clear chat window
        chatWindow.innerHTML = '';
        
        // Show welcome message again
        if (welcomeMessage) {
            welcomeMessage.style.display = 'block';
        }
        
        // Call API to clear session
        const response = await fetch('/api/clear-session', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(currentSessionId)
        });
        
        if (response.ok) {
            console.log('Chat session cleared successfully');
        } else {
            console.warn('Failed to clear server-side session');
        }
        
    } catch (error) {
        console.error('Error clearing chat:', error);
    }
    
    messageInput.focus();
}

/**
 * Update character counter for message input
 */
function updateCharacterCounter() {
    const currentLength = messageInput.value.length;
    const maxLength = 2000;
    
    charCounter.textContent = `${currentLength}/${maxLength}`;
    
    if (currentLength > maxLength * 0.9) {
        charCounter.className = 'text-xs text-red-500';
    } else if (currentLength > maxLength * 0.8) {
        charCounter.className = 'text-xs text-yellow-500';
    } else {
        charCounter.className = 'text-xs text-gray-500';
    }
}

/**
 * Set loading state for UI elements
 * @param {boolean} loading - Whether loading state is active
 */
function setLoadingState(loading) {
    isLoading = loading;
    
    sendButton.disabled = loading;
    messageInput.disabled = loading;
    
    const sendText = sendButton.querySelector('.send-text');
    const sendLoading = sendButton.querySelector('.send-loading');
    
    if (loading) {
        sendText.classList.add('hidden');
        sendLoading.classList.remove('hidden');
        sendButton.classList.add('cursor-not-allowed');
    } else {
        sendText.classList.remove('hidden');
        sendLoading.classList.add('hidden');
        sendButton.classList.remove('cursor-not-allowed');
    }
}

/**
 * Scroll chat window to bottom
 */
function scrollToBottom() {
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

/**
 * Escape HTML to prevent XSS
 * @param {string} text - Text to escape
 * @returns {string} Escaped text
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Format bot messages with markdown-like formatting and code blocks
 * @param {string} message - Raw bot message
 * @returns {string} Formatted HTML
 */
function formatBotMessage(message) {
    console.log('📝 Formatting bot message, length:', message.length);
    console.log('🔍 Looking for code blocks with regex: /```(\\w*)\\s*([\\s\\S]*?)```/g');
    
    // First, handle ```language\ncode\n``` blocks BEFORE escaping HTML
    // This prevents double-escaping of code content
    const codeBlocks = [];
    let html = message.replace(/```(\w*)\s*([\s\S]*?)```/g, function(match, language, code) {
        const lang = language || 'json';
        const cleanCode = code.trim();
        
        console.log('✅ Found code block:', lang, 'Length:', cleanCode.length);
        
        // Skip empty code blocks
        if (!cleanCode) {
            return '';
        }
        
        // Store code block with placeholder
        const placeholder = `___CODE_BLOCK_${codeBlocks.length}___`;
        codeBlocks.push({ lang, code: cleanCode });
        return placeholder;
    });
    
    // Now escape HTML in the remaining text (not code blocks)
    html = escapeHtml(html);
    
    // Replace placeholders with formatted code blocks
    codeBlocks.forEach((block, index) => {
        const placeholder = `___CODE_BLOCK_${index}___`;
        const { lang, code } = block;
        
        // Special handling for Mermaid diagrams
        if (lang.toLowerCase() === 'mermaid') {
            const blockId = 'mermaid-' + Math.random().toString(36).substr(2, 9);
            console.log('🎨 Detected Mermaid block, creating diagram container:', blockId);
            console.log('📊 Mermaid code length:', code.length);
            const formattedBlock = `<div class="mermaid-block" id="${blockId}">
                <div class="mermaid-header">
                    <span class="mermaid-label">📊 Dependency Graph</span>
                    <div class="mermaid-controls">
                        <button class="mermaid-zoom-btn" onclick="zoomMermaid('${blockId}', -0.2)">−</button>
                        <span class="mermaid-zoom-level" id="${blockId}-zoom">100%</span>
                        <button class="mermaid-zoom-btn" onclick="zoomMermaid('${blockId}', 0.2)">+</button>
                        <button class="copy-btn" onclick="copyMermaidCode('${blockId}')">
                            <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M5.5 4.5V2.5C5.5 1.94772 5.94772 1.5 6.5 1.5H13.5C14.0523 1.5 14.5 1.94772 14.5 2.5V9.5C14.5 10.0523 14.0523 10.5 13.5 10.5H11.5" stroke="currentColor" stroke-linecap="round"/>
                                <rect x="1.5" y="5.5" width="9" height="9" rx="1" stroke="currentColor"/>
                            </svg>
                            <span class="copy-text">Copy</span>
                        </button>
                    </div>
                </div>
                <div class="mermaid-content">
                    <div class="mermaid-wrapper" id="${blockId}-wrapper">
                        <div class="mermaid">${code}</div>
                    </div>
                </div>
            </div>`;
            html = html.replace(placeholder, formattedBlock);
            return;
        }
        
        // Regular code blocks with syntax highlighting
        const blockId = 'code-' + Math.random().toString(36).substr(2, 9);
        
        try {
            // Apply syntax highlighting
            const highlighted = hljs.highlight(code, { language: lang, ignoreIllegals: true }).value;
            
            const formattedBlock = `<div class="code-block" data-code-id="${blockId}">
                <div class="code-header">
                    <span class="code-language">${lang}</span>
                    <button class="copy-btn" data-copy-target="${blockId}">
                        <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M5.5 4.5V2.5C5.5 1.94772 5.94772 1.5 6.5 1.5H13.5C14.0523 1.5 14.5 1.94772 14.5 2.5V9.5C14.5 10.0523 14.0523 10.5 13.5 10.5H11.5" stroke="currentColor" stroke-linecap="round"/>
                            <rect x="1.5" y="5.5" width="9" height="9" rx="1" stroke="currentColor"/>
                        </svg>
                        <span class="copy-text">Copy</span>
                    </button>
                </div>
                <div class="code-content">
                    <pre><code class="hljs language-${lang}" data-code="${blockId}">${highlighted}</code></pre>
                </div>
            </div>`;
            html = html.replace(placeholder, formattedBlock);
        } catch (e) {
            // Fallback if highlighting fails
            console.warn('Syntax highlighting failed for language:', lang, e);
            const escapedCode = escapeHtml(code);
            const formattedBlock = `<div class="code-block" data-code-id="${blockId}">
                <div class="code-header">
                    <span class="code-language">${lang}</span>
                    <button class="copy-btn" data-copy-target="${blockId}">
                        <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M5.5 4.5V2.5C5.5 1.94772 5.94772 1.5 6.5 1.5H13.5C14.0523 1.5 14.5 1.94772 14.5 2.5V9.5C14.5 10.0523 14.0523 10.5 13.5 10.5H11.5" stroke="currentColor" stroke-linecap="round"/>
                            <rect x="1.5" y="5.5" width="9" height="9" rx="1" stroke="currentColor"/>
                        </svg>
                        <span class="copy-text">Copy</span>
                    </button>
                </div>
                <div class="code-content">
                    <pre><code class="hljs" data-code="${blockId}">${escapedCode}</code></pre>
                </div>
            </div>`;
            html = html.replace(placeholder, formattedBlock);
        }
    });
    
    // Convert **bold** to <strong> (but not inside code blocks)
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    // Convert *italic* to <em> (but not inside code blocks)  
    html = html.replace(/(?<!<[^>]*)\*([^*\s][^*]*[^*\s]|\S)\*(?![^<]*>)/g, '<em>$1</em>');
    
    // Convert inline `code` to <code> (but not inside code blocks)
    html = html.replace(/(?<!<[^>]*)`([^`]+)`(?![^<]*>)/g, '<code class="bg-gray-100 text-gray-800 px-1 py-0.5 rounded text-sm font-mono">$1</code>');
    
    // Convert URLs to links
    html = html.replace(
        /(https?:\/\/[^\s<>"]+)/g, 
        '<a href="$1" target="_blank" rel="noopener noreferrer" class="text-blue-600 hover:text-blue-800 underline">$1</a>'
    );
    
    return html;
}

/**
 * Copy code to clipboard
 * @param {HTMLElement} button - Copy button element
 * @param {string} text - Text to copy
 */
function copyToClipboard(button, text) {
    console.log('copyToClipboard called');
    console.log('Text to copy:', text);
    
    const copyText = button.querySelector('.copy-text');
    const originalText = copyText ? copyText.textContent : 'Copy';
    
    // Try modern clipboard API first
    if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(() => {
            console.log('Copy successful!');
            if (copyText) {
                copyText.textContent = 'Copied!';
            }
            button.classList.add('copied');
            
            setTimeout(() => {
                if (copyText) {
                    copyText.textContent = originalText;
                }
                button.classList.remove('copied');
            }, 2000);
        }).catch(err => {
            console.error('Clipboard API failed:', err);
            fallbackCopy(text, button, copyText, originalText);
        });
    } else {
        console.log('Clipboard API not available, using fallback');
        fallbackCopy(text, button, copyText, originalText);
    }
}

/**
 * Fallback copy method for older browsers
 */
function fallbackCopy(text, button, copyText, originalText) {
    try {
        const textArea = document.createElement('textarea');
        textArea.value = text;
        textArea.style.position = 'fixed';
        textArea.style.left = '-999999px';
        textArea.style.top = '-999999px';
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        
        const successful = document.execCommand('copy');
        textArea.remove();
        
        if (successful) {
            console.log('Copy successful (fallback)!');
            if (copyText) {
                copyText.textContent = 'Copied!';
            }
            button.classList.add('copied');
            
            setTimeout(() => {
                if (copyText) {
                    copyText.textContent = originalText;
                }
                button.classList.remove('copied');
            }, 2000);
        } else {
            throw new Error('execCommand failed');
        }
    } catch (fallbackError) {
        console.error('Clipboard fallback failed:', fallbackError);
        if (copyText) {
            copyText.textContent = 'Failed';
            setTimeout(() => {
                copyText.textContent = originalText;
            }, 2000);
        }
    }
}

/**
 * Zoom Mermaid diagram
 * @param {string} blockId - The ID of the mermaid block
 * @param {number} delta - Zoom delta (positive to zoom in, negative to zoom out)
 */
function zoomMermaid(blockId, delta) {
    const wrapper = document.getElementById(`${blockId}-wrapper`);
    const zoomDisplay = document.getElementById(`${blockId}-zoom`);
    
    if (!wrapper || !zoomDisplay) return;
    
    // Get current scale or initialize
    const currentScale = parseFloat(wrapper.dataset.scale || '1');
    
    // Calculate new scale (min 0.5, max 3.0)
    const newScale = Math.min(3.0, Math.max(0.5, currentScale + delta));
    
    // Apply transform
    wrapper.style.transform = `scale(${newScale})`;
    wrapper.dataset.scale = newScale;
    
    // Update display
    zoomDisplay.textContent = `${Math.round(newScale * 100)}%`;
}

/**
 * Check API health and update status indicator
 */
async function checkApiHealth() {
    try {
        const response = await fetch('/api/health');
        const data = await response.json();
        
        updateConnectionStatus(data.status === 'healthy');
        
    } catch (error) {
        console.error('Health check failed:', error);
        updateConnectionStatus(false);
    }
}

/**
 * Update connection status indicator
 * @param {boolean} isHealthy - Whether connection is healthy
 */
function updateConnectionStatus(isHealthy) {
    if (isHealthy) {
        statusIndicator.className = 'w-3 h-3 bg-green-500 rounded-full animate-pulse';
        statusText.textContent = 'Online';
        statusText.className = 'text-sm text-gray-600';
    } else {
        statusIndicator.className = 'w-3 h-3 bg-red-500 rounded-full';
        statusText.textContent = 'Offline';
        statusText.className = 'text-sm text-red-600';
    }
}

/**
 * Copy Mermaid diagram code to clipboard
 * @param {string} blockId - ID of the Mermaid block
 */
function copyMermaidCode(blockId) {
    const block = document.getElementById(blockId);
    if (!block) return;
    
    const codeElement = block.querySelector('[data-mermaid-code]');
    if (!codeElement) return;
    
    const mermaidCode = codeElement.getAttribute('data-mermaid-code');
    const button = block.querySelector('.copy-btn');
    
    copyToClipboard(button, mermaidCode);
}

/**
 * Periodically check API health
 */
setInterval(checkApiHealth, 30000); // Check every 30 seconds

// Export functions for testing (if needed)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        addMessageToChatWindow,
        clearChat,
        formatBotMessage,
        escapeHtml
    };
}