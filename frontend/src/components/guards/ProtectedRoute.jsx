import { useEffect, useState } from 'react'
import { Navigate, Outlet } from 'react-router-dom'
import useAuthStore from '../../store/authStore'
import { refreshAccessToken } from '../../api/auth'

export default function ProtectedRoute() {
  const { isAuthenticated, setAccessToken, clearAuth } = useAuthStore()
  const [checking, setChecking] = useState(!isAuthenticated)

  useEffect(() => {
    if (isAuthenticated) return

    refreshAccessToken()
      .then((data) => setAccessToken(data.access_token))
      .catch(() => clearAuth())
      .finally(() => setChecking(false))
  }, [])

  if (checking) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin h-8 w-8 border-4 border-indigo-600 border-t-transparent rounded-full" />
      </div>
    )
  }

  return isAuthenticated ? <Outlet /> : <Navigate to="/login" replace />
}
