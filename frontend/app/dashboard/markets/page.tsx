'use client'

export default function MarketsPage() {
  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Markets</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="card-stripe p-6">
          <h3 className="text-sm text-slate-600 mb-2">S&P 500</h3>
          <p className="text-2xl font-bold">4,567.89</p>
          <p className="text-green-600 text-sm">+1.23%</p>
        </div>
        <div className="card-stripe p-6">
          <h3 className="text-sm text-slate-600 mb-2">NASDAQ</h3>
          <p className="text-2xl font-bold">14,234.56</p>
          <p className="text-green-600 text-sm">+0.89%</p>
        </div>
        <div className="card-stripe p-6">
          <h3 className="text-sm text-slate-600 mb-2">DOW</h3>
          <p className="text-2xl font-bold">34,567.89</p>
          <p className="text-red-600 text-sm">-0.45%</p>
        </div>
      </div>
      <div className="card-stripe p-6">
        <h2 className="text-xl font-semibold mb-4">Real-Time Market Data</h2>
        <p className="text-slate-600">Market charts and data will be displayed here</p>
      </div>
    </div>
  )
}
