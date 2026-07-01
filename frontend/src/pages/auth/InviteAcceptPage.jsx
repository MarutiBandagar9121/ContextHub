import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useQuery, useMutation } from '@tanstack/react-query'
import { checkInvitationStatus, acceptInvitationNewUser } from '../../api/organization'
import useAuthStore from '../../store/authStore'
import Button from '../../components/ui/Button'
import Input from '../../components/ui/Input'

export default function InviteAcceptPage() {
  const { token } = useParams()
  const navigate = useNavigate()
  const { setAuth } = useAuthStore()
  const [form, setForm] = useState({ first_name: '', last_name: '', password: '' })

  const { data: invitation, isLoading, error } = useQuery({
    queryKey: ['invitation', token],
    queryFn: () => checkInvitationStatus(token),
  })

  // If the user already exists, redirect them to login with a note
  useEffect(() => {
    if (invitation?.user_exists) {
      navigate('/login', {
        state: { notice: `Sign in to accept your invitation to ${invitation.org_name}.` },
      })
    }
  }, [invitation])

  const accept = useMutation({
    mutationFn: (data) => acceptInvitationNewUser(token, data),
    onSuccess: (data) => {
      setAuth(
        { id: data.user_id },
        data.access_token
      )
      navigate('/dashboard')
    },
  })

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin h-8 w-8 border-4 border-indigo-600 border-t-transparent rounded-full" />
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center p-4">
        <div className="text-center">
          <h2 className="text-xl font-bold text-gray-900 mb-2">Invalid invitation</h2>
          <p className="text-gray-500 text-sm">
            {error.response?.data?.detail ?? 'This invitation link is invalid or has expired.'}
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <h1 className="text-center text-3xl font-bold text-indigo-600">ContextHub</h1>
        <h2 className="mt-4 text-center text-xl font-semibold text-gray-900">
          You've been invited to{' '}
          <span className="text-indigo-600">{invitation?.org_name}</span>
        </h2>
        <p className="mt-1 text-center text-sm text-gray-500">
          as <span className="font-medium">{invitation?.user_role}</span> · {invitation?.user_email}
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white py-8 px-4 shadow rounded-lg sm:px-10">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Create your account</h3>

          {accept.error && (
            <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-md text-sm text-red-700">
              {accept.error.response?.data?.detail ?? 'Something went wrong. Please try again.'}
            </div>
          )}

          <form
            onSubmit={(e) => {
              e.preventDefault()
              accept.mutate(form)
            }}
            className="space-y-4"
          >
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
              label="Password"
              type="password"
              required
              autoComplete="new-password"
              value={form.password}
              onChange={(e) => setForm((f) => ({ ...f, password: e.target.value }))}
            />
            <Button type="submit" className="w-full" isLoading={accept.isPending}>
              Create account & join {invitation?.org_name}
            </Button>
          </form>
        </div>
      </div>
    </div>
  )
}
