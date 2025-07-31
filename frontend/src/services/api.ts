import axios, { AxiosResponse } from 'axios'
import toast from 'react-hot-toast'
import type {
  AuthToken,
  LoginCredentials,
  Customer,
  CustomerListResponse,
  CustomerMetrics,
  Segment,
  SegmentListResponse,
  Campaign,
  CampaignListResponse,
  CampaignMetrics,
  DashboardMetrics,
  CustomerFilters,
  SegmentFilters,
  CampaignFilters,
  CustomerEvent,
  Offer
} from '../types'

// Create axios instance
const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
})

// Request interceptor to add auth token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    } else if (error.response?.status >= 500) {
      toast.error('Server error. Please try again later.')
    } else if (error.response?.data?.detail) {
      toast.error(error.response.data.detail)
    } else if (error.message) {
      toast.error(error.message)
    }
    return Promise.reject(error)
  }
)

// Auth API
export const authApi = {
  login: async (credentials: LoginCredentials): Promise<AuthToken> => {
    const response: AxiosResponse<AuthToken> = await api.post('/auth/login', credentials)
    return response.data
  },

  getCurrentUser: async () => {
    const response = await api.get('/auth/me')
    return response.data
  },

  logout: async () => {
    await api.post('/auth/logout')
    localStorage.removeItem('access_token')
    localStorage.removeItem('user')
  }
}

// Customer API
export const customerApi = {
  getCustomers: async (filters: CustomerFilters = {}): Promise<CustomerListResponse> => {
    const response: AxiosResponse<CustomerListResponse> = await api.get('/customers', {
      params: filters
    })
    return response.data
  },

  getCustomer: async (id: string): Promise<Customer> => {
    const response: AxiosResponse<Customer> = await api.get(`/customers/${id}`)
    return response.data
  },

  getCustomerMetrics: async (): Promise<CustomerMetrics> => {
    const response: AxiosResponse<CustomerMetrics> = await api.get('/customers/metrics')
    return response.data
  },

  getCustomerEvents: async (id: string, limit = 50): Promise<{ customer_id: string; events: CustomerEvent[] }> => {
    const response = await api.get(`/customers/${id}/events`, {
      params: { limit }
    })
    return response.data
  },

  predictChurn: async (id: string) => {
    const response = await api.post(`/customers/${id}/predict-churn`)
    return response.data
  },

  getNextBestOffer: async (id: string) => {
    const response = await api.get(`/customers/${id}/next-best-offer`)
    return response.data
  },

  createCustomer: async (data: Partial<Customer>): Promise<Customer> => {
    const response: AxiosResponse<Customer> = await api.post('/customers', data)
    return response.data
  },

  updateCustomer: async (id: string, data: Partial<Customer>): Promise<Customer> => {
    const response: AxiosResponse<Customer> = await api.put(`/customers/${id}`, data)
    return response.data
  },

  deleteCustomer: async (id: string): Promise<void> => {
    await api.delete(`/customers/${id}`)
  }
}

// Segment API
export const segmentApi = {
  getSegments: async (filters: SegmentFilters = {}): Promise<SegmentListResponse> => {
    const response: AxiosResponse<SegmentListResponse> = await api.get('/segments', {
      params: filters
    })
    return response.data
  },

  getSegment: async (id: string): Promise<Segment> => {
    const response: AxiosResponse<Segment> = await api.get(`/segments/${id}`)
    return response.data
  },

  createSegment: async (data: Partial<Segment>): Promise<Segment> => {
    const response: AxiosResponse<Segment> = await api.post('/segments', data)
    return response.data
  },

  updateSegment: async (id: string, data: Partial<Segment>): Promise<Segment> => {
    const response: AxiosResponse<Segment> = await api.put(`/segments/${id}`, data)
    return response.data
  },

  deleteSegment: async (id: string): Promise<void> => {
    await api.delete(`/segments/${id}`)
  },

  previewSegment: async (conditions: Record<string, any>): Promise<{ customer_count: number }> => {
    const response = await api.post('/segments/preview', conditions)
    return response.data
  },

  refreshSegment: async (id: string): Promise<{ segment_id: string; customer_count: number }> => {
    const response = await api.post(`/segments/${id}/refresh`)
    return response.data
  },

  getSegmentCustomers: async (id: string, page = 1, page_size = 20) => {
    const response = await api.get(`/segments/${id}/customers`, {
      params: { page, page_size }
    })
    return response.data
  },

  getSegmentAnalytics: async (id: string) => {
    const response = await api.get(`/segments/${id}/analytics`)
    return response.data
  }
}

// Campaign API
export const campaignApi = {
  getCampaigns: async (filters: CampaignFilters = {}): Promise<CampaignListResponse> => {
    const response: AxiosResponse<CampaignListResponse> = await api.get('/campaigns', {
      params: filters
    })
    return response.data
  },

  getCampaign: async (id: string): Promise<Campaign> => {
    const response: AxiosResponse<Campaign> = await api.get(`/campaigns/${id}`)
    return response.data
  },

  getCampaignMetrics: async (): Promise<CampaignMetrics> => {
    const response: AxiosResponse<CampaignMetrics> = await api.get('/campaigns/metrics')
    return response.data
  },

  createCampaign: async (data: Partial<Campaign>): Promise<Campaign> => {
    const response: AxiosResponse<Campaign> = await api.post('/campaigns', data)
    return response.data
  },

  updateCampaign: async (id: string, data: Partial<Campaign>): Promise<Campaign> => {
    const response: AxiosResponse<Campaign> = await api.put(`/campaigns/${id}`, data)
    return response.data
  },

  deleteCampaign: async (id: string): Promise<void> => {
    await api.delete(`/campaigns/${id}`)
  },

  launchCampaign: async (id: string): Promise<{ message: string; campaign_id: string }> => {
    const response = await api.post(`/campaigns/${id}/launch`)
    return response.data
  },

  pauseCampaign: async (id: string): Promise<{ message: string; campaign_id: string }> => {
    const response = await api.post(`/campaigns/${id}/pause`)
    return response.data
  },

  resumeCampaign: async (id: string): Promise<{ message: string; campaign_id: string }> => {
    const response = await api.post(`/campaigns/${id}/resume`)
    return response.data
  },

  getCampaignInteractions: async (id: string, page = 1, page_size = 50, interaction_type?: string) => {
    const response = await api.get(`/campaigns/${id}/interactions`, {
      params: { page, page_size, interaction_type }
    })
    return response.data
  },

  getCampaignPerformance: async (id: string) => {
    const response = await api.get(`/campaigns/${id}/performance`)
    return response.data
  },

  testCampaign: async (id: string, phone_numbers: string[]) => {
    const response = await api.post(`/campaigns/${id}/test`, { test_phone_numbers: phone_numbers })
    return response.data
  }
}

// Analytics API
export const analyticsApi = {
  getDashboardMetrics: async (): Promise<DashboardMetrics> => {
    const response: AxiosResponse<DashboardMetrics> = await api.get('/analytics/dashboard')
    return response.data
  },

  getChurnAnalytics: async (days = 30) => {
    const response = await api.get('/analytics/churn', {
      params: { days }
    })
    return response.data
  },

  getRevenueAnalytics: async (days = 30) => {
    const response = await api.get('/analytics/revenue', {
      params: { days }
    })
    return response.data
  },

  getCampaignAnalytics: async (days = 30) => {
    const response = await api.get('/analytics/campaigns', {
      params: { days }
    })
    return response.data
  },

  getCustomerJourney: async (customerId: string, days = 90) => {
    const response = await api.get(`/analytics/customer-journey/${customerId}`, {
      params: { days }
    })
    return response.data
  },

  getCohortAnalysis: async (cohort_type = 'monthly', periods = 12) => {
    const response = await api.get('/analytics/cohort-analysis', {
      params: { cohort_type, periods }
    })
    return response.data
  },

  getSegmentPerformance: async (days = 30) => {
    const response = await api.get('/analytics/segment-performance', {
      params: { days }
    })
    return response.data
  },

  getRealTimeMetrics: async () => {
    const response = await api.get('/analytics/real-time-metrics')
    return response.data
  },

  getTrends: async (metric = 'arpu', period = 'daily', days = 30) => {
    const response = await api.get('/analytics/trends', {
      params: { metric, period, days }
    })
    return response.data
  },

  getKPICards: async () => {
    const response = await api.get('/analytics/kpi-cards')
    return response.data
  }
}

// Offer API
export const offerApi = {
  getOffers: async (filters: any = {}) => {
    const response = await api.get('/offers', {
      params: filters
    })
    return response.data
  },

  getOffer: async (id: string): Promise<Offer> => {
    const response: AxiosResponse<Offer> = await api.get(`/offers/${id}`)
    return response.data
  },

  createOffer: async (data: Partial<Offer>): Promise<Offer> => {
    const response: AxiosResponse<Offer> = await api.post('/offers', data)
    return response.data
  },

  updateOffer: async (id: string, data: Partial<Offer>): Promise<Offer> => {
    const response: AxiosResponse<Offer> = await api.put(`/offers/${id}`, data)
    return response.data
  },

  deleteOffer: async (id: string): Promise<void> => {
    await api.delete(`/offers/${id}`)
  },

  getOfferTypes: async () => {
    const response = await api.get('/offers/types/available')
    return response.data
  },

  getOfferPerformance: async (id: string, days = 30) => {
    const response = await api.get(`/offers/${id}/performance`, {
      params: { days }
    })
    return response.data
  }
}

export default api