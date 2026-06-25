import { useState, useEffect } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'
import styles from './AuthPage.module.css'

export default function AuthPage() {
  const [params] = useSearchParams()
  const [mode, setMode] = useState(params.get('mode') === 'register' ? 'register' : 'login')
  const [form, setForm] = useState({ name: '', email: '', password: '' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const { login, register, user } = useAuth()
  const navigate = useNavigate()

  useEffect(() => {
    if (user) navigate('/chat')
  }, [user, navigate])

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      if (mode === 'login') {
        await login(form.email, form.password)
      } else {
        await register(form.name, form.email, form.password)
      }
      navigate('/chat')
    } catch (err) {
      setError(err.response?.data?.detail || 'Something went wrong. Try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className={styles.page}>
      <div className={styles.bgDecor} aria-hidden>
        <span>☕</span><span>🫘</span><span>🌿</span><span>✨</span>
      </div>

      <button className={styles.backBtn} onClick={() => navigate('/')}>
        ← Back
      </button>

      <div className={styles.card}>
        <div className={styles.cardHeader}>
          <span className={styles.cupIcon}>☕</span>
          <h1 className={styles.title}>
            {mode === 'login' ? 'Welcome back!' : 'Join BeanBrew'}
          </h1>
          <p className={styles.subtitle}>
            {mode === 'login'
              ? 'Sign in to chat with our barista'
              : 'Create your account and start ordering'}
          </p>
        </div>

        <form onSubmit={handleSubmit} className={styles.form}>
          {mode === 'register' && (
            <div className={styles.field}>
              <label htmlFor="name">Your name</label>
              <input
                id="name"
                type="text"
                placeholder="Alice"
                value={form.name}
                onChange={(e) => setForm({ ...form, name: e.target.value })}
                required
                minLength={2}
              />
            </div>
          )}
          <div className={styles.field}>
            <label htmlFor="email">Email</label>
            <input
              id="email"
              type="email"
              placeholder="alice@example.com"
              value={form.email}
              onChange={(e) => setForm({ ...form, email: e.target.value })}
              required
            />
          </div>
          <div className={styles.field}>
            <label htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              placeholder={mode === 'register' ? 'At least 6 characters' : '••••••••'}
              value={form.password}
              onChange={(e) => setForm({ ...form, password: e.target.value })}
              required
              minLength={6}
            />
          </div>

          {error && <p className={styles.error}>{error}</p>}

          <button type="submit" className={styles.submitBtn} disabled={loading}>
            {loading ? '⏳ Please wait...' : mode === 'login' ? '☕ Sign In' : '✨ Create Account'}
          </button>
        </form>

        <p className={styles.toggle}>
          {mode === 'login' ? "Don't have an account?" : 'Already have an account?'}
          {' '}
          <button
            className={styles.toggleBtn}
            onClick={() => { setMode(mode === 'login' ? 'register' : 'login'); setError('') }}
          >
            {mode === 'login' ? 'Register' : 'Sign in'}
          </button>
        </p>
      </div>
    </div>
  )
}
