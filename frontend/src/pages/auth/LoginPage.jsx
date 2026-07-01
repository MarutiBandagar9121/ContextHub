import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useLogin } from '../../hooks/useAuth'
import Button from '../../components/ui/Button'
import Input from '../../components/ui/Input'

export default function LoginPage() {
  const [form, setForm] = useState({ email: '', password: '' })
  const login = useLogin()

  const handleSubmit = (e) => {
    e.preventDefault()
    login.mutate(form)
  }

  return (
    <div>
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Sign in</h2>

      {login.error && (
        <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-md text-sm text-red-700">
          {login.error.response?.data?.detail ?? 'Login failed. Please try again.'}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <Input
          label="Email"
          type="email"
          required
          autoComplete="email"
          value={form.email}
          onChange={(e) => setForm((f) => ({ ...f, email: e.target.value }))}
        />
        <Input
          label="Password"
          type="password"
          required
          autoComplete="current-password"
          value={form.password}
          onChange={(e) => setForm((f) => ({ ...f, password: e.target.value }))}
        />
        <Button type="submit" className="w-full" isLoading={login.isPending}>
          Sign in
        </Button>
      </form>

      <p className="mt-4 text-sm text-center text-gray-600">
        Don't have an account?{' '}
        <Link to="/register" className="text-indigo-600 hover:text-indigo-500 font-medium">
          Register
        </Link>
      </p>
    </div>
  )
}
