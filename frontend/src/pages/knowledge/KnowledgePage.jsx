import { useParams, Link } from 'react-router-dom'
import Card from '../../components/ui/Card'

export default function KnowledgePage() {
  const { orgId } = useParams()

  return (
    <div>
      <div className="flex items-center gap-2 text-sm text-gray-500 mb-4">
        <Link to="/dashboard" className="hover:text-indigo-600">Organizations</Link>
        <span>/</span>
        <Link to={`/organization/${orgId}`} className="hover:text-indigo-600">Organization</Link>
        <span>/</span>
        <span className="text-gray-900">Knowledge Base</span>
      </div>

      <h1 className="text-2xl font-bold text-gray-900 mb-6">Knowledge Base</h1>

      <Card>
        <Card.Body>
          <div className="text-center py-12 text-gray-400">
            <p className="text-lg font-medium">Coming soon</p>
            <p className="text-sm mt-1">Knowledge base management will be available here.</p>
          </div>
        </Card.Body>
      </Card>
    </div>
  )
}
