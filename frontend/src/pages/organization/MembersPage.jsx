import { Link, useParams } from 'react-router-dom'
import { useOrganizationDetails } from '../../hooks/useOrganization'
import useAuthStore from '../../store/authStore'
import Card from '../../components/ui/Card'
import Button from '../../components/ui/Button'

export default function MembersPage() {
  const { orgId } = useParams()
  const { user } = useAuthStore()
  const { data: org, isLoading } = useOrganizationDetails(orgId)

  const currentMember = org?.users?.find((u) => u.id === user?.id)
  const isOwner = currentMember?.user_role === 'owner'

  if (isLoading) {
    return (
      <div className="flex justify-center py-12">
        <div className="animate-spin h-8 w-8 border-4 border-indigo-600 border-t-transparent rounded-full" />
      </div>
    )
  }

  return (
    <div>
      <div className="flex items-center gap-2 text-sm text-gray-500 mb-4">
        <Link to="/dashboard" className="hover:text-indigo-600">Organizations</Link>
        <span>/</span>
        <Link to={`/organization/${orgId}`} className="hover:text-indigo-600">{org?.name}</Link>
        <span>/</span>
        <span className="text-gray-900">Members</span>
      </div>

      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Members</h1>
        {['owner', 'admin'].includes(currentMember?.user_role) && (
          <Link to={`/organization/${orgId}/invite`}>
            <Button>Invite Member</Button>
          </Link>
        )}
      </div>

      <Card>
        <Card.Body className="p-0">
          <table className="min-w-full divide-y divide-gray-100">
            <thead>
              <tr className="bg-gray-50">
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Email</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Role</th>
                {isOwner && (
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                )}
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {org?.users?.map((member) => (
                <tr key={member.id}>
                  <td className="px-6 py-4 text-sm font-medium text-gray-900">
                    {member.first_name} {member.last_name}
                    {member.id === user?.id && (
                      <span className="ml-2 text-xs text-gray-400">(you)</span>
                    )}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-500">{member.email}</td>
                  <td className="px-6 py-4">
                    <span className="text-xs font-medium capitalize text-indigo-700 bg-indigo-50 px-2 py-0.5 rounded-full">
                      {member.user_role}
                    </span>
                  </td>
                  {isOwner && (
                    <td className="px-6 py-4 text-right">
                      {member.user_role !== 'owner' && (
                        <button className="text-sm text-red-500 hover:text-red-700">
                          Revoke
                        </button>
                      )}
                    </td>
                  )}
                </tr>
              ))}
            </tbody>
          </table>
        </Card.Body>
      </Card>
    </div>
  )
}
