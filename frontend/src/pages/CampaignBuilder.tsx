const CampaignBuilder = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Campaign Builder</h1>
        <p className="mt-1 text-sm text-gray-500">
          Create a new marketing campaign
        </p>
      </div>
      
      <div className="card p-6">
        <p className="text-gray-600">
          Campaign builder with drag-and-drop interface is under development. This will include:
        </p>
        <ul className="mt-4 space-y-2 text-gray-600">
          <li>• Visual campaign flow designer</li>
          <li>• Segment selection and targeting</li>
          <li>• Message template editor</li>
          <li>• A/B testing configuration</li>
          <li>• Scheduling and automation rules</li>
        </ul>
      </div>
    </div>
  )
}

export default CampaignBuilder