import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useCreateOrganization, useDeleteOrganization, useUserOrganizations } from '../../hooks/useOrganization'
import useAuthStore from '../../store/authStore'
import Button from '../../components/ui/Button'
import Card from '../../components/ui/Card'
import Input from '../../components/ui/Input'

export default function DashboardPage() {
  const { user } = useAuthStore()
  const { data: orgs, isLoading } = useUserOrganizations()
  const createOrg = useCreateOrganization()
  const deleteOrg = useDeleteOrganization()

  const [showCreate, setShowCreate] = useState(false)
  const [form, setForm] = useState({ name: '', description: '' })

  const handleCreate = (e) => {
    e.preventDefault()
    createOrg.mutate(form, {
      onSuccess: () => {
        setForm({ name: '', description: '' })
        setShowCreate(false)
      },
    })
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Your Organizations</h1>
          {user && (
            <p className="text-sm text-gray-500 mt-1">Welcome back, {user.first_name}</p>
          )}
        </div>
        <Button onClick={() => setShowCreate(true)}>New Organization</Button>
      </div>

      {showCreate && (
        <Card className="mb-6">
          <Card.Header>
            <h2 className="text-base font-semibold text-gray-900">Create Organization</h2>
          </Card.Header>
          <Card.Body>
            <form onSubmit={handleCreate} className="space-y-3 max-w-md">
              <Input
                label="Name"
                type="text"
                required
                value={form.name}
                onChange={(e) => setForm((f) => ({ ...f, name: e.target.value }))}
              />
              <Input
                label="Description (optional)"
                type="text"
                value={form.description}
                onChange={(e) => setForm((f) => ({ ...f, description: e.target.value }))}
              />
              {createOrg.error && (
                <p className="text-sm text-red-600">
                  {createOrg.error.response?.data?.detail ?? 'Failed to create organization.'}
                </p>
              )}
              <div className="flex gap-2">
                <Button type="submit" isLoading={createOrg.isPending}>Create</Button>
                <Button
                  type="button"
                  variant="secondary"
                  onClick={() => setShowCreate(false)}
                >
                  Cancel
                </Button>
              </div>
            </form>
          </Card.Body>
        </Card>
      )}

      {isLoading ? (
        <div className="flex justify-center py-12">
          <div className="animate-spin h-8 w-8 border-4 border-indigo-600 border-t-transparent rounded-full" />
        </div>
      ) : orgs?.length === 0 ? (
        <div className="text-center py-16 text-gray-400">
          <p className="text-lg font-medium">No organizations yet</p>
          <p className="text-sm mt-1">Create one to get started</p>
        </div>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {orgs?.map((org) => (
            <Card key={org.org_id} className="hover:shadow-md transition-shadow">
              <Card.Body>
                <div className="flex justify-between items-start">
                  <div>
                    <h3 className="font-semibold text-gray-900">{org.name}</h3>
                    {org.description && (
                      <p className="text-sm text-gray-500 mt-1 line-clamp-2">{org.description}</p>
                    )}
                    <span className="inline-block mt-2 text-xs font-medium bg-indigo-50 text-indigo-700 px-2 py-0.5 rounded-full capitalize">
                      {org.role}
                    </span>
                  </div>
                </div>
                <div className="mt-4 flex gap-2">
                  <Link
                    to={`/organization/${org.org_id}`}
                    className="text-sm text-indigo-600 hover:text-indigo-500 font-medium"
                  >
                    View →
                  </Link>
                  {(org.role === 'owner') && (
                    <button
                      onClick={() => deleteOrg.mutate(org.org_id)}
                      className="text-sm text-red-500 hover:text-red-700 ml-auto"
                    >
                      Delete
                    </button>
                  )}
                </div>
              </Card.Body>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}
