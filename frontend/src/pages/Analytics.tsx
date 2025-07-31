const Analytics = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Analytics</h1>
        <p className="mt-1 text-sm text-gray-500">
          Advanced analytics and reporting
        </p>
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Churn Analytics</h3>
          <p className="text-gray-600">
            Advanced churn prediction analytics, risk factor analysis, and retention insights.
          </p>
        </div>
        
        <div className="card p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Revenue Analytics</h3>
          <p className="text-gray-600">
            Revenue trends, ARPU analysis, and customer lifetime value insights.
          </p>
        </div>
        
        <div className="card p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Campaign Analytics</h3>
          <p className="text-gray-600">
            Campaign performance analysis, conversion funnels, and ROI tracking.
          </p>
        </div>
        
        <div className="card p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Customer Journey</h3>
          <p className="text-gray-600">
            Customer journey mapping, touchpoint analysis, and behavior patterns.
          </p>
        </div>
      </div>
    </div>
  )
}

export default Analytics