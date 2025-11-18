'use client'

import { useState } from 'react'
import { useAuth } from '../../../context/auth-context'
import { useRouter } from 'next/navigation'
import Link from 'next/link'

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const { login } = useAuth()
  const router = useRouter()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    
    try {
      await login(email, password)
      router.push('/dashboard')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Login failed')
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-b from-slate-50 to-white px-6">
      <div className="card-stripe p-8 w-full max-w-md">
        <h1 className="text-3xl font-bold mb-6">Login to ORIONX</h1>
        <form onSubmit={handleSubmit} className="space-y-4">
          {error && (
            <div className="bg-red-50 text-red-600 p-3 rounded-lg text-sm">
              {error}
            </div>
          )}
          <div>
            <label className="block text-sm font-medium mb-2">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="input-stripe w-full"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-2">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="input-stripe w-full"
              required
            />
          </div>
          <button type="submit" className="btn-stripe w-full">
            Login
          </button>
        </form>
        <p className="mt-6 text-center text-slate-600">
          Don't have an account?{' '}
          <Link href="/auth/register" className="text-stripe-blue hover:underline">
            Sign up
          </Link>
        </p>
      </div>
    </div>
  )
}
