import React, { useEffect, useState } from 'react'

function App() {
  const [status, setStatus] = useState({})

  useEffect(() => {
    fetch('/api/status').then(res => res.json()).then(setStatus)
  }, [])

  return (
    <div>
      <h1>TTS Bot Panel</h1>
      <pre>{JSON.stringify(status, null, 2)}</pre>
    </div>
  )
}

export default App
