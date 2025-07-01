import React, { useEffect, useState } from 'react'

function Setup({ onDone }) {
  const [form, setForm] = useState({
    admin_user: '',
    admin_pass: '',
    OPENAI_API_KEY: '',
    ELEVENLABS_API_KEY: '',
    WHISPER_API_KEY: ''
  })

  const submit = async () => {
    await fetch('/api/setup/install', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form)
    })
    onDone()
  }

  return (
    <div>
      <h2>Installer</h2>
      <input placeholder="Admin User" value={form.admin_user} onChange={e => setForm({ ...form, admin_user: e.target.value })} />
      <input type="password" placeholder="Password" value={form.admin_pass} onChange={e => setForm({ ...form, admin_pass: e.target.value })} />
      <input placeholder="OpenAI Key" value={form.OPENAI_API_KEY} onChange={e => setForm({ ...form, OPENAI_API_KEY: e.target.value })} />
      <input placeholder="ElevenLabs Key" value={form.ELEVENLABS_API_KEY} onChange={e => setForm({ ...form, ELEVENLABS_API_KEY: e.target.value })} />
      <input placeholder="Whisper Key" value={form.WHISPER_API_KEY} onChange={e => setForm({ ...form, WHISPER_API_KEY: e.target.value })} />
      <button onClick={submit}>Install</button>
    </div>
  )
}

function Login({ onToken }) {
  const [form, setForm] = useState({ username: '', password: '' })
  const login = async () => {
    const res = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form)
    })
    const data = await res.json()
    onToken(data.token)
  }
  return (
    <div>
      <h2>Login</h2>
      <input placeholder="User" value={form.username} onChange={e => setForm({ ...form, username: e.target.value })} />
      <input type="password" placeholder="Password" value={form.password} onChange={e => setForm({ ...form, password: e.target.value })} />
      <button onClick={login}>Login</button>
    </div>
  )
}

function Dashboard({ token }) {
  const [status, setStatus] = useState({})
  const load = () => {
    fetch('/api/status', { headers: { Authorization: `Bearer ${token}` } })
      .then(r => r.json()).then(setStatus)
  }
  useEffect(load, [token])
  return (
    <div>
      <h2>Status</h2>
      <pre>{JSON.stringify(status, null, 2)}</pre>
      <button onClick={load}>Refresh</button>
    </div>
  )
}

function App() {
  const [installed, setInstalled] = useState(null)
  const [token, setToken] = useState(localStorage.getItem('token') || '')

  useEffect(() => {
    fetch('/api/setup/status').then(res => res.json()).then(data => setInstalled(data.installed))
  }, [])

  if (installed === false) return <Setup onDone={() => setInstalled(true)} />
  if (!token) return <Login onToken={t => { localStorage.setItem('token', t); setToken(t) }} />
  return <Dashboard token={token} />
}

export default App
