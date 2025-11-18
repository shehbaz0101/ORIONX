'use client'

export default function PortfolioPage() {
  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Portfolio</h1>
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="card-stripe p-6">
          <h3 className="text-sm text-slate-600 mb-2">Total Value</h3>
          <p className="text-2xl font-bold">$125,450.00</p>
        </div>
        <div className="card-stripe p-6">
          <h3 className="text-sm text-slate-600 mb-2">PnL</h3>
          <p className="text-2xl font-bold text-green-600">+$12,450.00</p>
        </div>
        <div className="card-stripe p-6">
          <h3 className="text-sm text-slate-600 mb-2">PnL %</h3>
          <p className="text-2xl font-bold text-green-600">+11.02%</p>
        </div>
        <div className="card-stripe p-6">
          <h3 className="text-sm text-slate-600 mb-2">Positions</h3>
          <p className="text-2xl font-bold">24</p>
        </div>
      </div>
      <div className="card-stripe p-6">
        <h2 className="text-xl font-semibold mb-4">Holdings</h2>
        <p className="text-slate-600">Portfolio holdings table will be displayed here</p>
      </div>
    </div>
  )
}
