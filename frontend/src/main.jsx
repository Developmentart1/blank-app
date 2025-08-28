import React from 'react'
import { createRoot } from 'react-dom/client'

function App() {
  const [health, setHealth] = React.useState(null)
  React.useEffect(() => {
    const base = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'
    fetch(`${base}/health`).then(r => r.json()).then(setHealth).catch(() => setHealth({ status: 'error' }))
  }, [])
  return (
    <div style={{ fontFamily: 'Inter, system-ui, Arial', padding: 16 }}>
      <h1>Modelo Vivo — Ejecutivo</h1>
      <p>API health: {health ? JSON.stringify(health) : '...'}</p>
    </div>
  )
}

createRoot(document.getElementById('root')).render(<App />)
