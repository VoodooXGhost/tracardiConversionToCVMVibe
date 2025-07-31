"""
Generate mock data for CVM MVP demonstration
This script creates realistic telco customer data for Tmcel
"""

import asyncio
import random
from datetime import datetime, timedelta, date
from decimal import Decimal
from faker import Faker
import uuid

from app.core.database import AsyncSessionLocal, engine, Base
from app.models import Customer, Event, Campaign, CampaignInteraction, Offer, LoyaltyPoint, Segment, CustomerSegment

# Initialize Faker with Portuguese locale for Mozambique
fake = Faker(['pt_PT', 'en_US'])

# Mozambican provinces
PROVINCES = [
    'Maputo', 'Gaza', 'Inhambane', 'Sofala', 'Manica', 
    'Tete', 'Zambézia', 'Nampula', 'Cabo Delgado', 'Niassa'
]

# Major cities in Mozambique
CITIES = {
    'Maputo': ['Maputo', 'Matola', 'Boane'],
    'Gaza': ['Xai-Xai', 'Chokwé', 'Chibuto'],
    'Inhambane': ['Inhambane', 'Maxixe', 'Vilanculos'],
    'Sofala': ['Beira', 'Dondo', 'Nhamatanda'],
    'Manica': ['Chimoio', 'Gondola', 'Manica'],
    'Tete': ['Tete', 'Moatize', 'Cahora Bassa'],
    'Zambézia': ['Quelimane', 'Mocuba', 'Gurué'],
    'Nampula': ['Nampula', 'Nacala', 'Ilha de Moçambique'],
    'Cabo Delgado': ['Pemba', 'Montepuez', 'Mocímboa da Praia'],
    'Niassa': ['Lichinga', 'Cuamba', 'Mandimba']
}

# Device brands popular in Mozambique
DEVICE_BRANDS = {
    'smartphone': ['Samsung', 'Xiaomi', 'Tecno', 'Infinix', 'Huawei', 'Oppo'],
    'feature_phone': ['Nokia', 'Itel', 'Tecno', 'Infinix']
}

# Event types for telco
EVENT_TYPES = [
    ('recharge', 'Account Recharge'),
    ('call_outgoing', 'Outgoing Call'),
    ('call_incoming', 'Incoming Call'),
    ('sms_sent', 'SMS Sent'),
    ('sms_received', 'SMS Received'),
    ('data_session', 'Data Session'),
    ('bundle_purchase', 'Bundle Purchase'),
    ('balance_inquiry', 'Balance Inquiry'),
    ('service_activation', 'Service Activation'),
    ('payment', 'Payment Made')
]

class MockDataGenerator:
    def __init__(self):
        self.customers = []
        self.offers = []
        self.segments = []
        self.campaigns = []

    async def generate_all_data(self):
        """Generate all mock data"""
        print("🚀 Starting mock data generation for CVM MVP...")
        
        async with AsyncSessionLocal() as session:
            # Create tables
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            
            print("📊 Generating offers...")
            await self.generate_offers(session)
            
            print("👥 Generating customers...")
            await self.generate_customers(session, count=10000)
            
            print("📱 Generating events...")
            await self.generate_events(session, count=50000)
            
            print("🎯 Generating segments...")
            await self.generate_segments(session)
            
            print("📢 Generating campaigns...")
            await self.generate_campaigns(session)
            
            print("🎁 Generating loyalty points...")
            await self.generate_loyalty_points(session)
            
            await session.commit()
            print("✅ Mock data generation completed!")

    async def generate_offers(self, session):
        """Generate sample offers"""
        offers_data = [
            {
                'name': '1GB Data Bundle',
                'description': '1GB high-speed data valid for 7 days',
                'offer_type': 'data_bundle',
                'price': Decimal('100.00'),
                'data_mb': 1024,
                'validity_days': 7
            },
            {
                'name': '5GB Data Bundle',
                'description': '5GB high-speed data valid for 30 days',
                'offer_type': 'data_bundle',
                'price': Decimal('400.00'),
                'data_mb': 5120,
                'validity_days': 30
            },
            {
                'name': '10GB Data Bundle',
                'description': '10GB high-speed data valid for 30 days',
                'offer_type': 'data_bundle',
                'price': Decimal('700.00'),
                'data_mb': 10240,
                'validity_days': 30
            },
            {
                'name': 'Weekend Voice Bundle',
                'description': '200 minutes valid for weekends',
                'offer_type': 'voice_bundle',
                'price': Decimal('150.00'),
                'voice_minutes': 200,
                'validity_days': 7
            },
            {
                'name': 'SMS Bundle 100',
                'description': '100 SMS to any network',
                'offer_type': 'sms_bundle',
                'price': Decimal('50.00'),
                'sms_count': 100,
                'validity_days': 30
            },
            {
                'name': 'Youth Combo',
                'description': '2GB + 100 minutes + 50 SMS',
                'offer_type': 'combo',
                'price': Decimal('250.00'),
                'data_mb': 2048,
                'voice_minutes': 100,
                'sms_count': 50,
                'validity_days': 30
            }
        ]
        
        for offer_data in offers_data:
            offer = Offer(**offer_data)
            session.add(offer)
            self.offers.append(offer)
        
        await session.flush()

    async def generate_customers(self, session, count=10000):
        """Generate realistic customer data"""
        
        for i in range(count):
            # Basic demographics
            gender = random.choice(['M', 'F'])
            first_name = fake.first_name_male() if gender == 'M' else fake.first_name_female()
            last_name = fake.last_name()
            
            # Age distribution (skewed towards younger population)
            age = int(random.betavariate(2, 5) * 60 + 18)  # 18-78, skewed young
            birth_date = date.today() - timedelta(days=age * 365)
            
            # Location
            province = random.choice(PROVINCES)
            city = random.choice(CITIES[province])
            
            # Customer type (70% prepaid, 30% postpaid)
            customer_type = 'prepaid' if random.random() < 0.7 else 'postpaid'
            
            # Phone number (Mozambican format)
            phone_number = f"+258{random.choice(['82', '83', '84', '85', '86', '87'])}{random.randint(1000000, 9999999)}"
            
            # Email (not everyone has email)
            email = fake.email() if random.random() < 0.4 else None
            
            # Activation date (spread over last 5 years)
            activation_date = fake.date_time_between(start_date='-5y', end_date='now')
            
            # Device information
            device_type = random.choices(['smartphone', 'feature_phone'], weights=[0.6, 0.4])[0]
            device_brand = random.choice(DEVICE_BRANDS[device_type])
            device_models = {
                'Samsung': ['Galaxy A12', 'Galaxy A32', 'Galaxy S21'],
                'Xiaomi': ['Redmi 9', 'Redmi Note 10', 'Mi 11'],
                'Tecno': ['Spark 7', 'Camon 17', 'Phantom X'],
                'Nokia': ['3310', '105', '216'],
                'Infinix': ['Hot 10', 'Note 8', 'Zero 8']
            }
            device_model = random.choice(device_models.get(device_brand, ['Unknown']))
            
            # Financial metrics based on customer profile
            if customer_type == 'postpaid':
                # Postpaid customers generally have higher ARPU
                base_arpu = random.uniform(800, 2500)
                current_balance = 0  # Postpaid doesn't have prepaid balance
            else:
                # Prepaid customers
                base_arpu = random.uniform(200, 1200)
                current_balance = random.uniform(0, 500)
            
            # Add some variation to ARPU
            arpu_30d = Decimal(str(round(base_arpu * random.uniform(0.8, 1.2), 2)))
            arpu_90d = Decimal(str(round(base_arpu * random.uniform(0.9, 1.1), 2)))
            
            # Usage patterns
            total_recharges = random.randint(5, 50) if customer_type == 'prepaid' else 0
            avg_recharge_amount = Decimal(str(round(float(arpu_30d) / max(total_recharges, 1), 2)))
            
            # Usage based on device type and customer profile
            if device_type == 'smartphone':
                total_data_mb = random.randint(500, 15000)
                total_voice_minutes = random.randint(100, 2000)
                total_sms_sent = random.randint(20, 500)
            else:
                total_data_mb = random.randint(0, 1000)
                total_voice_minutes = random.randint(200, 3000)
                total_sms_sent = random.randint(50, 1000)
            
            # Activity and churn indicators
            days_since_last_activity = random.choices(
                range(0, 91), 
                weights=[50] + [max(1, 50-i) for i in range(1, 91)]
            )[0]
            
            # Status based on activity
            if days_since_last_activity > 60:
                status = random.choices(['active', 'churned'], weights=[0.3, 0.7])[0]
            else:
                status = 'active'
            
            # Churn score calculation (mock ML prediction)
            churn_factors = []
            if days_since_last_activity > 30:
                churn_factors.append(0.3)
            if float(arpu_30d) < 300:
                churn_factors.append(0.2)
            if customer_type == 'prepaid' and current_balance < 10:
                churn_factors.append(0.15)
            if total_recharges < 3:
                churn_factors.append(0.1)
            
            base_churn = sum(churn_factors)
            churn_score = Decimal(str(round(min(0.95, max(0.05, base_churn + random.uniform(-0.1, 0.1))), 3)))
            
            # Lifetime value estimation
            months_active = max(1, (datetime.now() - activation_date).days / 30)
            lifetime_value = Decimal(str(round(float(arpu_90d) * months_active * 0.3, 2)))
            
            # Total revenue
            total_revenue = Decimal(str(round(float(arpu_90d) * months_active, 2)))
            
            customer = Customer(
                phone_number=phone_number,
                email=email,
                first_name=first_name,
                last_name=last_name,
                date_of_birth=birth_date,
                gender=gender,
                customer_type=customer_type,
                activation_date=activation_date,
                status=status,
                province=province,
                city=city,
                current_balance=Decimal(str(round(current_balance, 2))),
                arpu_30d=arpu_30d,
                arpu_90d=arpu_90d,
                total_revenue=total_revenue,
                total_voice_minutes=total_voice_minutes,
                total_sms_sent=total_sms_sent,
                total_data_mb=total_data_mb,
                days_since_last_activity=days_since_last_activity,
                total_recharges=total_recharges,
                avg_recharge_amount=avg_recharge_amount,
                primary_device_brand=device_brand,
                primary_device_model=device_model,
                device_type=device_type,
                churn_score=churn_score,
                lifetime_value=lifetime_value,
                last_activity_at=datetime.now() - timedelta(days=days_since_last_activity)
            )
            
            session.add(customer)
            self.customers.append(customer)
            
            # Commit in batches
            if (i + 1) % 1000 == 0:
                await session.flush()
                print(f"  Generated {i + 1} customers...")

    async def generate_events(self, session, count=50000):
        """Generate customer events"""
        
        if not self.customers:
            print("No customers found, skipping events generation")
            return
        
        for i in range(count):
            customer = random.choice(self.customers)
            event_type, event_name = random.choice(EVENT_TYPES)
            
            # Event timing (more recent events are more likely)
            days_ago = int(random.expovariate(0.1))  # Exponential distribution
            days_ago = min(days_ago, 365)  # Cap at 1 year
            occurred_at = datetime.now() - timedelta(days=days_ago)
            
            # Event-specific data
            amount = None
            duration = None
            data_volume_mb = None
            properties = {}
            
            if event_type == 'recharge':
                amount = Decimal(str(random.choice([50, 100, 200, 500, 1000])))
                properties = {'method': random.choice(['mobile_money', 'scratch_card', 'bank'])}
            
            elif event_type in ['call_outgoing', 'call_incoming']:
                duration = random.randint(30, 1800)  # 30 seconds to 30 minutes
                properties = {'destination': random.choice(['local', 'national', 'international'])}
            
            elif event_type == 'data_session':
                data_volume_mb = random.randint(1, 500)
                duration = random.randint(60, 7200)  # 1 minute to 2 hours
                properties = {'app': random.choice(['WhatsApp', 'Facebook', 'YouTube', 'Browser'])}
            
            elif event_type == 'bundle_purchase':
                if self.offers:
                    offer = random.choice(self.offers)
                    amount = offer.price
                    properties = {'offer_id': str(offer.id), 'offer_name': offer.name}
            
            # Channel
            channel = random.choices(
                ['ussd', 'app', 'web', 'retail', 'call_center'],
                weights=[40, 25, 15, 15, 5]
            )[0]
            
            event = Event(
                customer_id=customer.id,
                event_type=event_type,
                event_name=event_name,
                properties=properties,
                amount=amount,
                duration=duration,
                data_volume_mb=data_volume_mb,
                channel=channel,
                location_province=customer.province,
                location_city=customer.city,
                occurred_at=occurred_at
            )
            
            session.add(event)
            
            # Commit in batches
            if (i + 1) % 5000 == 0:
                await session.flush()
                print(f"  Generated {i + 1} events...")

    async def generate_segments(self, session):
        """Generate predefined segments"""
        segments_data = [
            {
                'name': 'High Value Customers',
                'description': 'Customers with ARPU > 1000 MZN',
                'conditions': {'arpu_30d': {'operator': '>', 'value': 1000}},
                'created_by': 'system'
            },
            {
                'name': 'At Risk Customers',
                'description': 'Customers with high churn probability',
                'conditions': {'churn_score': {'operator': '>', 'value': 0.7}},
                'created_by': 'system'
            },
            {
                'name': 'Data Heavy Users',
                'description': 'Customers using >5GB monthly',
                'conditions': {'total_data_mb': {'operator': '>', 'value': 5120}},
                'created_by': 'system'
            },
            {
                'name': 'New Customers',
                'description': 'Customers activated in last 30 days',
                'conditions': {'days_since_last_activity': {'operator': '<', 'value': 30}},
                'created_by': 'system'
            },
            {
                'name': 'Prepaid Low Balance',
                'description': 'Prepaid customers with balance < 50 MZN',
                'conditions': {
                    'customer_type': {'operator': '=', 'value': 'prepaid'},
                    'current_balance': {'operator': '<', 'value': 50}
                },
                'created_by': 'system'
            },
            {
                'name': 'Smartphone Users',
                'description': 'Customers using smartphones',
                'conditions': {'device_type': {'operator': '=', 'value': 'smartphone'}},
                'created_by': 'system'
            },
            {
                'name': 'Maputo Customers',
                'description': 'Customers in Maputo province',
                'conditions': {'province': {'operator': '=', 'value': 'Maputo'}},
                'created_by': 'system'
            }
        ]
        
        for segment_data in segments_data:
            segment = Segment(**segment_data)
            
            # Calculate customer count (simplified for demo)
            if segment.name == 'High Value Customers':
                segment.customer_count = len([c for c in self.customers if float(c.arpu_30d) > 1000])
            elif segment.name == 'At Risk Customers':
                segment.customer_count = len([c for c in self.customers if float(c.churn_score) > 0.7])
            elif segment.name == 'Data Heavy Users':
                segment.customer_count = len([c for c in self.customers if c.total_data_mb > 5120])
            elif segment.name == 'Smartphone Users':
                segment.customer_count = len([c for c in self.customers if c.device_type == 'smartphone'])
            else:
                segment.customer_count = random.randint(100, 2000)
            
            session.add(segment)
            self.segments.append(segment)
        
        await session.flush()

    async def generate_campaigns(self, session):
        """Generate sample campaigns"""
        if not self.segments:
            print("No segments found, skipping campaigns generation")
            return
        
        campaigns_data = [
            {
                'name': 'Data Bundle Promotion',
                'description': 'Promote 5GB data bundle to high-value customers',
                'campaign_type': 'sms',
                'message_template': 'Hi {first_name}! Get 5GB data for only 400 MZN. Valid for 30 days. Reply YES to activate.',
                'status': 'completed',
                'budget': Decimal('50000.00'),
                'cost_per_message': Decimal('2.50')
            },
            {
                'name': 'Retention Campaign',
                'description': 'Win back at-risk customers',
                'campaign_type': 'sms',
                'message_template': 'We miss you! Come back with 50% off your next recharge. Use code COMEBACK50.',
                'status': 'completed',
                'budget': Decimal('30000.00'),
                'cost_per_message': Decimal('2.50')
            },
            {
                'name': 'Youth Combo Offer',
                'description': 'Target young customers with combo deals',
                'campaign_type': 'sms',
                'message_template': 'Youth Special: 2GB + 100min + 50SMS for 250 MZN! Perfect for social media. Reply YES.',
                'status': 'running',
                'budget': Decimal('25000.00'),
                'cost_per_message': Decimal('2.50')
            }
        ]
        
        for i, campaign_data in enumerate(campaigns_data):
            # Assign to random segment
            target_segment = random.choice(self.segments)
            campaign_data['target_segment_id'] = target_segment.id
            
            # Set dates
            if campaign_data['status'] == 'completed':
                start_date = fake.date_time_between(start_date='-60d', end_date='-30d')
                campaign_data['started_at'] = start_date
                campaign_data['completed_at'] = start_date + timedelta(days=random.randint(1, 7))
                campaign_data['scheduled_at'] = start_date - timedelta(hours=1)
            elif campaign_data['status'] == 'running':
                start_date = fake.date_time_between(start_date='-7d', end_date='now')
                campaign_data['started_at'] = start_date
                campaign_data['scheduled_at'] = start_date - timedelta(hours=1)
            
            # Performance metrics for completed campaigns
            if campaign_data['status'] == 'completed':
                target_count = min(target_segment.customer_count, random.randint(1000, 5000))
                sent_count = int(target_count * random.uniform(0.95, 1.0))
                delivered_count = int(sent_count * random.uniform(0.92, 0.98))
                opened_count = int(delivered_count * random.uniform(0.85, 0.95))  # SMS open rate is high
                clicked_count = int(opened_count * random.uniform(0.08, 0.15))
                converted_count = int(clicked_count * random.uniform(0.20, 0.40))
                
                campaign_data.update({
                    'target_count': target_count,
                    'sent_count': sent_count,
                    'delivered_count': delivered_count,
                    'opened_count': opened_count,
                    'clicked_count': clicked_count,
                    'converted_count': converted_count,
                    'total_cost': Decimal(str(sent_count * float(campaign_data['cost_per_message']))),
                    'revenue_generated': Decimal(str(converted_count * random.uniform(200, 800)))
                })
            
            campaign_data['created_by'] = 'demo_user'
            
            campaign = Campaign(**campaign_data)
            session.add(campaign)
            self.campaigns.append(campaign)
        
        await session.flush()

    async def generate_loyalty_points(self, session):
        """Generate loyalty points for some customers"""
        if not self.customers:
            return
        
        # Generate loyalty points for 30% of customers
        loyalty_customers = random.sample(self.customers, int(len(self.customers) * 0.3))
        
        for customer in loyalty_customers:
            # Generate 1-5 loyalty transactions per customer
            num_transactions = random.randint(1, 5)
            current_balance = 0
            
            for _ in range(num_transactions):
                transaction_type = random.choices(
                    ['earned', 'spent'], 
                    weights=[0.7, 0.3]
                )[0]
                
                if transaction_type == 'earned':
                    points = random.randint(10, 200)
                    current_balance += points
                    description = random.choice([
                        'Points earned from recharge',
                        'Bonus points for loyalty',
                        'Points from bundle purchase',
                        'Birthday bonus points'
                    ])
                else:
                    if current_balance > 0:
                        points = random.randint(10, min(current_balance, 100))
                        current_balance -= points
                        description = random.choice([
                            'Points redeemed for data bundle',
                            'Points used for discount',
                            'Points exchanged for airtime'
                        ])
                    else:
                        continue
                
                loyalty_point = LoyaltyPoint(
                    customer_id=customer.id,
                    points_earned=points if transaction_type == 'earned' else 0,
                    points_spent=points if transaction_type == 'spent' else 0,
                    current_balance=current_balance,
                    transaction_type=transaction_type,
                    description=description,
                    created_at=fake.date_time_between(start_date='-90d', end_date='now')
                )
                
                session.add(loyalty_point)

async def main():
    """Main function to run data generation"""
    generator = MockDataGenerator()
    await generator.generate_all_data()

if __name__ == "__main__":
    asyncio.run(main())