import { Link, useParams } from 'react-router-dom'
import { useOrganizationDetails } from '../../hooks/useOrganization'
import useAuthStore from '../../store/authStore'
import Button from '../../components/ui/Button'
import Card from '../../components/ui/Card'

export default function OrganizationPage() {
  const { orgId } = useParams()
  const { user } = useAuthStore()
  const { data: org, isLoading, error } = useOrganizationDetails(orgId)

  const currentMember = org?.users?.find((u) => u.id === user?.id)
  const canManage = ['owner', 'admin'].includes(currentMember?.user_role)

  if (isLoading) {
    return (
      <div className="flex justify-center py-12">
        <div className="animate-spin h-8 w-8 border-4 border-indigo-600 border-t-transparent rounded-full" />
      </div>
    )
  }

  if (error) {
    return (
      <div className="text-center py-12 text-red-600">
        {error.response?.data?.detail ?? 'Failed to load organization.'}
      </div>
    )
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <div>
          <div className="flex items-center gap-2 text-sm text-gray-500 mb-1">
            <Link to="/dashboard" className="hover:text-indigo-600">Organizations</Link>
            <span>/</span>
            <span className="text-gray-900">{org?.name}</span>
          </div>
          <h1 className="text-2xl font-bold text-gray-900">{org?.name}</h1>
          {org?.description && (
            <p className="text-gray-500 mt-1 text-sm">{org.description}</p>
          )}
        </div>

        {canManage && (
          <Link to={`/organization/${orgId}/invite`}>
            <Button>Invite Member</Button>
          </Link>
        )}
      </div>

      <Card>
        <Card.Header>
          <div className="flex items-center justify-between">
            <h2 className="text-base font-semibold text-gray-900">
              Members ({org?.users?.length ?? 0})
            </h2>
            <Link
              to={`/organization/${orgId}/members`}
              className="text-sm text-indigo-600 hover:text-indigo-500"
            >
              Manage →
            </Link>
          </div>
        </Card.Header>
        <Card.Body className="p-0">
          <ul className="divide-y divide-gray-100">
            {org?.users?.map((member) => (
              <li key={member.id} className="flex items-center justify-between px-6 py-3">
                <div>
                  <p className="text-sm font-medium text-gray-900">
                    {member.first_name} {member.last_name}
                    {member.id === user?.id && (
                      <span className="ml-2 text-xs text-gray-400">(you)</span>
                    )}
                  </p>
                  <p className="text-xs text-gray-500">{member.email}</p>
                </div>
                <span className="text-xs font-medium capitalize text-indigo-700 bg-indigo-50 px-2 py-0.5 rounded-full">
                  {member.user_role}
                </span>
              </li>
            ))}
          </ul>
        </Card.Body>
      </Card>
    </div>
  )
}
