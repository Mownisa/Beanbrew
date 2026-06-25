import { useNavigate } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'
import styles from './LandingPage.module.css'

export default function LandingPage() {
  const navigate = useNavigate()
  const { user } = useAuth()

  return (
    <div className={styles.page}>
      {/* Floating beans background */}
      <div className={styles.bgBeans} aria-hidden>
        {['☕','🫘','🌿','✨','🍵','☕','🫘','🌿'].map((e, i) => (
          <span key={i} className={styles.floatingBean} style={{
            '--delay': `${i * 0.7}s`,
            '--x': `${10 + i * 11}%`,
            '--size': `${1.2 + (i % 3) * 0.5}rem`,
          }}>{e}</span>
        ))}
      </div>

      <nav className={styles.nav}>
        <span className={styles.logo}>BeanBrew</span>
        <button
          className={styles.navBtn}
          onClick={() => navigate(user ? '/chat' : '/auth')}
        >
          {user ? 'Open Chat' : 'Sign In'}
        </button>
      </nav>

      <main className={styles.hero}>
        <p className={styles.eyebrow}>Your cozy corner, online ☕</p>
        <h1 className={styles.headline}>
          Coffee, ordered<br />
          <em>the clever way.</em>
        </h1>
        <p className={styles.sub}>
          Chat with our AI barista. Browse the menu, place orders, track your brew — 
          all in a single delightful conversation.
        </p>
        <div className={styles.ctas}>
          <button
            className={styles.primaryCta}
            onClick={() => navigate(user ? '/chat' : '/auth')}
          >
            {user ? '☕ Continue Chatting' : 'Start your order'}
          </button>
          <button
            className={styles.secondaryCta}
            onClick={() => navigate('/auth?mode=register')}
          >
            Create account
          </button>
        </div>
      </main>

      <section className={styles.features}>
        {[
          { icon: '🤖', title: 'AI Barista', desc: 'Our smart assistant knows the full menu and remembers your preferences across visits.' },
          { icon: '⚡', title: 'Instant Orders', desc: 'Just say what you want in plain language. No forms, no fuss, just coffee.' },
          { icon: '📍', title: 'Real-time Tracking', desc: 'Know exactly when your order moves from pending to ready.' },
        ].map((f) => (
          <div key={f.title} className={styles.featureCard}>
            <span className={styles.featureIcon}>{f.icon}</span>
            <h3 className={styles.featureTitle}>{f.title}</h3>
            <p className={styles.featureDesc}>{f.desc}</p>
          </div>
        ))}
      </section>

      <footer className={styles.footer}>
        <p>© 2025 BeanBrew · 42 Brew Street, Coimbatore · Made with ☕ &amp; LangGraph</p>
      </footer>
    </div>
  )
}
