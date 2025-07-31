// API Response Types
export interface ApiResponse<T> {
  data?: T
  message?: string
  error?: string
}

// User and Authentication
export interface User {
  id: string
  username: string
  email: string
  full_name: string
  role: string
  is_active: boolean
  last_login?: string
  created_at: string
  updated_at: string
}

export interface LoginCredentials {
  username: string
  password: string
}

export interface AuthToken {
  access_token: string
  token_type: string
  expires_in: number
  user: User
}

// Customer Types
export interface Customer {
  id: string
  phone_number: string
  email?: string
  first_name?: string
  last_name?: string
  date_of_birth?: string
  gender?: string
  customer_type: 'prepaid' | 'postpaid'
  activation_date: string
  status: 'active' | 'suspended' | 'churned'
  province?: string
  city?: string
  current_balance: number
  arpu_30d: number
  arpu_90d: number
  total_revenue: number
  total_voice_minutes: number
  total_sms_sent: number
  total_data_mb: number
  days_since_last_activity: number
  total_recharges: number
  avg_recharge_amount: number
  primary_device_brand?: string
  primary_device_model?: string
  device_type?: string
  churn_score: number
  lifetime_value: number
  next_best_offer_id?: string
  created_at: string
  updated_at: string
  last_activity_at: string
  full_name?: string
  is_high_value: boolean
  is_at_risk: boolean
  risk_level: 'low' | 'medium' | 'high' | 'unknown'
}

export interface CustomerSummary {
  id: string
  phone_number: string
  full_name?: string
  customer_type: 'prepaid' | 'postpaid'
  status: string
  arpu_30d: number
  churn_score: number
  days_since_last_activity: number
  risk_level: string
  created_at: string
  last_activity_at: string
}

export interface CustomerListResponse {
  customers: CustomerSummary[]
  total: number
  page: number
  page_size: number
  total_pages: number
}

export interface CustomerMetrics {
  total_customers: number
  active_customers: number
  churned_customers: number
  high_value_customers: number
  at_risk_customers: number
  avg_arpu: number
  avg_churn_score: number
  prepaid_customers: number
  postpaid_customers: number
}

// Segment Types
export interface SegmentCondition {
  field: string
  operator: string
  value: any
}

export interface Segment {
  id: string
  name: string
  description?: string
  conditions: Record<string, any>
  is_active: boolean
  customer_count: number
  created_by?: string
  created_at: string
  updated_at: string
}

export interface SegmentListResponse {
  segments: Segment[]
  total: number
  page: number
  page_size: number
  total_pages: number
}

// Campaign Types
export interface Campaign {
  id: string
  name: string
  description?: string
  campaign_type: string
  message_template: string
  target_segment_id?: string
  status: 'draft' | 'scheduled' | 'running' | 'completed' | 'paused'
  scheduled_at?: string
  started_at?: string
  completed_at?: string
  target_count: number
  sent_count: number
  delivered_count: number
  opened_count: number
  clicked_count: number
  converted_count: number
  budget?: number
  cost_per_message?: number
  total_cost: number
  revenue_generated: number
  delivery_rate: number
  open_rate: number
  click_rate: number
  conversion_rate: number
  roi_percentage: number
  created_by?: string
  created_at: string
  updated_at: string
}

export interface CampaignListResponse {
  campaigns: Campaign[]
  total: number
  page: number
  page_size: number
  total_pages: number
}

export interface CampaignMetrics {
  total_campaigns: number
  active_campaigns: number
  completed_campaigns: number
  total_sent: number
  total_delivered: number
  total_opened: number
  total_clicked: number
  total_converted: number
  avg_delivery_rate: number
  avg_open_rate: number
  avg_click_rate: number
  avg_conversion_rate: number
  total_cost: number
  total_revenue: number
  avg_roi: number
}

// Analytics Types
export interface DashboardMetrics {
  total_customers: number
  active_customers: number
  new_customers_30d: number
  churned_customers_30d: number
  churn_rate_30d: number
  total_revenue: number
  arpu_30d: number
  revenue_growth_30d: number
  active_campaigns: number
  total_campaigns_30d: number
  avg_campaign_roi: number
  avg_days_since_activity: number
  high_value_customers: number
  at_risk_customers: number
}

export interface ChartData {
  labels: string[]
  datasets: Array<{
    label: string
    data: number[]
    backgroundColor?: string
    borderColor?: string
    fill?: boolean
  }>
}

export interface KPICard {
  title: string
  value: string
  change?: number
  change_type?: 'increase' | 'decrease' | 'neutral'
  format_type: 'number' | 'currency' | 'percentage'
}

// Event Types
export interface CustomerEvent {
  id: string
  event_type: string
  event_name: string
  amount?: number
  duration?: number
  data_volume_mb?: number
  channel?: string
  occurred_at: string
  properties?: Record<string, any>
}

// Offer Types
export interface Offer {
  id: string
  name: string
  description?: string
  offer_type: string
  price: number
  value?: number
  validity_days?: number
  data_mb?: number
  voice_minutes?: number
  sms_count?: number
  discount_percentage?: number
  is_active: boolean
  valid_from: string
  valid_until?: string
  created_at: string
  updated_at: string
  is_valid: boolean
}

// Pagination
export interface PaginationParams {
  page?: number
  page_size?: number
  search?: string
}

// Filter Types
export interface CustomerFilters extends PaginationParams {
  customer_type?: string
  status?: string
  risk_level?: string
}

export interface SegmentFilters extends PaginationParams {
  is_active?: boolean
}

export interface CampaignFilters extends PaginationParams {
  status?: string
  campaign_type?: string
}

// WebSocket Message Types
export interface WebSocketMessage {
  type: string
  timestamp: number
  data: any
}