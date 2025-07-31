import { useQuery } from 'react-query'
import { 
  UsersIcon, 
  CurrencyDollarIcon, 
  MegaphoneIcon,
  ExclamationTriangleIcon,
  TrendingUpIcon,
  TrendingDownIcon
} from '@heroicons/react/24/outline'
import { analyticsApi, customerApi, campaignApi } from '../services/api'
import LoadingSpinner from '../components/LoadingSpinner'
import { formatCurrency, formatNumber, formatPercentage } from '../utils/formatters'

const Dashboard = () => {
  // Fetch dashboard data
  const { data: dashboardMetrics, isLoading: metricsLoading } = useQuery(
    'dashboard-metrics',
    analyticsApi.getDashboardMetrics,
    { refetchInterval: 30000 } // Refresh every 30 seconds
  )

  const { data: customerMetrics, isLoading: customerLoading } = useQuery(
    'customer-metrics',
    customerApi.getCustomerMetrics,
    { refetchInterval: 60000 }
  )

  const { data: campaignMetrics, isLoading: campaignLoading } = useQuery(
    'campaign-metrics',
    campaignApi.getCampaignMetrics,
    { refetchInterval: 60000 }
  )

  if (metricsLoading || customerLoading || campaignLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <LoadingSpinner size="lg" />
      </div>
    )
  }

  const kpiCards = [
    {
      title: 'Total Customers',
      value: formatNumber(customerMetrics?.total_customers || 0),
      change: dashboardMetrics?.new_customers_30d || 0,
      changeType: 'increase' as const,
      icon: UsersIcon,
      color: 'blue'
    },
    {
      title: 'Monthly ARPU',
      value: formatCurrency(dashboardMetrics?.arpu_30d || 0),
      change: dashboardMetrics?.revenue_growth_30d || 0,
      changeType: dashboardMetrics?.revenue_growth_30d >= 0 ? 'increase' as const : 'decrease' as const,
      icon: CurrencyDollarIcon,
      color: 'green'
    },
    {
      title: 'Churn Rate',
      value: formatPercentage(dashboardMetrics?.churn_rate_30d || 0),
      change: -2.1, // Mock improvement
      changeType: 'decrease' as const,
      icon: ExclamationTriangleIcon,
      color: 'red'
    },
    {
      title: 'Active Campaigns',
      value: formatNumber(campaignMetrics?.active_campaigns || 0),
      change: dashboardMetrics?.total_campaigns_30d || 0,
      changeType: 'increase' as const,
      icon: MegaphoneIcon,
      color: 'purple'
    }
  ]

  const colorClasses = {
    blue: 'bg-blue-500',
    green: 'bg-green-500',
    red: 'bg-red-500',
    purple: 'bg-purple-500'
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="mt-1 text-sm text-gray-500">
          Overview of your customer value management metrics
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {kpiCards.map((card) => (
          <div key={card.title} className="card p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className={`p-3 rounded-md ${colorClasses[card.color]}`}>
                  <card.icon className="h-6 w-6 text-white" />
                </div>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    {card.title}
                  </dt>
                  <dd className="flex items-baseline">
                    <div className="text-2xl font-semibold text-gray-900">
                      {card.value}
                    </div>
                    <div className={`ml-2 flex items-baseline text-sm font-semibold ${
                      card.changeType === 'increase' ? 'text-green-600' : 'text-red-600'
                    }`}>
                      {card.changeType === 'increase' ? (
                        <TrendingUpIcon className="self-center flex-shrink-0 h-4 w-4 text-green-500" />
                      ) : (
                        <TrendingDownIcon className="self-center flex-shrink-0 h-4 w-4 text-red-500" />
                      )}
                      <span className="ml-1">
                        {Math.abs(card.change)}
                      </span>
                    </div>
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Charts and detailed metrics */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Customer Segments Overview */}
        <div className="card p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Customer Segments</h3>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">High Value Customers</span>
              <div className="flex items-center">
                <span className="text-sm font-medium text-gray-900 mr-2">
                  {formatNumber(customerMetrics?.high_value_customers || 0)}
                </span>
                <div className="w-16 bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-green-500 h-2 rounded-full" 
                    style={{ 
                      width: `${((customerMetrics?.high_value_customers || 0) / (customerMetrics?.total_customers || 1)) * 100}%` 
                    }}
                  />
                </div>
              </div>
            </div>
            
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">At Risk Customers</span>
              <div className="flex items-center">
                <span className="text-sm font-medium text-gray-900 mr-2">
                  {formatNumber(customerMetrics?.at_risk_customers || 0)}
                </span>
                <div className="w-16 bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-red-500 h-2 rounded-full" 
                    style={{ 
                      width: `${((customerMetrics?.at_risk_customers || 0) / (customerMetrics?.total_customers || 1)) * 100}%` 
                    }}
                  />
                </div>
              </div>
            </div>
            
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Prepaid Customers</span>
              <div className="flex items-center">
                <span className="text-sm font-medium text-gray-900 mr-2">
                  {formatNumber(customerMetrics?.prepaid_customers || 0)}
                </span>
                <div className="w-16 bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-blue-500 h-2 rounded-full" 
                    style={{ 
                      width: `${((customerMetrics?.prepaid_customers || 0) / (customerMetrics?.total_customers || 1)) * 100}%` 
                    }}
                  />
                </div>
              </div>
            </div>
            
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Postpaid Customers</span>
              <div className="flex items-center">
                <span className="text-sm font-medium text-gray-900 mr-2">
                  {formatNumber(customerMetrics?.postpaid_customers || 0)}
                </span>
                <div className="w-16 bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-purple-500 h-2 rounded-full" 
                    style={{ 
                      width: `${((customerMetrics?.postpaid_customers || 0) / (customerMetrics?.total_customers || 1)) * 100}%` 
                    }}
                  />
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Campaign Performance */}
        <div className="card p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Campaign Performance</h3>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Total Campaigns</span>
              <span className="text-sm font-medium text-gray-900">
                {formatNumber(campaignMetrics?.total_campaigns || 0)}
              </span>
            </div>
            
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Messages Sent</span>
              <span className="text-sm font-medium text-gray-900">
                {formatNumber(campaignMetrics?.total_sent || 0)}
              </span>
            </div>
            
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Delivery Rate</span>
              <span className="text-sm font-medium text-green-600">
                {formatPercentage(campaignMetrics?.avg_delivery_rate || 0)}
              </span>
            </div>
            
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Conversion Rate</span>
              <span className="text-sm font-medium text-blue-600">
                {formatPercentage(campaignMetrics?.avg_conversion_rate || 0)}
              </span>
            </div>
            
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Average ROI</span>
              <span className={`text-sm font-medium ${
                (campaignMetrics?.avg_roi || 0) >= 0 ? 'text-green-600' : 'text-red-600'
              }`}>
                {formatPercentage(campaignMetrics?.avg_roi || 0)}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="card p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Recent Activity</h3>
        <div className="space-y-3">
          <div className="flex items-center space-x-3">
            <div className="w-2 h-2 bg-green-400 rounded-full"></div>
            <span className="text-sm text-gray-600">
              New campaign "Data Bundle Promotion" launched with 2,500 target customers
            </span>
            <span className="text-xs text-gray-400">2 hours ago</span>
          </div>
          
          <div className="flex items-center space-x-3">
            <div className="w-2 h-2 bg-blue-400 rounded-full"></div>
            <span className="text-sm text-gray-600">
              Segment "High Value Customers" updated with 1,247 customers
            </span>
            <span className="text-xs text-gray-400">4 hours ago</span>
          </div>
          
          <div className="flex items-center space-x-3">
            <div className="w-2 h-2 bg-yellow-400 rounded-full"></div>
            <span className="text-sm text-gray-600">
              Churn prediction model identified 156 at-risk customers
            </span>
            <span className="text-xs text-gray-400">6 hours ago</span>
          </div>
          
          <div className="flex items-center space-x-3">
            <div className="w-2 h-2 bg-purple-400 rounded-full"></div>
            <span className="text-sm text-gray-600">
              Campaign "Retention Offer" completed with 23% conversion rate
            </span>
            <span className="text-xs text-gray-400">1 day ago</span>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard