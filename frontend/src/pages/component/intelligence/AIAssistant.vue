<template>
  <q-page class="ai-page">
    <div class="ai-shell">

      <!-- Header -->
      <div class="ai-header">
        <div class="ai-title-area">
          <div class="ai-title-icon">
            <q-icon
              name="auto_awesome"
              size="25px"
            />
          </div>

          <div>
            <div class="ai-title">
              SOMI AI Assistant
            </div>

            <div class="ai-subtitle">
              Your intelligent assistant for SOMI office data
            </div>
          </div>
        </div>

        <div class="ai-header-actions">
          <div class="ai-status">
            <span class="status-dot"></span>

            <div>
              <div class="status-title">
                AI Online
              </div>

              <div class="status-subtitle">
                Local Llama · Ollama
              </div>
            </div>
          </div>

          <q-btn
            flat
            round
            dense
            icon="delete_sweep"
            class="clear-btn"
            :disable="loading || messages.length === 0"
            @click="clearChat"
          >
            <q-tooltip>
              Clear conversation
            </q-tooltip>
          </q-btn>
        </div>
      </div>

      <!-- Main Chat Card -->
      <q-card
        flat
        bordered
        class="chat-card"
      >

        <!-- Chat Header -->
        <div class="chat-card-header">
          <div class="assistant-profile">
            <div class="assistant-avatar">
              <q-icon
                name="auto_awesome"
                size="18px"
              />
            </div>

            <div>
              <div class="assistant-name">
                SOMI AI Assistant
              </div>

              <div class="assistant-caption">
                Answers are based on available SOMI intelligence data.
              </div>
            </div>
          </div>

          <div class="data-badge">
            <q-icon
              name="database"
              size="14px"
            />
            SOMI Data
          </div>
        </div>

        <div class="chat-divider"></div>

        <!-- Messages -->
        <div
          ref="messagesContainer"
          class="messages-container"
        >

          <!-- Welcome -->
          <div
            v-if="messages.length === 0"
            class="welcome-state"
          >
            <div class="welcome-icon">
              <q-icon
                name="auto_awesome"
                size="34px"
              />
            </div>

            <div class="welcome-title">
              How can I help you today?
            </div>

            <div class="welcome-description">
              Ask SOMI about attendance, leave, payroll,
              tasks, performance or overall office intelligence.
            </div>

            <div class="suggestions">
              <button
                v-for="suggestion in suggestions"
                :key="suggestion.label"
                class="suggestion-card"
                :disabled="loading"
                @click="askSuggestion(suggestion.question)"
              >
                <div class="suggestion-icon">
                  <q-icon
                    :name="suggestion.icon"
                    size="18px"
                  />
                </div>

                <div class="suggestion-content">
                  <div class="suggestion-title">
                    {{ suggestion.label }}
                  </div>

                  <div class="suggestion-question">
                    {{ suggestion.question }}
                  </div>
                </div>

                <q-icon
                  name="arrow_forward"
                  size="16px"
                  class="suggestion-arrow"
                />
              </button>
            </div>
          </div>

          <!-- Conversation -->
          <div
            v-for="(message, index) in messages"
            :key="message.id || index"
            :class="[
              'message-row',
              message.role === 'user'
                ? 'user-row'
                : 'assistant-row'
            ]"
          >

            <!-- Assistant Avatar -->
            <div
              v-if="message.role === 'assistant'"
              class="message-avatar assistant-message-avatar"
            >
              <q-icon
                name="auto_awesome"
                size="17px"
              />
            </div>

            <div class="message-content">

              <div
                v-if="message.role === 'assistant'"
                class="message-meta assistant-meta"
              >
                <span>SOMI AI</span>

                <span class="ai-label">
                  AI Assistant
                </span>
              </div>

              <div
                v-if="message.role === 'user'"
                class="message-meta user-meta"
              >
                <span>You</span>
              </div>

              <div
                :class="[
                  'message-bubble',
                  message.role === 'user'
                    ? 'user-bubble'
                    : 'assistant-bubble'
                ]"
              >
                <div class="message-text">
                  {{ message.content }}

                  <span
                    v-if="
                      streaming &&
                      message.role === 'assistant' &&
                      index === messages.length - 1
                    "
                    class="streaming-cursor"
                  >
                    ▌
                  </span>
                </div>
              </div>
            </div>

            <!-- User Avatar -->
            <div
              v-if="message.role === 'user'"
              class="message-avatar user-message-avatar"
            >
              <q-icon
                name="person"
                size="17px"
              />
            </div>
          </div>

          <!-- Thinking -->
          <div
            v-if="loading && !streaming"
            class="thinking-row"
          >
            <div class="message-avatar assistant-message-avatar">
              <q-icon
                name="auto_awesome"
                size="17px"
              />
            </div>

            <div class="thinking-content">
              <div class="message-meta assistant-meta">
                <span>SOMI AI</span>

                <span class="ai-label">
                  AI Assistant
                </span>
              </div>

              <div class="thinking-bubble">
                <div class="thinking-dots">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>

                <span>
                  SOMI AI is analyzing your data...
                </span>
              </div>
            </div>
          </div>

          <!-- Error -->
          <div
            v-if="errorMessage"
            class="error-box"
          >
            <div class="error-icon">
              <q-icon
                name="error_outline"
                size="19px"
              />
            </div>

            <div class="error-content">
              <div class="error-title">
                SOMI AI could not complete the request
              </div>

              <div class="error-text">
                {{ errorMessage }}
              </div>

              <q-btn
                flat
                dense
                no-caps
                icon="refresh"
                label="Try again"
                class="retry-btn"
                :disable="loading"
                @click="retryLastMessage"
              />
            </div>
          </div>
        </div>

        <!-- Composer -->
        <div class="composer-area">

          <div class="composer-box">
            <q-input
              v-model="inputMessage"
              borderless
              autogrow
              dense
              type="textarea"
              class="composer-input"
              placeholder="Ask SOMI anything about your office data..."
              :disable="loading"
              @keydown.enter.exact.prevent="sendMessage"
              @keydown.enter.shift.stop
            />

            <q-btn
              round
              unelevated
              icon="arrow_upward"
              class="send-btn"
              :disable="!canSend"
              @click="sendMessage"
            >
              <q-tooltip>
                Send message
              </q-tooltip>
            </q-btn>
          </div>

          <div class="composer-footer">
            <div class="composer-hint">
              <q-icon
                name="info_outline"
                size="14px"
              />

              SOMI AI uses controlled office intelligence data.
            </div>

            <div class="model-info">
              <span class="model-dot"></span>
              llama3.2:3b · Local AI
            </div>
          </div>
        </div>
      </q-card>

      <!-- Information Cards -->
      <div class="info-grid">

        <div class="info-card">
          <div class="info-icon blue-icon">
            <q-icon
              name="security"
              size="19px"
            />
          </div>

          <div>
            <div class="info-title">
              Controlled Data
            </div>

            <div class="info-text">
              AI receives relevant SOMI intelligence data instead
              of unrestricted database access.
            </div>
          </div>
        </div>

        <div class="info-card">
          <div class="info-icon purple-icon">
            <q-icon
              name="psychology"
              size="19px"
            />
          </div>

          <div>
            <div class="info-title">
              Smart Analysis
            </div>

            <div class="info-text">
              SOMI combines structured business data with
              natural-language AI reasoning.
            </div>
          </div>
        </div>

        <div class="info-card">
          <div class="info-icon green-icon">
            <q-icon
              name="bolt"
              size="19px"
            />
          </div>

          <div>
            <div class="info-title">
              Local AI
            </div>

            <div class="info-text">
              Current responses are generated locally using
              Ollama and llama3.2:3b.
            </div>
          </div>
        </div>

      </div>
    </div>
  </q-page>
</template>

<script>
import api from 'src/services/api'
import AuthenticationService from 'src/pages/authentication/AuthenticationService'

export default {
  name: 'AIAssistant',

  data () {
    return {
      inputMessage: '',
      loading: false,
      streaming: false,
      errorMessage: '',
      lastQuestion: '',
      messages: [],

      suggestions: [
        {
          label: 'Attendance',
          icon: 'schedule',
          question: 'How is attendance this month? Give me a short summary.'
        },
        {
          label: 'Leave',
          icon: 'event_available',
          question: 'Give me a summary of leave activity this month.'
        },
        {
          label: 'Tasks',
          icon: 'task_alt',
          question: 'Give me a summary of task completion and pending work.'
        },
        {
          label: 'Performance',
          icon: 'insights',
          question: 'Give me a performance summary.'
        },
        {
          label: 'Payroll',
          icon: 'payments',
          question: 'Give me just the payroll report for this month.'
        },
        {
          label: 'Office',
          icon: 'business',
          question: 'Give me a short overall summary of the office.'
        }
      ]
    }
  },

  computed: {
    canSend () {
      return (
        this.inputMessage.trim().length > 0 &&
        !this.loading
      )
    }
  },

  methods: {
    async sendMessage () {
      const message = this.inputMessage.trim()

      if (!message || this.loading) {
        return
      }

      this.lastQuestion = message
      this.errorMessage = ''

      this.messages.push({
        id: `${Date.now()}-user`,
        role: 'user',
        content: message
      })

      this.inputMessage = ''

      await this.scrollToBottom()

      this.loading = true
      this.streaming = false

      try {
        await this.streamMessage(message)
      } catch (error) {
        console.error(
          'SOMI AI Assistant error:',
          error
        )

        this.errorMessage =
          this.getErrorMessage(error)
      } finally {
        this.loading = false
        this.streaming = false

        await this.scrollToBottom()
      }
    },

    async streamMessage (message, retryAfterRefresh = true) {
      const baseURL = (
        api.defaults.baseURL ||
        'http://127.0.0.1:8000/api'
      ).replace(/\/$/, '')

      const token = AuthenticationService.getToken()

      const response = await fetch(
        `${baseURL}/intelligence/assistant/`,
        {
          method: 'POST',

          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json',
            Accept: '*/*'
          },

          body: JSON.stringify({
            message,
            stream: true
          })
        } 
      )

      /*
       * Fetch does not use Axios interceptors.
       * Therefore, handle an expired access token here.
       */
      if (response.status === 401 && retryAfterRefresh) {
        try {
          await AuthenticationService.refreshToken()

          return await this.streamMessage(
            message,
            false
          )
        } catch (refreshError) {
          const authError = new Error(
            'Your session has expired. Please log in again.'
          )

          authError.status = 401

          throw authError
        }
      }

      if (!response.ok) {
        await this.throwStreamingError(response)
      }

      /*
       * Some environments may return a normal JSON response.
       * Handle that gracefully as a fallback.
       */
      const contentType =
        response.headers.get('content-type') || ''

      if (
        contentType.includes('application/json') &&
        !contentType.includes('application/x-ndjson')
      ) {
        const data = await response.json()

        this.messages.push({
          id: `${Date.now()}-assistant`,
          role: 'assistant',
          content:
            data.answer ||
            'SOMI AI did not return an answer.'
        })

        return
      }

      if (!response.body) {
        throw new Error(
          'The browser did not provide a streaming response.'
        )
      }

      /*
       * Create the assistant message immediately after
       * receiving successful response headers.
       *
       * The content starts empty and is filled chunk-by-chunk.
       */
      const assistantMessage = {
        id: `${Date.now()}-assistant`,
        role: 'assistant',
        content: ''
      }

      this.messages.push(assistantMessage)

      const assistantIndex =
        this.messages.length - 1

      this.streaming = true

      const reader =
        response.body.getReader()

      const decoder =
        new TextDecoder('utf-8')

      let buffer = ''

      while (true) {
        const {
          value,
          done
        } = await reader.read()

        if (done) {
          break
        }

        buffer += decoder.decode(
          value,
          {
            stream: true
          }
        )

        const lines =
          buffer.split('\n')

        buffer =
          lines.pop() || ''

        for (const line of lines) {
          await this.processStreamLine(
            line,
            assistantIndex
          )
        }

        await this.scrollToBottom()
      }

      /*
       * Flush remaining UTF-8 bytes.
       */
      buffer += decoder.decode()

      if (buffer.trim()) {
        await this.processStreamLine(
          buffer,
          assistantIndex
        )
      }

      /*
       * If Ollama/backend returned no tokens,
       * don't leave an empty assistant bubble.
       */
      if (
        !this.messages[assistantIndex] ||
        !this.messages[assistantIndex].content.trim()
      ) {
        this.messages[assistantIndex].content =
          'SOMI AI did not return an answer.'
      }

      this.streaming = false
    },

    async processStreamLine (
      line,
      assistantIndex
    ) {
      const trimmedLine =
        line.trim()

      if (!trimmedLine) {
        return
      }

      let chunk

      try {
        chunk = JSON.parse(trimmedLine)
      } catch (error) {
        console.warn(
          'SOMI AI returned an invalid stream chunk:',
          trimmedLine
        )

        return
      }

      if (chunk.type === 'token') {
        if (!this.messages[assistantIndex]) {
          return
        }

        this.messages[assistantIndex].content +=
          chunk.content || ''

        return
      }

      if (chunk.type === 'done') {
        this.streaming = false

        return
      }

      if (chunk.type === 'error') {
        const streamError =
          new Error(
            chunk.detail ||
            'SOMI AI stream failed.'
          )

        streamError.status =
          chunk.status || 500

        throw streamError
      }

      /*
       * Compatibility:
       * If backend ever sends a direct answer field,
       * accept it as an assistant response.
       */
      if (chunk.answer) {
        if (!this.messages[assistantIndex]) {
          return
        }

        this.messages[assistantIndex].content +=
          chunk.answer
      }
    },

    async throwStreamingError (response) {
      let detail =
        'SOMI AI could not process the request right now.'

      try {
        const contentType =
          response.headers.get('content-type') || ''

        if (contentType.includes('application/json')) {
          const data =
            await response.json()

          detail =
            data.detail ||
            detail
        } else {
          const text =
            await response.text()

          if (text.trim()) {
            detail = text
          }
        }
      } catch (error) {
        /*
         * Keep the default error message.
         */
      }

      const error =
        new Error(detail)

      error.status =
        response.status

      throw error
    },

    async askSuggestion (suggestion) {
      if (this.loading) {
        return
      }

      this.inputMessage = suggestion

      await this.sendMessage()
    },

    async retryLastMessage () {
      if (
        !this.lastQuestion ||
        this.loading
      ) {
        return
      }

      this.errorMessage = ''
      this.inputMessage =
        this.lastQuestion

      await this.sendMessage()
    },

    clearChat () {
      if (this.loading) {
        return
      }

      this.messages = []
      this.inputMessage = ''
      this.errorMessage = ''
      this.lastQuestion = ''
      this.streaming = false
    },

    getErrorMessage (error) {
      const status =
        error.status ||
        error.response?.status

      if (status === 401) {
        return (
          'Your session has expired. Please log in again.'
        )
      }

      if (status === 503) {
        return (
          error.response?.data?.detail ||
          error.message ||
          'SOMI AI is currently unavailable. Please make sure Ollama is running.'
        )
      }

      if (status >= 500) {
        return (
          error.message ||
          'SOMI AI could not process the request right now.'
        )
      }

      return (
        error.response?.data?.detail ||
        error.message ||
        'Unable to connect to SOMI AI. Please try again.'
      )
    },

    async scrollToBottom () {
      await this.$nextTick()

      const container =
        this.$refs.messagesContainer

      if (!container) {
        return
      }

      container.scrollTop =
        container.scrollHeight
    }
  }
}
</script>

<style scoped>
.ai-page {
  min-height: 100vh;
  padding: 20px;
  background: #f5f7fb;
}

.ai-shell {
  width: 100%;
  max-width: 1450px;
  margin: 0 auto;
}

.ai-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 18px;
}

.ai-title-area {
  display: flex;
  align-items: center;
  gap: 13px;
}

.ai-title-icon {
  width: 48px;
  height: 48px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #eaf1ff;
  color: #285dcc;
}

.ai-title {
  color: #17233c;
  font-size: 24px;
  font-weight: 750;
  line-height: 1.15;
}

.ai-subtitle {
  margin-top: 4px;
  color: #7b879a;
  font-size: 12px;
}

.ai-header-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.ai-status {
  display: flex;
  align-items: center;
  gap: 9px;
  min-width: 145px;
  padding: 9px 13px;
  border: 1px solid #e3e8f1;
  border-radius: 11px;
  background: #ffffff;
}

.status-dot {
  width: 8px;
  height: 8px;
  flex-shrink: 0;
  border-radius: 50%;
  background: #20a36a;
  box-shadow: 0 0 0 4px #e8f8f0;
}

.status-title {
  color: #26334a;
  font-size: 11px;
  font-weight: 700;
}

.status-subtitle {
  margin-top: 2px;
  color: #8a95a7;
  font-size: 9px;
}

.clear-btn {
  color: #7c8799;
}

.chat-card {
  overflow: hidden;
  border-color: #e1e7f0;
  border-radius: 18px;
  background: #ffffff;
  box-shadow: 0 10px 35px rgba(31, 48, 80, 0.06);
}

.chat-card-header {
  min-height: 68px;
  padding: 14px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 15px;
}

.assistant-profile {
  display: flex;
  align-items: center;
  gap: 10px;
}

.assistant-avatar {
  width: 32px;
  height: 32px;
  border-radius: 9px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #edf3ff;
  color: #2b60d0;
}

.assistant-name {
  color: #26344d;
  font-size: 12px;
  font-weight: 750;
}

.assistant-caption {
  margin-top: 2px;
  color: #8a96a8;
  font-size: 9px;
}

.data-badge {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 5px 8px;
  border-radius: 7px;
  background: #f3f6fb;
  color: #718096;
  font-size: 9px;
  font-weight: 650;
}

.chat-divider {
  height: 1px;
  margin: 0 20px;
  background: #e8edf4;
}

.messages-container {
  height: min(62vh, 650px);
  min-height: 420px;
  overflow-y: auto;
  padding: 22px 24px;
  scroll-behavior: smooth;
}

.messages-container::-webkit-scrollbar {
  width: 7px;
}

.messages-container::-webkit-scrollbar-track {
  background: transparent;
}

.messages-container::-webkit-scrollbar-thumb {
  border-radius: 10px;
  background: #cbd3df;
}

.welcome-state {
  max-width: 760px;
  margin: 35px auto 20px;
  text-align: center;
}

.welcome-icon {
  width: 66px;
  height: 66px;
  margin: 0 auto 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 19px;
  background: #edf3ff;
  color: #285fd0;
}

.welcome-title {
  color: #24324a;
  font-size: 20px;
  font-weight: 750;
}

.welcome-description {
  max-width: 580px;
  margin: 8px auto 25px;
  color: #7e899b;
  font-size: 12px;
  line-height: 1.7;
}

.suggestions {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
  text-align: left;
}

.suggestion-card {
  min-height: 72px;
  display: flex;
  align-items: center;
  gap: 11px;
  padding: 12px;
  border: 1px solid #e3e8f1;
  border-radius: 12px;
  background: #ffffff;
  cursor: pointer;
  text-align: left;
  transition: 0.18s ease;
}

.suggestion-card:hover:not(:disabled) {
  border-color: #b9caf0;
  background: #f8faff;
  transform: translateY(-1px);
}

.suggestion-card:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

.suggestion-icon {
  width: 35px;
  height: 35px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  background: #edf3ff;
  color: #3264cf;
}

.suggestion-content {
  flex: 1;
  min-width: 0;
}

.suggestion-title {
  color: #2d3a50;
  font-size: 11px;
  font-weight: 750;
}

.suggestion-question {
  margin-top: 3px;
  overflow: hidden;
  color: #8792a4;
  font-size: 9px;
  line-height: 1.45;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.suggestion-arrow {
  color: #9ba6b6;
}

.message-row {
  display: flex;
  align-items: flex-start;
  gap: 9px;
  margin-bottom: 25px;
}

.assistant-row {
  justify-content: flex-start;
}

.user-row {
  justify-content: flex-end;
}

.message-content {
  max-width: min(78%, 900px);
}

.message-avatar {
  width: 33px;
  height: 33px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
}

.assistant-message-avatar {
  background: #edf3ff;
  color: #285fd0;
}

.user-message-avatar {
  background: #edf1f7;
  color: #607089;
}

.message-meta {
  display: flex;
  align-items: center;
  gap: 6px;
  height: 18px;
  margin-bottom: 5px;
  font-size: 9px;
  font-weight: 700;
}

.assistant-meta {
  color: #5d6c82;
}

.user-meta {
  justify-content: flex-end;
  color: #66758c;
}

.ai-label {
  padding: 2px 5px;
  border-radius: 4px;
  background: #eef3ff;
  color: #4771cf;
  font-size: 7px;
  font-weight: 700;
}

.message-bubble {
  padding: 11px 14px;
  border-radius: 11px;
  font-size: 12px;
  line-height: 1.65;
  white-space: pre-wrap;
  word-break: break-word;
}

.assistant-bubble {
  border: 1px solid #dfe6ef;
  background: #f9fbfd;
  color: #273650;
  border-top-left-radius: 4px;
}

.user-bubble {
  background: #3564cf;
  color: #ffffff;
  border-top-right-radius: 4px;
}

.streaming-cursor {
  display: inline-block;
  margin-left: 2px;
  color: #3264cf;
  animation: cursorBlink 0.8s infinite;
}

@keyframes cursorBlink {
  0%,
  45% {
    opacity: 1;
  }

  46%,
  100% {
    opacity: 0;
  }
}

.thinking-row {
  display: flex;
  align-items: flex-start;
  gap: 9px;
  margin-bottom: 25px;
}

.thinking-content {
  max-width: 500px;
}

.thinking-bubble {
  display: flex;
  align-items: center;
  gap: 9px;
  padding: 10px 13px;
  border: 1px solid #e1e7ef;
  border-radius: 10px;
  border-top-left-radius: 4px;
  background: #f9fbfd;
  color: #8792a4;
  font-size: 10px;
}

.thinking-dots {
  display: flex;
  align-items: center;
  gap: 3px;
}

.thinking-dots span {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: #5c79bd;
  animation: thinking 1.2s infinite;
}

.thinking-dots span:nth-child(2) {
  animation-delay: 0.15s;
}

.thinking-dots span:nth-child(3) {
  animation-delay: 0.3s;
}

@keyframes thinking {
  0%,
  60%,
  100% {
    opacity: 0.3;
    transform: translateY(0);
  }

  30% {
    opacity: 1;
    transform: translateY(-2px);
  }
}

.error-box {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  max-width: 650px;
  margin: 5px auto 20px;
  padding: 12px 14px;
  border: 1px solid #f0d2d2;
  border-radius: 10px;
  background: #fff8f8;
}

.error-icon {
  width: 30px;
  height: 30px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  background: #ffeaea;
  color: #c55454;
}

.error-title {
  color: #9c3d3d;
  font-size: 10px;
  font-weight: 750;
}

.error-text {
  margin-top: 3px;
  color: #9d6d6d;
  font-size: 9px;
  line-height: 1.5;
}

.retry-btn {
  margin-top: 5px;
  padding: 0;
  color: #315fc4;
  font-size: 9px;
}

.composer-area {
  padding: 15px 20px 13px;
  border-top: 1px solid #e8edf4;
  background: #ffffff;
}

.composer-box {
  display: flex;
  align-items: flex-end;
  gap: 10px;
  min-height: 49px;
  padding: 5px 6px 5px 13px;
  border: 1px solid #dce3ed;
  border-radius: 13px;
  background: #fafbfd;
  transition: 0.18s ease;
}

.composer-box:focus-within {
  border-color: #9bb4e8;
  background: #ffffff;
  box-shadow: 0 0 0 3px rgba(50, 100, 207, 0.06);
}

.composer-input {
  flex: 1;
  min-width: 0;
  color: #26354d;
  font-size: 12px;
}

.composer-input :deep(.q-field__control) {
  min-height: 38px;
}

.composer-input :deep(textarea) {
  max-height: 120px;
  line-height: 1.5;
}

.send-btn {
  width: 35px;
  height: 35px;
  flex-shrink: 0;
  background: #3263ce;
  color: #ffffff;
}

.send-btn:disabled {
  background: #dfe5ef !important;
  color: #96a1b2 !important;
}

.composer-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  margin-top: 8px;
}

.composer-hint {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #9aa4b3;
  font-size: 8px;
}

.model-info {
  display: flex;
  align-items: center;
  gap: 5px;
  color: #8c98a9;
  font-size: 8px;
}

.model-dot {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: #22a36a;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
  margin-top: 13px;
}

.info-card {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 13px;
  border: 1px solid #e1e7f0;
  border-radius: 12px;
  background: #ffffff;
}

.info-icon {
  width: 34px;
  height: 34px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 9px;
}

.blue-icon {
  background: #edf3ff;
  color: #3264cf;
}

.purple-icon {
  background: #f2edff;
  color: #7353c7;
}

.green-icon {
  background: #eaf8f1;
  color: #29966a;
}

.info-title {
  color: #344158;
  font-size: 10px;
  font-weight: 750;
}

.info-text {
  margin-top: 3px;
  color: #8994a5;
  font-size: 8px;
  line-height: 1.5;
}

/* Dark mode */
.body--dark .ai-page {
  background: #111827;
}

.body--dark .chat-card,
.body--dark .ai-status,
.body--dark .composer-area,
.body--dark .info-card,
.body--dark .suggestion-card {
  background: #182131;
  border-color: #293548;
}

.body--dark .ai-title,
.body--dark .assistant-name,
.body--dark .welcome-title,
.body--dark .info-title,
.body--dark .suggestion-title,
.body--dark .message-text {
  color: #e5ebf5;
}

.body--dark .ai-subtitle,
.body--dark .assistant-caption,
.body--dark .welcome-description,
.body--dark .suggestion-question,
.body--dark .info-text,
.body--dark .composer-hint,
.body--dark .model-info {
  color: #8e9aae;
}

.body--dark .chat-divider,
.body--dark .composer-area {
  border-color: #293548;
}

.body--dark .assistant-bubble,
.body--dark .thinking-bubble,
.body--dark .composer-box {
  background: #202b3d;
  border-color: #334157;
}

.body--dark .assistant-bubble,
.body--dark .thinking-bubble {
  color: #dce4ef;
}

.body--dark .data-badge {
  background: #202b3d;
  color: #98a6bb;
}

.body--dark .ai-title-icon,
.body--dark .assistant-avatar,
.body--dark .welcome-icon,
.body--dark .suggestion-icon,
.body--dark .assistant-message-avatar,
.body--dark .blue-icon {
  background: #202f4d;
}

.body--dark .user-message-avatar {
  background: #273246;
  color: #a9b5c7;
}

.body--dark .user-bubble {
  background: #315ec1;
  color: #ffffff;
}

.body--dark .suggestion-card:hover:not(:disabled) {
  background: #202b3d;
  border-color: #405275;
}

.body--dark .error-box {
  background: #2a1d21;
  border-color: #4d3036;
}

.body--dark .error-title {
  color: #e48c8c;
}

.body--dark .error-text {
  color: #c18c8c;
}

.body--dark .purple-icon {
  background: #2d2543;
}

.body--dark .green-icon {
  background: #1d352c;
}

/* Responsive */
@media (max-width: 900px) {
  .ai-page {
    padding: 14px;
  }

  .messages-container {
    height: 58vh;
    min-height: 400px;
  }

  .message-content {
    max-width: 86%;
  }

  .info-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 650px) {
  .ai-page {
    padding: 8px;
  }

  .ai-header {
    align-items: flex-start;
  }

  .ai-title {
    font-size: 19px;
  }

  .ai-subtitle {
    font-size: 10px;
  }

  .ai-status {
    min-width: auto;
    padding: 7px;
  }

  .ai-status > div {
    display: none;
  }

  .chat-card-header {
    padding: 12px;
  }

  .chat-divider {
    margin: 0 12px;
  }

  .messages-container {
    min-height: 400px;
    height: 57vh;
    padding: 16px 12px;
  }

  .suggestions {
    grid-template-columns: 1fr;
  }

  .message-content {
    max-width: calc(100% - 42px);
  }

  .composer-area {
    padding: 11px 12px;
  }

  .composer-footer {
    align-items: flex-start;
    flex-direction: column;
  }

  .data-badge {
    display: none;
  }

  .welcome-state {
    margin-top: 25px;
  }
}
</style>
