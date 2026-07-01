import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useRegister } from '../../hooks/useAuth'
import Button from '../../components/ui/Button'
import Input from '../../components/ui/Input'

export default function RegisterPage() {
  const [form, setForm] = useState({
    first_name: '',
    last_name: '',
    email: '',
    password: '',
  })
  const register = useRegister()

  const handleSubmit = (e) => {
    e.preventDefault()
    register.mutate(form)
  }

  return (
    <div>
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Create account</h2>

      {register.error && (
        <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-md text-sm text-red-700">
          {register.error.response?.data?.detail ?? 'Registration failed. Please try again.'}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="flex gap-3">
          <Input
            label="First name"
            type="text"
            required
            value={form.first_name}
            onChange={(e) => setForm((f) => ({ ...f, first_name: e.target.value }))}
          />
          <Input
            label="Last name"
            type="text"
            value={form.last_name}
            onChange={(e) => setForm((f) => ({ ...f, last_name: e.target.value }))}
          />
        </div>
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
          autoComplete="new-password"
          value={form.password}
          onChange={(e) => setForm((f) => ({ ...f, password: e.target.value }))}
        />
        <Button type="submit" className="w-full" isLoading={register.isPending}>
          Create account
        </Button>
      </form>

      <p className="mt-4 text-sm text-center text-gray-600">
        Already have an account?{' '}
        <Link to="/login" className="text-indigo-600 hover:text-indigo-500 font-medium">
          Sign in
        </Link>
      </p>
    </div>
  )
}
