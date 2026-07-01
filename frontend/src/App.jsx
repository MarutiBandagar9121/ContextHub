import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'

import AuthLayout from './components/layout/AuthLayout'
import AppLayout from './components/layout/AppLayout'
import ProtectedRoute from './components/guards/ProtectedRoute'

import LoginPage from './pages/auth/LoginPage'
import RegisterPage from './pages/auth/RegisterPage'
import VerifyOtpPage from './pages/auth/VerifyOtpPage'
import InviteAcceptPage from './pages/auth/InviteAcceptPage'

import DashboardPage from './pages/dashboard/DashboardPage'
import OrganizationPage from './pages/organization/OrganizationPage'
import MembersPage from './pages/organization/MembersPage'
import InvitePage from './pages/organization/InvitePage'
import KnowledgePage from './pages/knowledge/KnowledgePage'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      staleTime: 30_000,
    },
  },
})

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          {/* Public auth routes */}
          <Route element={<AuthLayout />}>
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/verify-otp" element={<VerifyOtpPage />} />
          </Route>

          {/* Invitation accept — standalone page (no layout shell) */}
          <Route path="/invite/:token" element={<InviteAcceptPage />} />

          {/* Protected app routes */}
          <Route element={<ProtectedRoute />}>
            <Route element={<AppLayout />}>
              <Route path="/dashboard" element={<DashboardPage />} />
              <Route path="/organization/:orgId" element={<OrganizationPage />} />
              <Route path="/organization/:orgId/members" element={<MembersPage />} />
              <Route path="/organization/:orgId/invite" element={<InvitePage />} />
              <Route path="/organization/:orgId/knowledge" element={<KnowledgePage />} />
            </Route>
          </Route>

          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  )
}
