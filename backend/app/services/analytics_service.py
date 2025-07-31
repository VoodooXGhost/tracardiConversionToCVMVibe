from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, desc, text
from typing import Dict, Any, List
from datetime import datetime, timedelta
from decimal import Decimal

from ..models import Customer, Campaign, Event, Segment
from ..schemas import DashboardMetrics

class AnalyticsService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_dashboard_metrics(self) -> DashboardMetrics:
        """Get main dashboard metrics"""
        
        # Date ranges
        now = datetime.utcnow()
        thirty_days_ago = now - timedelta(days=30)
        
        # Total customers
        total_customers_query = select(func.count()).select_from(Customer)
        total_customers_result = await self.db.execute(total_customers_query)
        total_customers = total_customers_result.scalar()
        
        # Active customers
        active_customers_query = select(func.count()).select_from(Customer).where(Customer.status == 'active')
        active_customers_result = await self.db.execute(active_customers_query)
        active_customers = active_customers_result.scalar()
        
        # New customers in last 30 days
        new_customers_query = select(func.count()).select_from(Customer).where(
            Customer.created_at >= thirty_days_ago
        )
        new_customers_result = await self.db.execute(new_customers_query)
        new_customers_30d = new_customers_result.scalar()
        
        # Churned customers in last 30 days
        churned_customers_query = select(func.count()).select_from(Customer).where(
            and_(
                Customer.status == 'churned',
                Customer.updated_at >= thirty_days_ago
            )
        )
        churned_customers_result = await self.db.execute(churned_customers_query)
        churned_customers_30d = churned_customers_result.scalar()
        
        # Churn rate
        churn_rate_30d = (churned_customers_30d / active_customers) if active_customers > 0 else 0
        
        # Revenue metrics
        total_revenue_query = select(func.sum(Customer.total_revenue)).select_from(Customer)
        total_revenue_result = await self.db.execute(total_revenue_query)
        total_revenue = total_revenue_result.scalar() or 0
        
        # ARPU
        arpu_query = select(func.avg(Customer.arpu_30d)).select_from(Customer).where(Customer.status == 'active')
        arpu_result = await self.db.execute(arpu_query)
        arpu_30d = arpu_result.scalar() or 0
        
        # Revenue growth (mock calculation)
        revenue_growth_30d = 0.05  # 5% growth
        
        # Campaign metrics
        active_campaigns_query = select(func.count()).select_from(Campaign).where(Campaign.status == 'running')
        active_campaigns_result = await self.db.execute(active_campaigns_query)
        active_campaigns = active_campaigns_result.scalar()
        
        total_campaigns_30d_query = select(func.count()).select_from(Campaign).where(
            Campaign.created_at >= thirty_days_ago
        )
        total_campaigns_30d_result = await self.db.execute(total_campaigns_30d_query)
        total_campaigns_30d = total_campaigns_30d_result.scalar()
        
        # Average campaign ROI
        roi_query = select(func.avg(
            (Campaign.revenue_generated - Campaign.total_cost) / Campaign.total_cost
        )).select_from(Campaign).where(
            and_(
                Campaign.status == 'completed',
                Campaign.total_cost > 0
            )
        )
        roi_result = await self.db.execute(roi_query)
        avg_campaign_roi = roi_result.scalar() or 0
        
        # Activity metrics
        avg_days_query = select(func.avg(Customer.days_since_last_activity)).select_from(Customer).where(
            Customer.status == 'active'
        )
        avg_days_result = await self.db.execute(avg_days_query)
        avg_days_since_activity = avg_days_result.scalar() or 0
        
        # High value customers
        high_value_query = select(func.count()).select_from(Customer).where(Customer.arpu_30d > 1000)
        high_value_result = await self.db.execute(high_value_query)
        high_value_customers = high_value_result.scalar()
        
        # At risk customers
        at_risk_query = select(func.count()).select_from(Customer).where(Customer.churn_score > 0.7)
        at_risk_result = await self.db.execute(at_risk_query)
        at_risk_customers = at_risk_result.scalar()
        
        return DashboardMetrics(
            total_customers=total_customers,
            active_customers=active_customers,
            new_customers_30d=new_customers_30d,
            churned_customers_30d=churned_customers_30d,
            churn_rate_30d=churn_rate_30d,
            total_revenue=Decimal(str(total_revenue)),
            arpu_30d=Decimal(str(arpu_30d)),
            revenue_growth_30d=revenue_growth_30d,
            active_campaigns=active_campaigns,
            total_campaigns_30d=total_campaigns_30d,
            avg_campaign_roi=avg_campaign_roi,
            avg_days_since_activity=avg_days_since_activity,
            high_value_customers=high_value_customers,
            at_risk_customers=at_risk_customers
        )

    async def get_churn_analytics(self, days: int = 30) -> Dict[str, Any]:
        """Get churn analytics"""
        
        # Overall churn rate
        total_customers_query = select(func.count()).select_from(Customer).where(Customer.status == 'active')
        total_customers_result = await self.db.execute(total_customers_query)
        total_customers = total_customers_result.scalar()
        
        churned_query = select(func.count()).select_from(Customer).where(Customer.status == 'churned')
        churned_result = await self.db.execute(churned_query)
        churned_customers = churned_result.scalar()
        
        overall_churn_rate = (churned_customers / (total_customers + churned_customers)) if (total_customers + churned_customers) > 0 else 0
        
        # Churn by customer type
        churn_by_type_query = select(
            Customer.customer_type,
            func.count().label('total'),
            func.sum(func.case((Customer.status == 'churned', 1), else_=0)).label('churned')
        ).group_by(Customer.customer_type)
        
        churn_by_type_result = await self.db.execute(churn_by_type_query)
        churn_by_customer_type = {}
        
        for row in churn_by_type_result:
            customer_type, total, churned = row
            churn_rate = (churned / total) if total > 0 else 0
            churn_by_customer_type[customer_type] = churn_rate
        
        # Risk distribution
        high_risk_query = select(func.count()).select_from(Customer).where(Customer.churn_score > 0.8)
        high_risk_result = await self.db.execute(high_risk_query)
        high_risk_customers = high_risk_result.scalar()
        
        medium_risk_query = select(func.count()).select_from(Customer).where(
            and_(Customer.churn_score > 0.5, Customer.churn_score <= 0.8)
        )
        medium_risk_result = await self.db.execute(medium_risk_query)
        medium_risk_customers = medium_risk_result.scalar()
        
        low_risk_query = select(func.count()).select_from(Customer).where(Customer.churn_score <= 0.5)
        low_risk_result = await self.db.execute(low_risk_query)
        low_risk_customers = low_risk_result.scalar()
        
        return {
            "overall_churn_rate": overall_churn_rate,
            "churn_by_customer_type": churn_by_customer_type,
            "churn_by_province": {},  # Mock data
            "churn_by_device_type": {},  # Mock data
            "high_risk_customers": high_risk_customers,
            "medium_risk_customers": medium_risk_customers,
            "low_risk_customers": low_risk_customers,
            "churn_trend_30d": []  # Mock trend data
        }

    async def get_revenue_analytics(self, days: int = 30) -> Dict[str, Any]:
        """Get revenue analytics"""
        
        # Total revenue
        total_revenue_query = select(func.sum(Customer.total_revenue)).select_from(Customer)
        total_revenue_result = await self.db.execute(total_revenue_query)
        total_revenue = total_revenue_result.scalar() or 0
        
        # Revenue by customer type
        revenue_by_type_query = select(
            Customer.customer_type,
            func.sum(Customer.total_revenue)
        ).group_by(Customer.customer_type)
        
        revenue_by_type_result = await self.db.execute(revenue_by_type_query)
        revenue_by_customer_type = dict(revenue_by_type_result.fetchall())
        
        # ARPU distribution
        arpu_ranges = [
            ("0-200", 0, 200),
            ("200-500", 200, 500),
            ("500-1000", 500, 1000),
            ("1000+", 1000, float('inf'))
        ]
        
        arpu_distribution = {}
        for range_name, min_val, max_val in arpu_ranges:
            if max_val == float('inf'):
                count_query = select(func.count()).select_from(Customer).where(Customer.arpu_30d >= min_val)
            else:
                count_query = select(func.count()).select_from(Customer).where(
                    and_(Customer.arpu_30d >= min_val, Customer.arpu_30d < max_val)
                )
            
            count_result = await self.db.execute(count_query)
            arpu_distribution[range_name] = count_result.scalar()
        
        return {
            "total_revenue": total_revenue,
            "revenue_by_customer_type": revenue_by_customer_type,
            "revenue_by_province": {},  # Mock data
            "arpu_distribution": arpu_distribution,
            "revenue_trend_30d": [],  # Mock trend data
            "top_revenue_customers": []  # Mock data
        }

    async def get_campaign_analytics(self, days: int = 30) -> Dict[str, Any]:
        """Get campaign analytics"""
        
        date_filter = datetime.utcnow() - timedelta(days=days)
        
        # Total campaigns
        total_campaigns_query = select(func.count()).select_from(Campaign).where(
            Campaign.created_at >= date_filter
        )
        total_campaigns_result = await self.db.execute(total_campaigns_query)
        total_campaigns = total_campaigns_result.scalar()
        
        # Campaign performance
        performance_query = select(
            Campaign.name,
            Campaign.status,
            Campaign.sent_count,
            Campaign.delivered_count,
            Campaign.opened_count,
            Campaign.clicked_count,
            Campaign.converted_count,
            Campaign.total_cost,
            Campaign.revenue_generated
        ).where(Campaign.created_at >= date_filter)
        
        performance_result = await self.db.execute(performance_query)
        campaign_performance = []
        
        for row in performance_result:
            campaign_performance.append({
                "name": row[0],
                "status": row[1],
                "sent_count": row[2],
                "delivered_count": row[3],
                "opened_count": row[4],
                "clicked_count": row[5],
                "converted_count": row[6],
                "total_cost": float(row[7]) if row[7] else 0,
                "revenue_generated": float(row[8]) if row[8] else 0,
                "delivery_rate": (row[3] / row[2]) if row[2] > 0 else 0,
                "conversion_rate": (row[6] / row[5]) if row[5] > 0 else 0
            })
        
        return {
            "total_campaigns": total_campaigns,
            "campaign_performance": campaign_performance,
            "channel_performance": {},  # Mock data
            "roi_by_campaign_type": {},  # Mock data
            "conversion_funnel": {},  # Mock data
            "best_performing_campaigns": campaign_performance[:5]  # Top 5
        }

    async def get_real_time_metrics(self) -> Dict[str, Any]:
        """Get real-time metrics for WebSocket updates"""
        
        # Active customers
        active_customers_query = select(func.count()).select_from(Customer).where(Customer.status == 'active')
        active_customers_result = await self.db.execute(active_customers_query)
        active_customers = active_customers_result.scalar()
        
        # Average churn rate
        avg_churn_query = select(func.avg(Customer.churn_score)).select_from(Customer).where(Customer.status == 'active')
        avg_churn_result = await self.db.execute(avg_churn_query)
        churn_rate = avg_churn_result.scalar() or 0
        
        # Average ARPU
        avg_arpu_query = select(func.avg(Customer.arpu_30d)).select_from(Customer).where(Customer.status == 'active')
        avg_arpu_result = await self.db.execute(avg_arpu_query)
        arpu = avg_arpu_result.scalar() or 0
        
        # Active campaigns
        active_campaigns_query = select(func.count()).select_from(Campaign).where(Campaign.status == 'running')
        active_campaigns_result = await self.db.execute(active_campaigns_query)
        active_campaigns = active_campaigns_result.scalar()
        
        return {
            "active_customers": active_customers,
            "churn_rate": float(churn_rate),
            "arpu": float(arpu),
            "active_campaigns": active_campaigns,
            "timestamp": datetime.utcnow().isoformat()
        }

    async def get_kpi_cards(self) -> List[Dict[str, Any]]:
        """Get KPI cards for dashboard"""
        
        # Total customers
        total_customers_query = select(func.count()).select_from(Customer)
        total_customers_result = await self.db.execute(total_customers_query)
        total_customers = total_customers_result.scalar()
        
        # ARPU
        arpu_query = select(func.avg(Customer.arpu_30d)).select_from(Customer).where(Customer.status == 'active')
        arpu_result = await self.db.execute(arpu_query)
        arpu = arpu_result.scalar() or 0
        
        # Churn rate
        churn_query = select(func.avg(Customer.churn_score)).select_from(Customer).where(Customer.status == 'active')
        churn_result = await self.db.execute(churn_query)
        churn_rate = churn_result.scalar() or 0
        
        # Active campaigns
        campaigns_query = select(func.count()).select_from(Campaign).where(Campaign.status == 'running')
        campaigns_result = await self.db.execute(campaigns_query)
        active_campaigns = campaigns_result.scalar()
        
        return [
            {
                "title": "Total Customers",
                "value": f"{total_customers:,}",
                "change": 5.2,
                "change_type": "increase",
                "format_type": "number"
            },
            {
                "title": "Average ARPU",
                "value": f"{arpu:.0f} MZN",
                "change": 3.1,
                "change_type": "increase",
                "format_type": "currency"
            },
            {
                "title": "Churn Rate",
                "value": f"{churn_rate*100:.1f}%",
                "change": -2.1,
                "change_type": "decrease",
                "format_type": "percentage"
            },
            {
                "title": "Active Campaigns",
                "value": f"{active_campaigns}",
                "change": 1,
                "change_type": "increase",
                "format_type": "number"
            }
        ]

    async def get_trends(self, metric: str, period: str, days: int) -> Dict[str, Any]:
        """Get trend data for charts"""
        # Mock trend data for demonstration
        import random
        from datetime import datetime, timedelta
        
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        # Generate mock trend data
        data_points = []
        current_date = start_date
        
        while current_date <= end_date:
            if period == 'daily':
                value = random.uniform(500, 1500) if metric == 'arpu' else random.uniform(0.02, 0.08)
                data_points.append({
                    "date": current_date.strftime("%Y-%m-%d"),
                    "value": value
                })
                current_date += timedelta(days=1)
            elif period == 'weekly':
                value = random.uniform(500, 1500) if metric == 'arpu' else random.uniform(0.02, 0.08)
                data_points.append({
                    "date": current_date.strftime("%Y-W%U"),
                    "value": value
                })
                current_date += timedelta(weeks=1)
        
        return {
            "metric": metric,
            "period": period,
            "data": data_points
        }