import { useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { useCreateInvitation, useOrganizationDetails } from '../../hooks/useOrganization'
import Button from '../../components/ui/Button'
import Input from '../../components/ui/Input'
import Card from '../../components/ui/Card'

const ROLES = ['admin', 'member', 'viewer']

export default function InvitePage() {
  const { orgId } = useParams()
  const { data: org } = useOrganizationDetails(orgId)
  const invite = useCreateInvitation(orgId)

  const [form, setForm] = useState({
    org_id: Number(orgId),
    invited_user_email: '',
    invited_for_role: 'member',
  })

  const handleSubmit = (e) => {
    e.preventDefault()
    invite.mutate(form, {
      onSuccess: () => setForm((f) => ({ ...f, invited_user_email: '' })),
    })
  }

  return (
    <div className="max-w-lg">
      <div className="flex items-center gap-2 text-sm text-gray-500 mb-4">
        <Link to="/dashboard" className="hover:text-indigo-600">Organizations</Link>
        <span>/</span>
        <Link to={`/organization/${orgId}`} className="hover:text-indigo-600">{org?.name}</Link>
        <span>/</span>
        <span className="text-gray-900">Invite</span>
      </div>

      <h1 className="text-2xl font-bold text-gray-900 mb-6">Invite a member</h1>

      <Card>
        <Card.Body>
          {invite.isSuccess && (
            <div className="mb-4 p-3 bg-green-50 border border-green-200 rounded-md text-sm text-green-700">
              Invitation sent successfully.
            </div>
          )}

          {invite.error && (
            <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-md text-sm text-red-700">
              {invite.error.response?.data?.detail ?? 'Failed to send invitation.'}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <Input
              label="Email address"
              type="email"
              required
              placeholder="colleague@example.com"
              value={form.invited_user_email}
              onChange={(e) => setForm((f) => ({ ...f, invited_user_email: e.target.value }))}
            />

            <div className="flex flex-col gap-1">
              <label className="text-sm font-medium text-gray-700">Role</label>
              <select
                value={form.invited_for_role}
                onChange={(e) => setForm((f) => ({ ...f, invited_for_role: e.target.value }))}
                className="block w-full px-3 py-2 border border-gray-300 rounded-md text-sm
                  focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500"
              >
                {ROLES.map((r) => (
                  <option key={r} value={r} className="capitalize">{r}</option>
                ))}
              </select>
            </div>

            <div className="flex gap-2 pt-2">
              <Button type="submit" isLoading={invite.isPending}>Send invitation</Button>
              <Link to={`/organization/${orgId}`}>
                <Button type="button" variant="secondary">Cancel</Button>
              </Link>
            </div>
          </form>
        </Card.Body>
      </Card>
    </div>
  )
}
