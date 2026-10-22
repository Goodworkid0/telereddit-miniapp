import { useEffect, useMemo, useState } from 'react'
import './index.css'
import WebApp from '@twa-dev/sdk'

function App() {
  const [user, setUser] = useState<any>(null)
  const [error, setError] = useState<string | null>(null)
  const initData = useMemo(() => WebApp.initData || '', [])

  useEffect(() => {
    WebApp.ready()
    // Optional: expand to full height
    try { WebApp.expand() } catch {}
  }, [])

  async function verifySession() {
    setError(null)
    try {
      const res = await fetch('http://localhost:8000/api/session/verify', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ initData }),
      })
      if (!res.ok) throw new Error(await res.text())
      const data = await res.json()
      setUser(data.user)
    } catch (e: any) {
      setError(e.message || 'Failed to verify')
    }
  }

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100">
      <header className="sticky top-0 z-10 border-b border-white/10 bg-gray-900/80 backdrop-blur">
        <div className="mx-auto max-w-3xl px-4 py-3 flex items-center justify-between">
          <h1 className="text-lg font-semibold">TeleReddit</h1>
          <div className="text-xs opacity-70">Mini App</div>
        </div>
      </header>

      <main className="mx-auto max-w-3xl px-4 py-6 space-y-4">
        <section className="rounded-lg border border-white/10 bg-gray-900 p-4">
          <h2 className="text-sm font-medium mb-2">Session</h2>
          <div className="text-xs break-all text-gray-400">initData: {initData ? 'present' : 'missing (open in Telegram)'}
          </div>
          <div className="mt-3 flex gap-2">
            <button onClick={verifySession} className="px-3 py-1.5 rounded bg-emerald-600 hover:bg-emerald-500 text-sm">Verify</button>
            {user && <div className="text-sm">Hello, <span className="font-semibold">{user.first_name || user.id}</span></div>}
            {error && <div className="text-sm text-red-400">{error}</div>}
          </div>
        </section>

        <section className="rounded-lg border border-white/10 bg-gray-900 p-4">
          <h2 className="text-sm font-medium mb-2">Home</h2>
          <p className="text-sm text-gray-400">Coming soon: communities, posts, and feed.</p>
        </section>
      </main>
    </div>
  )
}

export default App
