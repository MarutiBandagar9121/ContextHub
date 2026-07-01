import { Link, NavLink, Outlet, useNavigate } from 'react-router-dom'
import useAuthStore from '../../store/authStore'
import { useLogout } from '../../hooks/useAuth'

export default function AppLayout() {
  const { user } = useAuthStore()
  const logout = useLogout()

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <div className="flex items-center gap-8">
              <Link to="/dashboard" className="text-xl font-bold text-indigo-600">
                ContextHub
              </Link>
              <NavLink
                to="/dashboard"
                className={({ isActive }) =>
                  `text-sm font-medium ${isActive ? 'text-indigo-600' : 'text-gray-500 hover:text-gray-900'}`
                }
              >
                Organizations
              </NavLink>
            </div>

            <div className="flex items-center gap-4">
              {user && (
                <span className="text-sm text-gray-600">
                  {user.first_name} {user.last_name}
                </span>
              )}
              <button
                onClick={() => logout.mutate()}
                className="text-sm text-gray-500 hover:text-gray-900"
              >
                Sign out
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Outlet />
      </main>
    </div>
  )
}
