from pydantic import BaseModel, ConfigDict
from typing import List, Dict, Any, Optional
from datetime import datetime
from decimal import Decimal

class DashboardMetrics(BaseModel):
    # Customer metrics
    total_customers: int
    active_customers: int
    new_customers_30d: int
    churned_customers_30d: int
    churn_rate_30d: float
    
    # Revenue metrics
    total_revenue: Decimal
    arpu_30d: Decimal
    revenue_growth_30d: float
    
    # Campaign metrics
    active_campaigns: int
    total_campaigns_30d: int
    avg_campaign_roi: float
    
    # Engagement metrics
    avg_days_since_activity: float
    high_value_customers: int
    at_risk_customers: int

class ChurnAnalytics(BaseModel):
    overall_churn_rate: float
    churn_by_customer_type: Dict[str, float]
    churn_by_province: Dict[str, float]
    churn_by_device_type: Dict[str, float]
    high_risk_customers: int
    medium_risk_customers: int
    low_risk_customers: int
    churn_trend_30d: List[Dict[str, Any]]  # Daily churn rates

class RevenueAnalytics(BaseModel):
    total_revenue: Decimal
    revenue_by_customer_type: Dict[str, Decimal]
    revenue_by_province: Dict[str, Decimal]
    arpu_distribution: Dict[str, int]  # ARPU ranges and customer counts
    revenue_trend_30d: List[Dict[str, Any]]  # Daily revenue
    top_revenue_customers: List[Dict[str, Any]]

class CampaignAnalytics(BaseModel):
    total_campaigns: int
    campaign_performance: List[Dict[str, Any]]
    channel_performance: Dict[str, Dict[str, Any]]
    roi_by_campaign_type: Dict[str, float]
    conversion_funnel: Dict[str, int]
    best_performing_campaigns: List[Dict[str, Any]]

class CustomerJourney(BaseModel):
    customer_id: str
    journey_stages: List[Dict[str, Any]]
    total_events: int
    journey_duration_days: int
    conversion_events: List[Dict[str, Any]]
    churn_indicators: List[Dict[str, Any]]

class SegmentAnalytics(BaseModel):
    segment_id: str
    segment_name: str
    customer_count: int
    avg_arpu: Decimal
    avg_churn_score: float
    conversion_rate: float
    revenue_contribution: Decimal

class TimeSeriesData(BaseModel):
    date: datetime
    value: float
    label: Optional[str] = None

class ChartData(BaseModel):
    labels: List[str]
    datasets: List[Dict[str, Any]]

class KPICard(BaseModel):
    title: str
    value: str
    change: Optional[float] = None
    change_type: Optional[str] = None  # "increase", "decrease", "neutral"
    format_type: str = "number"  # "number", "currency", "percentage"