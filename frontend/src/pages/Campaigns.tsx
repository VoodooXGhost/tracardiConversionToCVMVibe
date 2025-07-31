import { useState } from 'react'
import { useQuery } from 'react-query'
import { Link } from 'react-router-dom'
import { 
  MagnifyingGlassIcon, 
  PlusIcon,
  EyeIcon,
  PlayIcon,
  PauseIcon,
  StopIcon
} from '@heroicons/react/24/outline'
import { campaignApi } from '../services/api'
import LoadingSpinner from '../components/LoadingSpinner'
import { 
  formatCurrency, 
  formatNumber, 
  formatPercentage,
  formatStatus,
  getRelativeTime
} from '../utils/formatters'
import type { CampaignFilters } from '../types'

const Campaigns = () => {
  const [filters, setFilters] = useState<CampaignFilters>({
    page: 1,
    page_size: 20,
    search: '',
    status: '',
    campaign_type: ''
  })

  const { data: campaignsData, isLoading, refetch } = useQuery(
    ['campaigns', filters],
    () => campaignApi.getCampaigns(filters),
    { keepPreviousData: true }
  )

  const handleFilterChange = (key: keyof CampaignFilters, value: string) => {
    setFilters(prev => ({
      ...prev,
      [key]: value,
      page: 1
    }))
  }

  const handlePageChange = (page: number) => {
    setFilters(prev => ({ ...prev, page }))
  }

  const handleCampaignAction = async (campaignId: string, action: 'launch' | 'pause' | 'resume') => {
    try {
      switch (action) {
        case 'launch':
          await campaignApi.launchCampaign(campaignId)
          break
        case 'pause':
          await campaignApi.pauseCampaign(campaignId)
          break
        case 'resume':
          await campaignApi.resumeCampaign(campaignId)
          break
      }
      refetch()
    } catch (error) {
      console.error(`Error ${action}ing campaign:`, error)
    }
  }

  if (isLoading && !campaignsData) {
    return (
      <div className="flex items-center justify-center h-64">
        <LoadingSpinner size="lg" />
      </div>
    )
  }

  const campaigns = campaignsData?.campaigns || []
  const totalPages = campaignsData?.total_pages || 1
  const currentPage = campaignsData?.page || 1

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Campaigns</h1>
          <p className="mt-1 text-sm text-gray-500">
            Create and manage marketing campaigns
          </p>
        </div>
        <Link to="/campaigns/new" className="btn-primary">
          <PlusIcon className="h-5 w-5 mr-2" />
          Create Campaign
        </Link>
      </div>

      {/* Filters */}
      <div className="card p-4">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          {/* Search */}
          <div className="relative">
            <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search campaigns..."
              className="input pl-10"
              value={filters.search}
              onChange={(e) => handleFilterChange('search', e.target.value)}
            />
          </div>

          {/* Status */}
          <select
            className="input"
            value={filters.status}
            onChange={(e) => handleFilterChange('status', e.target.value)}
          >
            <option value="">All Status</option>
            <option value="draft">Draft</option>
            <option value="scheduled">Scheduled</option>
            <option value="running">Running</option>
            <option value="completed">Completed</option>
            <option value="paused">Paused</option>
          </select>

          {/* Campaign Type */}
          <select
            className="input"
            value={filters.campaign_type}
            onChange={(e) => handleFilterChange('campaign_type', e.target.value)}
          >
            <option value="">All Types</option>
            <option value="sms">SMS</option>
            <option value="email">Email</option>
            <option value="push">Push Notification</option>
          </select>

          {/* Filter Button */}
          <button
            onClick={() => refetch()}
            className="btn-secondary"
          >
            <MagnifyingGlassIcon className="h-5 w-5 mr-2" />
            Search
          </button>
        </div>
      </div>

      {/* Results Summary */}
      <div className="flex items-center justify-between text-sm text-gray-500">
        <span>
          Showing {((currentPage - 1) * (filters.page_size || 20)) + 1} to{' '}
          {Math.min(currentPage * (filters.page_size || 20), campaignsData?.total || 0)} of{' '}
          {campaignsData?.total || 0} campaigns
        </span>
      </div>

      {/* Campaigns Table */}
      <div className="card overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Campaign
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Type
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Target/Sent
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Performance
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  ROI
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Created
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {campaigns.map((campaign) => {
                const status = formatStatus(campaign.status)

                return (
                  <tr key={campaign.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div>
                        <div className="text-sm font-medium text-gray-900">
                          {campaign.name}
                        </div>
                        {campaign.description && (
                          <div className="text-sm text-gray-500 truncate max-w-xs">
                            {campaign.description}
                          </div>
                        )}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="inline-flex px-2 py-1 text-xs font-semibold rounded-full bg-blue-100 text-blue-800">
                        {campaign.campaign_type.toUpperCase()}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${status.color}`}>
                        {status.text}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      <div>
                        <div>{formatNumber(campaign.sent_count)} / {formatNumber(campaign.target_count)}</div>
                        <div className="text-xs text-gray-500">
                          {formatPercentage(campaign.delivery_rate)} delivered
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      <div className="space-y-1">
                        <div className="flex justify-between">
                          <span className="text-xs text-gray-500">Open:</span>
                          <span className="text-xs">{formatPercentage(campaign.open_rate)}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-xs text-gray-500">Convert:</span>
                          <span className="text-xs">{formatPercentage(campaign.conversion_rate)}</span>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm">
                      <div>
                        <div className={`font-medium ${
                          campaign.roi_percentage >= 0 ? 'text-green-600' : 'text-red-600'
                        }`}>
                          {formatPercentage(campaign.roi_percentage / 100)}
                        </div>
                        <div className="text-xs text-gray-500">
                          {formatCurrency(campaign.revenue_generated)}
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {getRelativeTime(campaign.created_at)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <div className="flex items-center space-x-2">
                        <Link
                          to={`/campaigns/${campaign.id}`}
                          className="text-tmcel-600 hover:text-tmcel-900"
                        >
                          <EyeIcon className="h-4 w-4" />
                        </Link>
                        
                        {campaign.status === 'draft' && (
                          <button
                            onClick={() => handleCampaignAction(campaign.id, 'launch')}
                            className="text-green-600 hover:text-green-900"
                            title="Launch Campaign"
                          >
                            <PlayIcon className="h-4 w-4" />
                          </button>
                        )}
                        
                        {campaign.status === 'running' && (
                          <button
                            onClick={() => handleCampaignAction(campaign.id, 'pause')}
                            className="text-yellow-600 hover:text-yellow-900"
                            title="Pause Campaign"
                          >
                            <PauseIcon className="h-4 w-4" />
                          </button>
                        )}
                        
                        {campaign.status === 'paused' && (
                          <button
                            onClick={() => handleCampaignAction(campaign.id, 'resume')}
                            className="text-green-600 hover:text-green-900"
                            title="Resume Campaign"
                          >
                            <PlayIcon className="h-4 w-4" />
                          </button>
                        )}
                      </div>
                    </td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>
      </div>

      {/* Empty State */}
      {campaigns.length === 0 && !isLoading && (
        <div className="text-center py-12">
          <div className="mx-auto h-12 w-12 text-gray-400">
            <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M11 5.882V19.24a1.76 1.76 0 01-3.417.592l-2.147-6.15M18 13a3 3 0 100-6M5.436 13.683A4.001 4.001 0 017 6h1.832c4.1 0 7.625-1.234 9.168-3v14c-1.543-1.766-5.067-3-9.168-3H7a3.988 3.988 0 01-1.564-.317z" />
            </svg>
          </div>
          <h3 className="mt-2 text-sm font-medium text-gray-900">No campaigns found</h3>
          <p className="mt-1 text-sm text-gray-500">
            Get started by creating your first marketing campaign.
          </p>
          <div className="mt-6">
            <Link to="/campaigns/new" className="btn-primary">
              <PlusIcon className="h-5 w-5 mr-2" />
              Create Campaign
            </Link>
          </div>
        </div>
      )}

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <button
              onClick={() => handlePageChange(currentPage - 1)}
              disabled={currentPage === 1}
              className="btn-secondary disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Previous
            </button>
            
            <div className="flex items-center space-x-1">
              {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
                const page = i + 1
                return (
                  <button
                    key={page}
                    onClick={() => handlePageChange(page)}
                    className={`px-3 py-2 text-sm font-medium rounded-md ${
                      page === currentPage
                        ? 'bg-tmcel-600 text-white'
                        : 'text-gray-700 hover:bg-gray-100'
                    }`}
                  >
                    {page}
                  </button>
                )
              })}
            </div>

            <button
              onClick={() => handlePageChange(currentPage + 1)}
              disabled={currentPage === totalPages}
              className="btn-secondary disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Next
            </button>
          </div>

          <div className="text-sm text-gray-500">
            Page {currentPage} of {totalPages}
          </div>
        </div>
      )}
    </div>
  )
}

export default Campaigns