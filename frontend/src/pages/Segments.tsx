import { useState } from 'react'
import { useQuery } from 'react-query'
import { 
  MagnifyingGlassIcon, 
  PlusIcon,
  EyeIcon,
  PencilIcon,
  TrashIcon,
  ArrowPathIcon
} from '@heroicons/react/24/outline'
import { segmentApi } from '../services/api'
import LoadingSpinner from '../components/LoadingSpinner'
import { formatNumber, getRelativeTime } from '../utils/formatters'
import type { SegmentFilters } from '../types'

const Segments = () => {
  const [filters, setFilters] = useState<SegmentFilters>({
    page: 1,
    page_size: 20,
    search: '',
    is_active: undefined
  })

  const { data: segmentsData, isLoading, refetch } = useQuery(
    ['segments', filters],
    () => segmentApi.getSegments(filters),
    { keepPreviousData: true }
  )

  const handleFilterChange = (key: keyof SegmentFilters, value: string | boolean) => {
    setFilters(prev => ({
      ...prev,
      [key]: value,
      page: 1
    }))
  }

  const handlePageChange = (page: number) => {
    setFilters(prev => ({ ...prev, page }))
  }

  const handleRefreshSegment = async (segmentId: string) => {
    try {
      await segmentApi.refreshSegment(segmentId)
      refetch()
    } catch (error) {
      console.error('Error refreshing segment:', error)
    }
  }

  if (isLoading && !segmentsData) {
    return (
      <div className="flex items-center justify-center h-64">
        <LoadingSpinner size="lg" />
      </div>
    )
  }

  const segments = segmentsData?.segments || []
  const totalPages = segmentsData?.total_pages || 1
  const currentPage = segmentsData?.page || 1

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Customer Segments</h1>
          <p className="mt-1 text-sm text-gray-500">
            Create and manage customer segments for targeted campaigns
          </p>
        </div>
        <button className="btn-primary">
          <PlusIcon className="h-5 w-5 mr-2" />
          Create Segment
        </button>
      </div>

      {/* Filters */}
      <div className="card p-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* Search */}
          <div className="relative">
            <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search segments..."
              className="input pl-10"
              value={filters.search}
              onChange={(e) => handleFilterChange('search', e.target.value)}
            />
          </div>

          {/* Status */}
          <select
            className="input"
            value={filters.is_active === undefined ? '' : filters.is_active.toString()}
            onChange={(e) => handleFilterChange('is_active', e.target.value === '' ? undefined : e.target.value === 'true')}
          >
            <option value="">All Segments</option>
            <option value="true">Active</option>
            <option value="false">Inactive</option>
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
          {Math.min(currentPage * (filters.page_size || 20), segmentsData?.total || 0)} of{' '}
          {segmentsData?.total || 0} segments
        </span>
      </div>

      {/* Segments Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {segments.map((segment) => (
          <div key={segment.id} className="card p-6 hover:shadow-md transition-shadow">
            <div className="flex items-start justify-between mb-4">
              <div className="flex-1">
                <h3 className="text-lg font-medium text-gray-900 mb-1">
                  {segment.name}
                </h3>
                {segment.description && (
                  <p className="text-sm text-gray-600 mb-3">
                    {segment.description}
                  </p>
                )}
              </div>
              <div className="flex items-center space-x-1">
                <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                  segment.is_active 
                    ? 'text-green-600 bg-green-100' 
                    : 'text-gray-600 bg-gray-100'
                }`}>
                  {segment.is_active ? 'Active' : 'Inactive'}
                </span>
              </div>
            </div>

            {/* Customer Count */}
            <div className="mb-4">
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Customers</span>
                <div className="flex items-center space-x-2">
                  <span className="text-2xl font-bold text-tmcel-600">
                    {formatNumber(segment.customer_count)}
                  </span>
                  <button
                    onClick={() => handleRefreshSegment(segment.id)}
                    className="text-gray-400 hover:text-gray-600"
                    title="Refresh count"
                  >
                    <ArrowPathIcon className="h-4 w-4" />
                  </button>
                </div>
              </div>
            </div>

            {/* Conditions Preview */}
            <div className="mb-4">
              <div className="text-xs text-gray-500 mb-1">Conditions</div>
              <div className="text-sm text-gray-700">
                {Object.keys(segment.conditions).length > 0 ? (
                  <div className="space-y-1">
                    {Object.entries(segment.conditions).slice(0, 2).map(([field, condition]: [string, any]) => (
                      <div key={field} className="text-xs bg-gray-100 px-2 py-1 rounded">
                        {field} {condition.operator} {condition.value}
                      </div>
                    ))}
                    {Object.keys(segment.conditions).length > 2 && (
                      <div className="text-xs text-gray-500">
                        +{Object.keys(segment.conditions).length - 2} more conditions
                      </div>
                    )}
                  </div>
                ) : (
                  <span className="text-gray-500">No conditions set</span>
                )}
              </div>
            </div>

            {/* Metadata */}
            <div className="text-xs text-gray-500 mb-4">
              Created {getRelativeTime(segment.created_at)}
              {segment.created_by && ` by ${segment.created_by}`}
            </div>

            {/* Actions */}
            <div className="flex items-center justify-between pt-4 border-t border-gray-200">
              <button className="text-tmcel-600 hover:text-tmcel-900 inline-flex items-center text-sm">
                <EyeIcon className="h-4 w-4 mr-1" />
                View Details
              </button>
              
              <div className="flex items-center space-x-2">
                <button className="text-gray-600 hover:text-gray-900">
                  <PencilIcon className="h-4 w-4" />
                </button>
                <button className="text-red-600 hover:text-red-900">
                  <TrashIcon className="h-4 w-4" />
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Empty State */}
      {segments.length === 0 && !isLoading && (
        <div className="text-center py-12">
          <div className="mx-auto h-12 w-12 text-gray-400">
            <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
          </div>
          <h3 className="mt-2 text-sm font-medium text-gray-900">No segments found</h3>
          <p className="mt-1 text-sm text-gray-500">
            Get started by creating your first customer segment.
          </p>
          <div className="mt-6">
            <button className="btn-primary">
              <PlusIcon className="h-5 w-5 mr-2" />
              Create Segment
            </button>
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

export default Segments