import React from 'react'

export default function OrdersTable({ orders }){
  if (!orders || !orders.length) return <p>추출된 항목이 없습니다.</p>
  return (
    <table className="orders">
      <thead>
        <tr>
          <th>품목명</th>
          <th>수량</th>
          <th>단가</th>
          <th>금액</th>
          <th>납기</th>
        </tr>
      </thead>
      <tbody>
        {orders.map((o, i) => (
          <tr key={i}>
            <td>{o.item}</td>
            <td>{o.qty || ''}</td>
            <td>{o.unit_price || ''}</td>
            <td>{o.amount || ''}</td>
            <td>{o.due || ''}</td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}
