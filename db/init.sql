-- CVM MVP Database Schema for Tmcel
-- PostgreSQL 14+ compatible

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Customers table (unified customer profiles)
CREATE TABLE customers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    phone_number VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(255),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    date_of_birth DATE,
    gender VARCHAR(10),
    
    -- Telco specific fields
    customer_type VARCHAR(20) NOT NULL DEFAULT 'prepaid', -- prepaid, postpaid
    activation_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) NOT NULL DEFAULT 'active', -- active, suspended, churned
    
    -- Location data
    province VARCHAR(50),
    city VARCHAR(50),
    
    -- Financial metrics
    current_balance DECIMAL(10,2) DEFAULT 0.00,
    arpu_30d DECIMAL(10,2) DEFAULT 0.00, -- Average Revenue Per User (30 days)
    arpu_90d DECIMAL(10,2) DEFAULT 0.00, -- Average Revenue Per User (90 days)
    total_revenue DECIMAL(12,2) DEFAULT 0.00,
    
    -- Usage metrics
    total_voice_minutes INTEGER DEFAULT 0,
    total_sms_sent INTEGER DEFAULT 0,
    total_data_mb BIGINT DEFAULT 0,
    
    -- Behavioral metrics
    days_since_last_activity INTEGER DEFAULT 0,
    total_recharges INTEGER DEFAULT 0,
    avg_recharge_amount DECIMAL(10,2) DEFAULT 0.00,
    
    -- Device information
    primary_device_brand VARCHAR(50),
    primary_device_model VARCHAR(100),
    device_type VARCHAR(20), -- smartphone, feature_phone, tablet
    
    -- Predictive scores (ML generated)
    churn_score DECIMAL(3,2) DEFAULT 0.00, -- 0.00 to 1.00
    lifetime_value DECIMAL(12,2) DEFAULT 0.00,
    next_best_offer_id UUID,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_activity_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Customer segments table
CREATE TABLE segments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    conditions JSONB NOT NULL, -- Segment rules in JSON format
    is_active BOOLEAN DEFAULT true,
    customer_count INTEGER DEFAULT 0,
    created_by VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Customer segment membership (many-to-many)
CREATE TABLE customer_segments (
    customer_id UUID REFERENCES customers(id) ON DELETE CASCADE,
    segment_id UUID REFERENCES segments(id) ON DELETE CASCADE,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (customer_id, segment_id)
);

-- Events table (customer interactions and activities)
CREATE TABLE events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    customer_id UUID REFERENCES customers(id) ON DELETE CASCADE,
    event_type VARCHAR(50) NOT NULL, -- recharge, call, sms, data_usage, etc.
    event_name VARCHAR(100) NOT NULL,
    
    -- Event data
    properties JSONB, -- Flexible event properties
    amount DECIMAL(10,2), -- For financial events
    duration INTEGER, -- For call events (seconds)
    data_volume_mb INTEGER, -- For data events
    
    -- Context
    channel VARCHAR(50), -- ussd, app, web, retail
    location_province VARCHAR(50),
    location_city VARCHAR(50),
    
    -- Metadata
    occurred_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Campaigns table
CREATE TABLE campaigns (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(200) NOT NULL,
    description TEXT,
    campaign_type VARCHAR(50) NOT NULL DEFAULT 'sms', -- sms, email, push, ussd
    
    -- Campaign configuration
    message_template TEXT NOT NULL,
    target_segment_id UUID REFERENCES segments(id),
    
    -- Scheduling
    status VARCHAR(20) DEFAULT 'draft', -- draft, scheduled, running, completed, paused
    scheduled_at TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    
    -- Performance metrics
    target_count INTEGER DEFAULT 0,
    sent_count INTEGER DEFAULT 0,
    delivered_count INTEGER DEFAULT 0,
    opened_count INTEGER DEFAULT 0,
    clicked_count INTEGER DEFAULT 0,
    converted_count INTEGER DEFAULT 0,
    
    -- Financial
    budget DECIMAL(10,2),
    cost_per_message DECIMAL(5,4),
    total_cost DECIMAL(10,2) DEFAULT 0.00,
    revenue_generated DECIMAL(12,2) DEFAULT 0.00,
    
    -- Metadata
    created_by VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Campaign interactions (tracking customer responses)
CREATE TABLE campaign_interactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    campaign_id UUID REFERENCES campaigns(id) ON DELETE CASCADE,
    customer_id UUID REFERENCES customers(id) ON DELETE CASCADE,
    
    -- Interaction details
    interaction_type VARCHAR(50) NOT NULL, -- sent, delivered, opened, clicked, converted
    occurred_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Additional data
    properties JSONB,
    
    UNIQUE(campaign_id, customer_id, interaction_type)
);

-- Offers table (products/services that can be offered to customers)
CREATE TABLE offers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(200) NOT NULL,
    description TEXT,
    offer_type VARCHAR(50) NOT NULL, -- data_bundle, voice_bundle, discount, upgrade
    
    -- Offer details
    price DECIMAL(10,2) NOT NULL,
    value DECIMAL(10,2), -- Original value for discounts
    validity_days INTEGER,
    
    -- Offer configuration
    data_mb INTEGER, -- For data bundles
    voice_minutes INTEGER, -- For voice bundles
    sms_count INTEGER, -- For SMS bundles
    discount_percentage DECIMAL(5,2), -- For discount offers
    
    -- Availability
    is_active BOOLEAN DEFAULT true,
    valid_from TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    valid_until TIMESTAMP,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Loyalty program
CREATE TABLE loyalty_points (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    customer_id UUID REFERENCES customers(id) ON DELETE CASCADE,
    
    -- Points
    points_earned INTEGER NOT NULL,
    points_spent INTEGER DEFAULT 0,
    current_balance INTEGER NOT NULL,
    
    -- Transaction details
    transaction_type VARCHAR(50) NOT NULL, -- earned, spent, expired
    description TEXT,
    reference_id UUID, -- Reference to campaign, offer, etc.
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP
);

-- System users (for RBAC)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(200),
    role VARCHAR(50) NOT NULL DEFAULT 'analyst', -- admin, manager, analyst, viewer
    is_active BOOLEAN DEFAULT true,
    
    -- Authentication (simplified for MVP)
    password_hash VARCHAR(255),
    last_login TIMESTAMP,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_customers_phone ON customers(phone_number);
CREATE INDEX idx_customers_status ON customers(status);
CREATE INDEX idx_customers_churn_score ON customers(churn_score DESC);
CREATE INDEX idx_customers_arpu ON customers(arpu_30d DESC);
CREATE INDEX idx_customers_last_activity ON customers(last_activity_at DESC);

CREATE INDEX idx_events_customer_id ON events(customer_id);
CREATE INDEX idx_events_type ON events(event_type);
CREATE INDEX idx_events_occurred_at ON events(occurred_at DESC);

CREATE INDEX idx_campaigns_status ON campaigns(status);
CREATE INDEX idx_campaigns_scheduled_at ON campaigns(scheduled_at);

CREATE INDEX idx_campaign_interactions_campaign ON campaign_interactions(campaign_id);
CREATE INDEX idx_campaign_interactions_customer ON campaign_interactions(customer_id);

-- Triggers for updated_at timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_customers_updated_at BEFORE UPDATE ON customers
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_segments_updated_at BEFORE UPDATE ON segments
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_campaigns_updated_at BEFORE UPDATE ON campaigns
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_offers_updated_at BEFORE UPDATE ON offers
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Views for common queries
CREATE VIEW customer_summary AS
SELECT 
    c.id,
    c.phone_number,
    c.first_name,
    c.last_name,
    c.customer_type,
    c.status,
    c.arpu_30d,
    c.churn_score,
    c.days_since_last_activity,
    COUNT(cs.segment_id) as segment_count,
    c.created_at,
    c.last_activity_at
FROM customers c
LEFT JOIN customer_segments cs ON c.id = cs.customer_id
GROUP BY c.id;

CREATE VIEW campaign_performance AS
SELECT 
    c.id,
    c.name,
    c.status,
    c.target_count,
    c.sent_count,
    c.delivered_count,
    c.opened_count,
    c.clicked_count,
    c.converted_count,
    CASE 
        WHEN c.sent_count > 0 THEN ROUND((c.delivered_count::DECIMAL / c.sent_count) * 100, 2)
        ELSE 0 
    END as delivery_rate,
    CASE 
        WHEN c.delivered_count > 0 THEN ROUND((c.opened_count::DECIMAL / c.delivered_count) * 100, 2)
        ELSE 0 
    END as open_rate,
    CASE 
        WHEN c.opened_count > 0 THEN ROUND((c.clicked_count::DECIMAL / c.opened_count) * 100, 2)
        ELSE 0 
    END as click_rate,
    CASE 
        WHEN c.clicked_count > 0 THEN ROUND((c.converted_count::DECIMAL / c.clicked_count) * 100, 2)
        ELSE 0 
    END as conversion_rate,
    c.total_cost,
    c.revenue_generated,
    CASE 
        WHEN c.total_cost > 0 THEN ROUND(((c.revenue_generated - c.total_cost) / c.total_cost) * 100, 2)
        ELSE 0 
    END as roi_percentage
FROM campaigns c;

-- Insert default admin user
INSERT INTO users (username, email, full_name, role, password_hash) 
VALUES ('admin', 'admin@tmcel.mz', 'System Administrator', 'admin', '$2b$12$dummy_hash_for_mvp');

-- Insert default segments
INSERT INTO segments (name, description, conditions) VALUES
('High Value Customers', 'Customers with ARPU > 1000 MZN', '{"arpu_30d": {"operator": ">", "value": 1000}}'),
('At Risk Customers', 'Customers with high churn probability', '{"churn_score": {"operator": ">", "value": 0.7}}'),
('Data Heavy Users', 'Customers using >5GB monthly', '{"total_data_mb": {"operator": ">", "value": 5120}}'),
('New Customers', 'Customers activated in last 30 days', '{"activation_date": {"operator": ">", "value": "30_days_ago"}}'),
('Prepaid Low Balance', 'Prepaid customers with balance < 50 MZN', '{"customer_type": {"operator": "=", "value": "prepaid"}, "current_balance": {"operator": "<", "value": 50}}');

-- Insert sample offers
INSERT INTO offers (name, description, offer_type, price, data_mb, validity_days) VALUES
('1GB Data Bundle', '1GB high-speed data valid for 7 days', 'data_bundle', 100.00, 1024, 7),
('5GB Data Bundle', '5GB high-speed data valid for 30 days', 'data_bundle', 400.00, 5120, 30),
('Weekend Voice Bundle', '200 minutes valid for weekends', 'voice_bundle', 150.00, NULL, 7),
('SMS Bundle 100', '100 SMS to any network', 'sms_bundle', 50.00, NULL, 30);

COMMIT;