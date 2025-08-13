import React, { useState } from 'react'
import axios from 'axios'
import OrdersTable from './components/OrdersTable'

export default function App() {
  const [orders, setOrders] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleFile = async (e) => {
    const file = e.target.files[0]
    if (!file) return
    const form = new FormData()
    form.append('file', file)
    setLoading(true)
    setError(null)
    try {
      const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000'
      const res = await axios.post(`${BACKEND_URL}/extract`, form, {
        headers: { 'Content-Type': 'multipart/form-data' },
        timeout: 60000,
      })
      setOrders(res.data.orders || [])
    } catch (err) {
      console.error(err)
      setError(err.response?.data?.detail || err.message)
    } finally {
      setLoading(false)
    }
  }

  const downloadCSV = () => {
    if (!orders.length) return
    const header = ['item,qty,unit_price,amount,due']
    const rows = orders.map(o => `${escapeCsv(o.item)},${o.qty||''},${o.unit_price||''},${o.amount||''},${o.due||''}`)
    const csv = header.concat(rows).join('\n')
    const blob = new Blob([csv], { type: 'text/csv' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'orders.csv'
    document.body.appendChild(a)
    a.click()
    a.remove()
    URL.revokeObjectURL(url)
  }

  const escapeCsv = (s) => '"' + (s || '').replace(/"/g, '""') + '"'

  return (
    <div className="container">
      <h1>일본어 PDF 발주서 추출기</h1>
      <p>PDF 업로드하면 주요 발주정보를 추출합니다.</p>

      <input type="file" accept="application/pdf" onChange={handleFile} />
      {loading && <p>처리중...</p>}
      {error && <p className="error">에러: {error}</p>}

      <div style={{ marginTop: 12 }}>
        <button onClick={downloadCSV} disabled={!orders.length}>CSV 다운로드</button>
      </div>

      <OrdersTable orders={orders} />
    </div>
  )
}
