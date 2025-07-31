import { useParams } from 'react-router-dom'
import { useQuery } from 'react-query'
import { 
  PhoneIcon, 
  EnvelopeIcon, 
  MapPinIcon,
  DevicePhoneMobileIcon,
  ExclamationTriangleIcon,
  CurrencyDollarIcon,
  ClockIcon,
  ChartBarIcon
} from '@heroicons/react/24/outline'
import { customerApi } from '../services/api'
import LoadingSpinner from '../components/LoadingSpinner'
import { 
  formatCurrency, 
  formatPhoneNumber, 
  formatRiskLevel, 
  formatCustomerType,
  formatStatus,
  formatDate,
  formatDataSize,
  formatDuration,
  getRelativeTime
} from '../utils/formatters'

const CustomerDetail = () => {
  const { id } = useParams<{ id: string }>()

  const { data: customer, isLoading: customerLoading } = useQuery(
    ['customer', id],
    () => customerApi.getCustomer(id!),
    { enabled: !!id }
  )

  const { data: eventsData, isLoading: eventsLoading } = useQuery(
    ['customer-events', id],
    () => customerApi.getCustomerEvents(id!, 20),
    { enabled: !!id }
  )

  const { data: churnPrediction } = useQuery(
    ['customer-churn', id],
    () => customerApi.predictChurn(id!),
    { enabled: !!id }
  )

  const { data: nextBestOffer } = useQuery(
    ['customer-nbo', id],
    () => customerApi.getNextBestOffer(id!),
    { enabled: !!id }
  )

  if (customerLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <LoadingSpinner size="lg" />
      </div>
    )
  }

  if (!customer) {
    return (
      <div className="text-center py-12">
        <h2 className="text-2xl font-bold text-gray-900">Customer not found</h2>
        <p className="mt-2 text-gray-600">The customer you're looking for doesn't exist.</p>
      </div>
    )
  }

  const riskLevel = formatRiskLevel(customer.risk_level)
  const customerType = formatCustomerType(customer.customer_type)
  const status = formatStatus(customer.status)

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">
            {customer.full_name || 'Unknown Customer'}
          </h1>
          <p className="mt-1 text-sm text-gray-500">
            Customer ID: {customer.id}
          </p>
        </div>
        <div className="flex items-center space-x-3">
          <span className={`inline-flex px-3 py-1 text-sm font-semibold rounded-full ${status.color}`}>
            {status.text}
          </span>
          <span className={`inline-flex px-3 py-1 text-sm font-semibold rounded-full ${riskLevel.color}`}>
            {riskLevel.text}
          </span>
        </div>
      </div>

      {/* Customer Overview */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Basic Information */}
        <div className="card p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Basic Information</h3>
          <div className="space-y-4">
            <div className="flex items-center">
              <PhoneIcon className="h-5 w-5 text-gray-400 mr-3" />
              <div>
                <div className="text-sm font-medium text-gray-900">
                  {formatPhoneNumber(customer.phone_number)}
                </div>
                <div className="text-xs text-gray-500">Phone Number</div>
              </div>
            </div>

            {customer.email && (
              <div className="flex items-center">
                <EnvelopeIcon className="h-5 w-5 text-gray-400 mr-3" />
                <div>
                  <div className="text-sm font-medium text-gray-900">{customer.email}</div>
                  <div className="text-xs text-gray-500">Email</div>
                </div>
              </div>
            )}

            <div className="flex items-center">
              <MapPinIcon className="h-5 w-5 text-gray-400 mr-3" />
              <div>
                <div className="text-sm font-medium text-gray-900">
                  {customer.city}, {customer.province}
                </div>
                <div className="text-xs text-gray-500">Location</div>
              </div>
            </div>

            <div className="flex items-center">
              <DevicePhoneMobileIcon className="h-5 w-5 text-gray-400 mr-3" />
              <div>
                <div className="text-sm font-medium text-gray-900">
                  {customer.primary_device_brand} {customer.primary_device_model}
                </div>
                <div className="text-xs text-gray-500">Device</div>
              </div>
            </div>

            <div className="pt-4 border-t">
              <div className="text-xs text-gray-500 mb-1">Customer Type</div>
              <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${customerType.color}`}>
                {customerType.text}
              </span>
            </div>
          </div>
        </div>

        {/* Financial Metrics */}
        <div className="card p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Financial Metrics</h3>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Current Balance</span>
              <span className="text-sm font-medium text-gray-900">
                {formatCurrency(customer.current_balance)}
              </span>
            </div>

            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">ARPU (30d)</span>
              <span className="text-sm font-medium text-gray-900">
                {formatCurrency(customer.arpu_30d)}
              </span>
            </div>

            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">ARPU (90d)</span>
              <span className="text-sm font-medium text-gray-900">
                {formatCurrency(customer.arpu_90d)}
              </span>
            </div>

            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Total Revenue</span>
              <span className="text-sm font-medium text-gray-900">
                {formatCurrency(customer.total_revenue)}
              </span>
            </div>

            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Lifetime Value</span>
              <span className="text-sm font-medium text-gray-900">
                {formatCurrency(customer.lifetime_value)}
              </span>
            </div>

            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Total Recharges</span>
              <span className="text-sm font-medium text-gray-900">
                {customer.total_recharges}
              </span>
            </div>

            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Avg Recharge</span>
              <span className="text-sm font-medium text-gray-900">
                {formatCurrency(customer.avg_recharge_amount)}
              </span>
            </div>
          </div>
        </div>

        {/* Usage Metrics */}
        <div className="card p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Usage Metrics</h3>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Voice Minutes</span>
              <span className="text-sm font-medium text-gray-900">
                {customer.total_voice_minutes.toLocaleString()}
              </span>
            </div>

            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">SMS Sent</span>
              <span className="text-sm font-medium text-gray-900">
                {customer.total_sms_sent.toLocaleString()}
              </span>
            </div>

            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Data Usage</span>
              <span className="text-sm font-medium text-gray-900">
                {formatDataSize(customer.total_data_mb * 1024 * 1024)}
              </span>
            </div>

            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Days Since Activity</span>
              <span className="text-sm font-medium text-gray-900">
                {customer.days_since_last_activity} days
              </span>
            </div>

            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Last Activity</span>
              <span className="text-sm font-medium text-gray-900">
                {formatDate(customer.last_activity_at)}
              </span>
            </div>

            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Customer Since</span>
              <span className="text-sm font-medium text-gray-900">
                {formatDate(customer.activation_date)}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* AI Insights */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Churn Prediction */}
        {churnPrediction && (
          <div className="card p-6">
            <div className="flex items-center mb-4">
              <ExclamationTriangleIcon className="h-6 w-6 text-red-500 mr-2" />
              <h3 className="text-lg font-medium text-gray-900">Churn Prediction</h3>
            </div>
            
            <div className="space-y-4">
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm text-gray-600">Churn Probability</span>
                  <span className="text-lg font-bold text-red-600">
                    {(churnPrediction.churn_probability * 100).toFixed(1)}%
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-red-500 h-2 rounded-full" 
                    style={{ width: `${churnPrediction.churn_probability * 100}%` }}
                  />
                </div>
              </div>

              {churnPrediction.factors && churnPrediction.factors.length > 0 && (
                <div>
                  <h4 className="text-sm font-medium text-gray-900 mb-2">Risk Factors</h4>
                  <div className="space-y-2">
                    {churnPrediction.factors.map((factor: any, index: number) => (
                      <div key={index} className="text-sm">
                        <div className="font-medium text-gray-900">{factor.factor}</div>
                        <div className="text-gray-600">{factor.description}</div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {churnPrediction.recommendations && churnPrediction.recommendations.length > 0 && (
                <div>
                  <h4 className="text-sm font-medium text-gray-900 mb-2">Recommendations</h4>
                  <div className="space-y-2">
                    {churnPrediction.recommendations.map((rec: any, index: number) => (
                      <div key={index} className="text-sm">
                        <div className="font-medium text-green-700">{rec.action}</div>
                        <div className="text-gray-600">{rec.description}</div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Next Best Offer */}
        {nextBestOffer && (
          <div className="card p-6">
            <div className="flex items-center mb-4">
              <CurrencyDollarIcon className="h-6 w-6 text-green-500 mr-2" />
              <h3 className="text-lg font-medium text-gray-900">Next Best Offer</h3>
            </div>
            
            <div className="space-y-4">
              <div>
                <h4 className="text-lg font-medium text-gray-900">{nextBestOffer.offer.name}</h4>
                <p className="text-sm text-gray-600">{nextBestOffer.offer.description}</p>
              </div>

              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Price</span>
                <span className="text-lg font-bold text-green-600">
                  {formatCurrency(nextBestOffer.offer.price)}
                </span>
              </div>

              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Confidence Score</span>
                <span className="text-sm font-medium text-gray-900">
                  {(nextBestOffer.confidence_score * 100).toFixed(0)}%
                </span>
              </div>

              {nextBestOffer.reasoning && nextBestOffer.reasoning.length > 0 && (
                <div>
                  <h4 className="text-sm font-medium text-gray-900 mb-2">Why this offer?</h4>
                  <ul className="text-sm text-gray-600 space-y-1">
                    {nextBestOffer.reasoning.map((reason: string, index: number) => (
                      <li key={index}>• {reason}</li>
                    ))}
                  </ul>
                </div>
              )}

              <button className="w-full btn-primary">
                Send Offer
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Recent Activity */}
      <div className="card p-6">
        <div className="flex items-center mb-4">
          <ClockIcon className="h-6 w-6 text-blue-500 mr-2" />
          <h3 className="text-lg font-medium text-gray-900">Recent Activity</h3>
        </div>

        {eventsLoading ? (
          <div className="flex items-center justify-center py-8">
            <LoadingSpinner />
          </div>
        ) : eventsData?.events && eventsData.events.length > 0 ? (
          <div className="space-y-4">
            {eventsData.events.slice(0, 10).map((event) => (
              <div key={event.id} className="flex items-center space-x-4 py-3 border-b border-gray-100 last:border-b-0">
                <div className="flex-shrink-0">
                  <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                    <ChartBarIcon className="h-4 w-4 text-blue-600" />
                  </div>
                </div>
                <div className="flex-1 min-w-0">
                  <div className="text-sm font-medium text-gray-900">{event.event_name}</div>
                  <div className="text-sm text-gray-500">
                    {event.channel && `via ${event.channel}`}
                    {event.amount && ` • ${formatCurrency(event.amount)}`}
                    {event.duration && ` • ${formatDuration(event.duration)}`}
                    {event.data_volume_mb && ` • ${formatDataSize(event.data_volume_mb * 1024 * 1024)}`}
                  </div>
                </div>
                <div className="text-sm text-gray-500">
                  {getRelativeTime(event.occurred_at)}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-8 text-gray-500">
            No recent activity found
          </div>
        )}
      </div>
    </div>
  )
}

export default CustomerDetail