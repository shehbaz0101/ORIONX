'use client'

import Link from 'next/link'
import { motion } from 'framer-motion'

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50 to-white">
      {/* Navigation */}
      <nav className="fixed top-0 w-full bg-white/80 backdrop-blur-sm border-b border-slate-200 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="text-2xl font-bold text-stripe-blue">ORIONX</div>
          <div className="flex items-center gap-6">
            <Link href="/auth/login" className="text-slate-600 hover:text-slate-900">Login</Link>
            <Link href="/auth/register" className="btn-stripe">Get Started</Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-6">
        <div className="max-w-7xl mx-auto text-center">
          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="text-6xl font-bold text-slate-900 mb-6"
          >
            AI-Powered Financial
            <br />
            <span className="text-stripe-blue">Terminal</span>
          </motion.h1>
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="text-xl text-slate-600 mb-8 max-w-2xl mx-auto"
          >
            Real-time market data, AI insights, portfolio analytics, and more.
            Built for modern traders and analysts.
          </motion.p>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
            className="flex gap-4 justify-center"
          >
            <Link href="/auth/register" className="btn-stripe text-lg px-8 py-4">
              Start Free Trial
            </Link>
            <Link href="/dashboard" className="btn-stripe bg-white text-stripe-blue border-2 border-stripe-blue hover:bg-slate-50 text-lg px-8 py-4">
              View Demo
            </Link>
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-6 bg-white">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-4xl font-bold text-center mb-16">Features</h2>
          <div className="grid md:grid-cols-3 gap-8">
            {[
              { title: "Real-Time Data", desc: "Live market data from multiple sources" },
              { title: "AI Copilot", desc: "Intelligent assistant for financial analysis" },
              { title: "Portfolio Analytics", desc: "Advanced PnL and risk metrics" },
              { title: "News & Sentiment", desc: "AI-powered news analysis" },
              { title: "SEC Filings RAG", desc: "Semantic search in filings" },
              { title: "Risk Engine", desc: "Comprehensive risk analysis" },
            ].map((feature, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: i * 0.1 }}
                className="card-stripe p-6"
              >
                <h3 className="text-xl font-semibold mb-3">{feature.title}</h3>
                <p className="text-slate-600">{feature.desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 px-6 border-t border-slate-200">
        <div className="max-w-7xl mx-auto text-center text-slate-600">
          <p>© 2024 ORIONX. All rights reserved.</p>
        </div>
      </footer>
    </div>
  )
}
