import { createContext, useContext, useState, useEffect, useCallback } from 'react'
import { login as apiLogin, register as apiRegister, getMe } from '../api/client'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem('bb_token')
    if (token) {
      getMe()
        .then((res) => setUser(res.data))
        .catch(() => localStorage.removeItem('bb_token'))
        .finally(() => setLoading(false))
    } else {
      setLoading(false)
    }
  }, [])

  const login = useCallback(async (email, password) => {
    const res = await apiLogin({ email, password })
    localStorage.setItem('bb_token', res.data.access_token)
    setUser({ customer_id: res.data.customer_id, name: res.data.name, email: res.data.email })
    return res.data
  }, [])

  const register = useCallback(async (name, email, password) => {
    const res = await apiRegister({ name, email, password })
    localStorage.setItem('bb_token', res.data.access_token)
    setUser({ customer_id: res.data.customer_id, name: res.data.name, email: res.data.email })
    return res.data
  }, [])

  const logout = useCallback(() => {
    localStorage.removeItem('bb_token')
    setUser(null)
  }, [])

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  return useContext(AuthContext)
}
