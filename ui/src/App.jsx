import { useState } from 'react'

export default function App() {
  const [maSv, setMaSv] = useState('')
  const [maPhien, setMaPhien] = useState('')
  const [status, setStatus] = useState('idle') // 'idle' | 'loading' | 'success' | 'conflict' | 'error'
  const [message, setMessage] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!maSv.trim() || !maPhien.trim()) {
      setStatus('error')
      setMessage('Vui lòng nhập đầy đủ mã sinh viên và mã phiên!')
      return
    }

    // Trạng thái 1: Đang gửi
    setStatus('loading')
    setMessage('Đang xử lý đăng ký...')

    try {
      const response = await fetch('http://localhost:8000/api/dang-ky', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ma_sv: maSv.trim(),
          ma_phien: maPhien.trim(),
        }),
      })

      if (response.status === 201) {
        // Trạng thái 2: Thành công (201 Created)
        setStatus('success')
        setMessage('Đăng ký tham gia phiên thành công! (Mã: 201 Created)')
      } else if (response.status === 409) {
        // Trạng thái 3: Báo lỗi trùng (409 Conflict)
        const data = await response.json().catch(() => ({}))
        setStatus('conflict')
        setMessage(
          `Bạn đã đăng ký phiên này trước đó rồi! (${data.detail || 'DA_DANG_KY'} - Mã: 409 Conflict)`
        )
      } else {
        const errorData = await response.json().catch(() => ({}))
        setStatus('error')
        setMessage(`Đã có lỗi xảy ra (${response.status}): ${JSON.stringify(errorData)}`)
      }
    } catch (err) {
      setStatus('error')
      setMessage(`Không thể kết nối đến máy chủ backend (http://localhost:8000): ${err.message}`)
    }
  }

  return (
    <div style={{
      maxWidth: '480px',
      width: '100%',
      backgroundColor: '#ffffff',
      borderRadius: '12px',
      boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
      padding: '32px',
      margin: '0 auto'
    }}>
      <div style={{ textAlign: 'center', marginBottom: '24px' }}>
        <h1 style={{ fontSize: '24px', fontWeight: 'bold', color: '#111827', marginBottom: '8px' }}>
          Đăng Ký Ngày Hội Việc Làm
        </h1>
        <p style={{ fontSize: '14px', color: '#6b7280' }}>
          Nhập mã sinh viên và chọn mã phiên hội thảo/phỏng vấn
        </p>
      </div>

      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '16px' }}>
          <label 
            htmlFor="ma_sv" 
            style={{ display: 'block', fontSize: '14px', fontWeight: '500', color: '#374151', marginBottom: '6px' }}
          >
            Mã sinh viên (ma_sv)
          </label>
          <input
            id="ma_sv"
            type="text"
            placeholder="Ví dụ: 22020001"
            value={maSv}
            onChange={(e) => setMaSv(e.target.value)}
            disabled={status === 'loading'}
            style={{
              width: '100%',
              padding: '10px 14px',
              borderRadius: '6px',
              border: '1px solid #d1d5db',
              fontSize: '14px',
              outline: 'none',
              boxSizing: 'border-box'
            }}
            required
          />
        </div>

        <div style={{ marginBottom: '20px' }}>
          <label 
            htmlFor="ma_phien" 
            style={{ display: 'block', fontSize: '14px', fontWeight: '500', color: '#374151', marginBottom: '6px' }}
          >
            Mã phiên (ma_phien)
          </label>
          <input
            id="ma_phien"
            type="text"
            placeholder="Ví dụ: P01"
            value={maPhien}
            onChange={(e) => setMaPhien(e.target.value)}
            disabled={status === 'loading'}
            style={{
              width: '100%',
              padding: '10px 14px',
              borderRadius: '6px',
              border: '1px solid #d1d5db',
              fontSize: '14px',
              outline: 'none',
              boxSizing: 'border-box'
            }}
            required
          />
        </div>

        <button
          type="submit"
          disabled={status === 'loading'}
          style={{
            width: '100%',
            backgroundColor: status === 'loading' ? '#9ca3af' : '#2563eb',
            color: '#ffffff',
            padding: '12px',
            borderRadius: '6px',
            border: 'none',
            fontSize: '16px',
            fontWeight: '600',
            cursor: status === 'loading' ? 'not-allowed' : 'pointer',
            transition: 'background-color 0.2s',
          }}
        >
          {status === 'loading' ? 'Đang gửi thông tin...' : 'Đăng Ký Tham Gia'}
        </button>
      </form>

      {/* Khu vực hiển thị 3 trạng thái rõ ràng */}
      <div style={{ marginTop: '24px' }}>
        {status === 'loading' && (
          <div style={{
            padding: '12px 16px',
            backgroundColor: '#eff6ff',
            color: '#1d4ed8',
            borderRadius: '6px',
            border: '1px solid #bfdbfe',
            fontSize: '14px',
            display: 'flex',
            alignItems: 'center',
            gap: '8px'
          }}>
            <span>⏳</span>
            <span><strong>Trạng thái: Đang gửi</strong> — {message}</span>
          </div>
        )}

        {status === 'success' && (
          <div style={{
            padding: '12px 16px',
            backgroundColor: '#ecfdf5',
            color: '#047857',
            borderRadius: '6px',
            border: '1px solid #a7f3d0',
            fontSize: '14px',
            display: 'flex',
            alignItems: 'center',
            gap: '8px'
          }}>
            <span>✅</span>
            <span><strong>Trạng thái: Thành công (201 Created)</strong> — {message}</span>
          </div>
        )}

        {status === 'conflict' && (
          <div style={{
            padding: '12px 16px',
            backgroundColor: '#fffbeb',
            color: '#b45309',
            borderRadius: '6px',
            border: '1px solid #fde68a',
            fontSize: '14px',
            display: 'flex',
            alignItems: 'center',
            gap: '8px'
          }}>
            <span>⚠️</span>
            <span><strong>Trạng thái: Báo lỗi trùng (409 Conflict)</strong> — {message}</span>
          </div>
        )}

        {status === 'error' && (
          <div style={{
            padding: '12px 16px',
            backgroundColor: '#fef2f2',
            color: '#b91c1c',
            borderRadius: '6px',
            border: '1px solid #fecaca',
            fontSize: '14px',
            display: 'flex',
            alignItems: 'center',
            gap: '8px'
          }}>
            <span>❌</span>
            <span>{message}</span>
          </div>
        )}
      </div>
    </div>
  )
}

