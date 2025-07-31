import numpy as np
import pandas as pd
from typing import Dict, Any, Optional, List
import uuid
import random
from datetime import datetime, timedelta

from ..schemas import CustomerResponse, OfferResponse

class MLService:
    """
    Mock ML Service for MVP demonstration
    In production, this would integrate with actual ML models
    """
    
    def __init__(self):
        # Mock model weights for demonstration
        self.churn_weights = {
            'days_since_last_activity': 0.3,
            'arpu_30d': -0.2,
            'total_recharges': -0.15,
            'current_balance': -0.1,
            'device_type_smartphone': -0.1,
            'customer_type_postpaid': -0.15
        }
        
        self.nbo_weights = {
            'data_bundle': {'arpu_high': 0.4, 'data_usage_low': 0.3, 'smartphone': 0.2},
            'voice_bundle': {'arpu_medium': 0.3, 'voice_usage_high': 0.4, 'feature_phone': 0.2},
            'sms_bundle': {'young_age': 0.3, 'sms_usage_high': 0.4, 'prepaid': 0.2}
        }

    async def predict_churn(self, customer: CustomerResponse) -> float:
        """
        Predict churn probability for a customer
        Returns probability between 0.0 and 1.0
        """
        
        # Extract features
        features = {
            'days_since_last_activity': min(customer.days_since_last_activity, 90) / 90.0,
            'arpu_30d': min(float(customer.arpu_30d), 2000) / 2000.0,
            'total_recharges': min(customer.total_recharges, 50) / 50.0,
            'current_balance': min(float(customer.current_balance), 1000) / 1000.0,
            'device_type_smartphone': 1.0 if customer.device_type == 'smartphone' else 0.0,
            'customer_type_postpaid': 1.0 if customer.customer_type == 'postpaid' else 0.0
        }
        
        # Calculate weighted score
        score = 0.0
        for feature, value in features.items():
            if feature in self.churn_weights:
                score += self.churn_weights[feature] * value
        
        # Apply sigmoid function to get probability
        probability = 1 / (1 + np.exp(-score))
        
        # Add some randomness for demo variety
        probability += random.uniform(-0.1, 0.1)
        probability = max(0.0, min(1.0, probability))
        
        return round(probability, 3)

    async def get_churn_factors(self, customer: CustomerResponse) -> List[Dict[str, Any]]:
        """Get factors contributing to churn risk"""
        factors = []
        
        if customer.days_since_last_activity > 30:
            factors.append({
                "factor": "Inactivity",
                "description": f"No activity for {customer.days_since_last_activity} days",
                "impact": "high",
                "weight": 0.3
            })
        
        if float(customer.arpu_30d) < 200:
            factors.append({
                "factor": "Low ARPU",
                "description": f"ARPU of {customer.arpu_30d} MZN is below average",
                "impact": "medium",
                "weight": 0.2
            })
        
        if float(customer.current_balance) < 10 and customer.customer_type == 'prepaid':
            factors.append({
                "factor": "Low Balance",
                "description": f"Current balance is only {customer.current_balance} MZN",
                "impact": "medium",
                "weight": 0.15
            })
        
        if customer.total_recharges < 5:
            factors.append({
                "factor": "Low Engagement",
                "description": f"Only {customer.total_recharges} recharges in recent period",
                "impact": "medium",
                "weight": 0.15
            })
        
        return factors

    async def get_retention_recommendations(self, customer: CustomerResponse) -> List[Dict[str, Any]]:
        """Get retention recommendations for at-risk customers"""
        recommendations = []
        
        if customer.days_since_last_activity > 30:
            recommendations.append({
                "action": "Re-engagement Campaign",
                "description": "Send personalized SMS with special offer",
                "priority": "high",
                "expected_impact": "25% reduction in churn probability"
            })
        
        if float(customer.current_balance) < 50 and customer.customer_type == 'prepaid':
            recommendations.append({
                "action": "Balance Bonus",
                "description": "Offer bonus credit on next recharge",
                "priority": "medium",
                "expected_impact": "15% increase in recharge likelihood"
            })
        
        if float(customer.arpu_30d) < 500:
            recommendations.append({
                "action": "Value Bundle Offer",
                "description": "Promote cost-effective data/voice bundles",
                "priority": "medium",
                "expected_impact": "20% ARPU increase"
            })
        
        return recommendations

    async def predict_next_best_offer(self, customer: CustomerResponse) -> Optional[uuid.UUID]:
        """
        Predict the next best offer for a customer
        Returns offer ID or None
        """
        
        # Mock offer IDs (in production, these would come from the offers table)
        mock_offers = {
            'data_bundle': uuid.UUID('12345678-1234-5678-9012-123456789012'),
            'voice_bundle': uuid.UUID('12345678-1234-5678-9012-123456789013'),
            'sms_bundle': uuid.UUID('12345678-1234-5678-9012-123456789014')
        }
        
        scores = {}
        
        # Score data bundle
        data_score = 0.0
        if float(customer.arpu_30d) > 800:  # High ARPU
            data_score += 0.4
        if customer.total_data_mb < 2048:  # Low data usage
            data_score += 0.3
        if customer.device_type == 'smartphone':
            data_score += 0.2
        scores['data_bundle'] = data_score
        
        # Score voice bundle
        voice_score = 0.0
        if 300 <= float(customer.arpu_30d) <= 800:  # Medium ARPU
            voice_score += 0.3
        if customer.total_voice_minutes > 500:  # High voice usage
            voice_score += 0.4
        if customer.device_type == 'feature_phone':
            voice_score += 0.2
        scores['voice_bundle'] = voice_score
        
        # Score SMS bundle
        sms_score = 0.0
        if customer.date_of_birth and (datetime.now().date() - customer.date_of_birth).days < 365 * 30:  # Young
            sms_score += 0.3
        if customer.total_sms_sent > 100:  # High SMS usage
            sms_score += 0.4
        if customer.customer_type == 'prepaid':
            sms_score += 0.2
        scores['sms_bundle'] = sms_score
        
        # Return offer with highest score
        if not scores or max(scores.values()) < 0.3:
            return None
        
        best_offer_type = max(scores, key=scores.get)
        return mock_offers.get(best_offer_type)

    async def get_offer_confidence(self, customer: CustomerResponse, offer: OfferResponse) -> float:
        """Get confidence score for offer recommendation"""
        # Mock confidence calculation
        base_confidence = 0.7
        
        # Adjust based on customer profile
        if customer.churn_score < 0.3:  # Low churn risk
            base_confidence += 0.2
        elif customer.churn_score > 0.8:  # High churn risk
            base_confidence -= 0.1
        
        if float(customer.arpu_30d) > 1000:  # High value customer
            base_confidence += 0.1
        
        return round(min(1.0, max(0.0, base_confidence)), 2)

    async def get_offer_reasoning(self, customer: CustomerResponse, offer: OfferResponse) -> List[str]:
        """Get reasoning for offer recommendation"""
        reasons = []
        
        if offer.offer_type == 'data_bundle':
            if customer.device_type == 'smartphone':
                reasons.append("Customer uses smartphone - likely to need data")
            if customer.total_data_mb < 2048:
                reasons.append("Low historical data usage - opportunity to increase")
            if float(customer.arpu_30d) > 800:
                reasons.append("High ARPU indicates willingness to spend on data")
        
        elif offer.offer_type == 'voice_bundle':
            if customer.total_voice_minutes > 500:
                reasons.append("High voice usage indicates need for voice bundles")
            if customer.customer_type == 'postpaid':
                reasons.append("Postpaid customers often prefer voice bundles")
        
        elif offer.offer_type == 'sms_bundle':
            if customer.total_sms_sent > 100:
                reasons.append("High SMS usage indicates bundle would provide value")
            if customer.customer_type == 'prepaid':
                reasons.append("Prepaid customers often use SMS bundles")
        
        if not reasons:
            reasons.append("Based on similar customer profiles and preferences")
        
        return reasons

    async def predict_campaign_success(self, campaign_data: Dict[str, Any]) -> Dict[str, float]:
        """Predict campaign success metrics"""
        # Mock prediction based on campaign characteristics
        base_rates = {
            'delivery_rate': 0.95,
            'open_rate': 0.25,
            'click_rate': 0.08,
            'conversion_rate': 0.03
        }
        
        # Adjust based on campaign type
        if campaign_data.get('campaign_type') == 'sms':
            base_rates['open_rate'] = 0.98  # SMS has very high open rate
            base_rates['click_rate'] = 0.12
        
        # Adjust based on target segment
        segment_conditions = campaign_data.get('segment_conditions', {})
        if 'arpu_30d' in segment_conditions and segment_conditions['arpu_30d'].get('value', 0) > 1000:
            # High value customers have better conversion
            base_rates['conversion_rate'] *= 1.5
        
        return base_rates

    async def get_segment_insights(self, segment_conditions: Dict[str, Any]) -> Dict[str, Any]:
        """Get insights about a customer segment"""
        insights = {
            'predicted_response_rate': random.uniform(0.02, 0.08),
            'avg_customer_value': random.uniform(500, 1500),
            'churn_risk_distribution': {
                'low': random.uniform(0.4, 0.7),
                'medium': random.uniform(0.2, 0.4),
                'high': random.uniform(0.1, 0.3)
            },
            'recommended_offers': ['data_bundle', 'voice_bundle'],
            'best_contact_time': 'afternoon',
            'preferred_channel': 'sms'
        }
        
        return insights