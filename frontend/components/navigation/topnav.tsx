'use client'

import { useAuth } from '../../context/auth-context'

export default function TopNav() {
  const { user, logout } = useAuth()

  return (
    <nav className="bg-white border-b border-slate-200 px-8 py-4 flex items-center justify-between">
      <div className="text-lg font-semibold">Dashboard</div>
      <div className="flex items-center gap-4">
        <span className="text-slate-600">{user?.email}</span>
        <button
          onClick={logout}
          className="text-slate-600 hover:text-slate-900"
        >
          Logout
        </button>
      </div>
    </nav>
  )
}
