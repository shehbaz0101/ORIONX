'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { 
  BarChart3, Portfolio, Newspaper, FileText, Shield, 
  Search, Zap, MessageSquare, Settings 
} from 'lucide-react'

const navItems = [
  { href: '/dashboard', label: 'Overview', icon: BarChart3 },
  { href: '/dashboard/markets', label: 'Markets', icon: BarChart3 },
  { href: '/dashboard/portfolio', label: 'Portfolio', icon: Portfolio },
  { href: '/dashboard/news', label: 'News', icon: Newspaper },
  { href: '/dashboard/filings', label: 'Filings', icon: FileText },
  { href: '/dashboard/risk', label: 'Risk', icon: Shield },
  { href: '/dashboard/screener', label: 'Screener', icon: Search },
  { href: '/dashboard/scenario', label: 'Scenario', icon: Zap },
  { href: '/dashboard/ai', label: 'AI Copilot', icon: MessageSquare },
  { href: '/dashboard/settings', label: 'Settings', icon: Settings },
]

export default function Sidebar() {
  const pathname = usePathname()

  return (
    <aside className="w-64 bg-white border-r border-slate-200 min-h-screen p-6">
      <div className="text-2xl font-bold text-stripe-blue mb-8">ORIONX</div>
      <nav className="space-y-2">
        {navItems.map((item) => {
          const Icon = item.icon
          const isActive = pathname === item.href
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                isActive
                  ? 'bg-stripe-blue text-white'
                  : 'text-slate-600 hover:bg-slate-100'
              }`}
            >
              <Icon size={20} />
              <span>{item.label}</span>
            </Link>
          )
        })}
      </nav>
    </aside>
  )
}
