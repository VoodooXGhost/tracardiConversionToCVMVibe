import { useParams } from 'react-router-dom'

const CampaignDetail = () => {
  const { id } = useParams<{ id: string }>()

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Campaign Detail</h1>
        <p className="mt-1 text-sm text-gray-500">
          Campaign ID: {id}
        </p>
      </div>
      
      <div className="card p-6">
        <p className="text-gray-600">
          Campaign detail page is under development. This will show comprehensive campaign analytics, 
          performance metrics, and interaction details.
        </p>
      </div>
    </div>
  )
}

export default CampaignDetail