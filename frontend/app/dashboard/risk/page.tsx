'use client'

export default function RiskPage() {
  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Risk Analysis</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="card-stripe p-6">
          <h3 className="text-sm text-slate-600 mb-2">Portfolio Volatility</h3>
          <p className="text-2xl font-bold">18.5%</p>
        </div>
        <div className="card-stripe p-6">
          <h3 className="text-sm text-slate-600 mb-2">VaR (95%)</h3>
          <p className="text-2xl font-bold">$12,450</p>
        </div>
        <div className="card-stripe p-6">
          <h3 className="text-sm text-slate-600 mb-2">Max Concentration</h3>
          <p className="text-2xl font-bold">15.2%</p>
        </div>
      </div>
      <div className="card-stripe p-6">
        <h2 className="text-xl font-semibold mb-4">Risk Metrics</h2>
        <p className="text-slate-600">Detailed risk analysis will be displayed here</p>
      </div>
    </div>
  )
}
