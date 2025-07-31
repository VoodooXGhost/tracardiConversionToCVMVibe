from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from datetime import datetime, timedelta
import uuid

from ..core.database import get_db
from ..schemas import (
    DashboardMetrics, ChurnAnalytics, RevenueAnalytics, 
    CampaignAnalytics, CustomerJourney
)
from ..services.analytics_service import AnalyticsService

router = APIRouter()

@router.get("/dashboard", response_model=DashboardMetrics)
async def get_dashboard_metrics(db: AsyncSession = Depends(get_db)):
    """Get main dashboard metrics"""
    service = AnalyticsService(db)
    return await service.get_dashboard_metrics()

@router.get("/churn", response_model=ChurnAnalytics)
async def get_churn_analytics(
    days: int = Query(30, ge=1, le=365),
    db: AsyncSession = Depends(get_db)
):
    """Get churn analytics"""
    service = AnalyticsService(db)
    return await service.get_churn_analytics(days)

@router.get("/revenue", response_model=RevenueAnalytics)
async def get_revenue_analytics(
    days: int = Query(30, ge=1, le=365),
    db: AsyncSession = Depends(get_db)
):
    """Get revenue analytics"""
    service = AnalyticsService(db)
    return await service.get_revenue_analytics(days)

@router.get("/campaigns", response_model=CampaignAnalytics)
async def get_campaign_analytics(
    days: int = Query(30, ge=1, le=365),
    db: AsyncSession = Depends(get_db)
):
    """Get campaign analytics"""
    service = AnalyticsService(db)
    return await service.get_campaign_analytics(days)

@router.get("/customer-journey/{customer_id}", response_model=CustomerJourney)
async def get_customer_journey(
    customer_id: uuid.UUID,
    days: int = Query(90, ge=1, le=365),
    db: AsyncSession = Depends(get_db)
):
    """Get customer journey analytics"""
    service = AnalyticsService(db)
    journey = await service.get_customer_journey(customer_id, days)
    if not journey:
        raise HTTPException(status_code=404, detail="Customer not found")
    return journey

@router.get("/cohort-analysis")
async def get_cohort_analysis(
    cohort_type: str = Query("monthly", regex="^(weekly|monthly|quarterly)$"),
    periods: int = Query(12, ge=1, le=24),
    db: AsyncSession = Depends(get_db)
):
    """Get cohort analysis"""
    service = AnalyticsService(db)
    return await service.get_cohort_analysis(cohort_type, periods)

@router.get("/segment-performance")
async def get_segment_performance(
    days: int = Query(30, ge=1, le=365),
    db: AsyncSession = Depends(get_db)
):
    """Get segment performance analytics"""
    service = AnalyticsService(db)
    return await service.get_segment_performance(days)

@router.get("/real-time-metrics")
async def get_real_time_metrics(db: AsyncSession = Depends(get_db)):
    """Get real-time metrics for WebSocket updates"""
    service = AnalyticsService(db)
    return await service.get_real_time_metrics()

@router.get("/trends")
async def get_trends(
    metric: str = Query("arpu", regex="^(arpu|churn|customers|revenue)$"),
    period: str = Query("daily", regex="^(hourly|daily|weekly|monthly)$"),
    days: int = Query(30, ge=1, le=365),
    db: AsyncSession = Depends(get_db)
):
    """Get trend data for charts"""
    service = AnalyticsService(db)
    return await service.get_trends(metric, period, days)

@router.get("/kpi-cards")
async def get_kpi_cards(db: AsyncSession = Depends(get_db)):
    """Get KPI cards for dashboard"""
    service = AnalyticsService(db)
    return await service.get_kpi_cards()

@router.get("/export/customers")
async def export_customers(
    format: str = Query("csv", regex="^(csv|excel)$"),
    segment_id: Optional[uuid.UUID] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    """Export customer data"""
    service = AnalyticsService(db)
    return await service.export_customers(format, segment_id)

@router.get("/export/campaigns")
async def export_campaigns(
    format: str = Query("csv", regex="^(csv|excel)$"),
    days: int = Query(30, ge=1, le=365),
    db: AsyncSession = Depends(get_db)
):
    """Export campaign data"""
    service = AnalyticsService(db)
    return await service.export_campaigns(format, days)