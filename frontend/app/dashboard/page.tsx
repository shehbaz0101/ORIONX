'use client'

export default function DashboardPage() {
  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="card-stripe p-6">
          <h3 className="text-sm text-slate-600 mb-2">Portfolio Value</h3>
          <p className="text-2xl font-bold">$125,450.00</p>
        </div>
        <div className="card-stripe p-6">
          <h3 className="text-sm text-slate-600 mb-2">Today's PnL</h3>
          <p className="text-2xl font-bold text-green-600">+$1,234.56</p>
        </div>
        <div className="card-stripe p-6">
          <h3 className="text-sm text-slate-600 mb-2">Positions</h3>
          <p className="text-2xl font-bold">24</p>
        </div>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="card-stripe p-6">
          <h2 className="text-xl font-semibold mb-4">Recent News</h2>
          <p className="text-slate-600">News feed will be displayed here</p>
        </div>
        <div className="card-stripe p-6">
          <h2 className="text-xl font-semibold mb-4">Risk Alerts</h2>
          <p className="text-slate-600">Risk alerts will be displayed here</p>
        </div>
      </div>
    </div>
  )
}

