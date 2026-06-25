import { useState, useRef, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'
import { sendMessage } from '../api/client'
import styles from './ChatPage.module.css'

const QUICK_PROMPTS = [
  { label: '📋 Show menu', message: 'What is on your menu?' },
  { label: '☕ Order cappuccino', message: 'I want 2 cappuccinos' },
  { label: '📦 Last order', message: 'What was my last order?' },
  { label: 'ℹ️ Shop info', message: 'Tell me about your shop' },
]

function Message({ msg }) {
  const isUser = msg.role === 'user'
  return (
    <div className={`${styles.msgRow} ${isUser ? styles.userRow : styles.botRow}`}>
      {!isUser && <span className={styles.avatar}>☕</span>}
      <div className={`${styles.bubble} ${isUser ? styles.userBubble : styles.botBubble}`}>
        {msg.loading ? (
          <span className={styles.typing}>
            <span>·</span><span>·</span><span>·</span>
          </span>
        ) : (
          <p className={styles.msgText}>{msg.text}</p>
        )}
        {msg.timestamp && (
          <span className={styles.timestamp}>
            {new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </span>
        )}
      </div>
      {isUser && <span className={styles.userAvatar}>👤</span>}
    </div>
  )
}

export default function ChatPage() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const [messages, setMessages] = useState([
    {
      id: 'welcome',
      role: 'bot',
      text: `Hey ${user?.name?.split(' ')[0] || 'there'}! ☕ Welcome to BeanBrew. I'm your AI barista — ask me about our menu, place an order, or check your order status. What can I brew for you today?`,
      timestamp: new Date().toISOString(),
    }
  ])
  const [input, setInput] = useState('')
  const [sending, setSending] = useState(false)
  const bottomRef = useRef(null)
  const inputRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleSend = async (text) => {
    const msg = (text || input).trim()
    if (!msg || sending) return

    const userMsg = {
      id: Date.now(),
      role: 'user',
      text: msg,
      timestamp: new Date().toISOString(),
    }
    const loadingId = Date.now() + 1
    const loadingMsg = { id: loadingId, role: 'bot', loading: true }

    setMessages((prev) => [...prev, userMsg, loadingMsg])
    setInput('')
    setSending(true)

    try {
      const res = await sendMessage(msg)
      const botText = res.data?.data?.response || "I'm not sure how to answer that. Could you rephrase?"
      setMessages((prev) =>
        prev.map((m) =>
          m.id === loadingId
            ? { id: loadingId, role: 'bot', text: botText, timestamp: new Date().toISOString() }
            : m
        )
      )
    } catch (err) {
      const errText =
        err.response?.status === 401
          ? 'Session expired. Please sign in again.'
          : err.response?.data?.message || 'Something went wrong. Please try again.'

      if (err.response?.status === 401) {
        logout()
        navigate('/auth')
        return
      }

      setMessages((prev) =>
        prev.map((m) =>
          m.id === loadingId
            ? { id: loadingId, role: 'bot', text: `⚠️ ${errText}`, timestamp: new Date().toISOString() }
            : m
        )
      )
    } finally {
      setSending(false)
      inputRef.current?.focus()
    }
  }

  const handleKey = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  const handleLogout = () => {
    logout()
    navigate('/')
  }

  return (
    <div className={styles.page}>
      {/* Sidebar */}
      <aside className={styles.sidebar}>
        <div className={styles.sidebarTop}>
          <h2 className={styles.sidebarLogo}>Bean<br />Brew</h2>
          <p className={styles.sidebarTagline}>Your AI barista</p>
        </div>

        <div className={styles.userCard}>
          <span className={styles.userInitial}>{user?.name?.[0] || '?'}</span>
          <div>
            <p className={styles.userName}>{user?.name}</p>
            <p className={styles.userEmail}>{user?.email}</p>
          </div>
        </div>

        <div className={styles.quickSection}>
          <p className={styles.quickLabel}>Quick asks</p>
          {QUICK_PROMPTS.map((qp) => (
            <button
              key={qp.label}
              className={styles.quickBtn}
              onClick={() => handleSend(qp.message)}
              disabled={sending}
            >
              {qp.label}
            </button>
          ))}
        </div>

        <button className={styles.logoutBtn} onClick={handleLogout}>
          Sign out
        </button>
      </aside>

      {/* Chat area */}
      <main className={styles.chat}>
        <header className={styles.chatHeader}>
          <div className={styles.headerLeft}>
            <span className={styles.onlineDot} />
            <span className={styles.headerTitle}>BeanBrew Barista</span>
          </div>
          <span className={styles.headerSub}>☕ 42 Brew Street, Coimbatore</span>
        </header>

        <div className={styles.messages}>
          {messages.map((msg) => (
            <Message key={msg.id} msg={msg} />
          ))}
          <div ref={bottomRef} />
        </div>

        <div className={styles.inputArea}>
          <textarea
            ref={inputRef}
            className={styles.input}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKey}
            placeholder="Ask your barista anything… ☕"
            rows={1}
            disabled={sending}
          />
          <button
            className={styles.sendBtn}
            onClick={() => handleSend()}
            disabled={!input.trim() || sending}
            aria-label="Send message"
          >
            {sending ? '⏳' : '→'}
          </button>
        </div>
      </main>
    </div>
  )
}
