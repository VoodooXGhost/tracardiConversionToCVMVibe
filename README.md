# EngageHub - CVM Platform for Tmcel

A Customer Value Management (CVM) platform built for Tmcel, leveraging the existing Tracardi CDP foundation.

## 🎯 MVP Features

### 1. **Unified Customer Data View**
- Consolidated customer profiles from multiple data sources
- Real-time customer 360° view with telco-specific metrics
- Clean, normalized customer data with ARPU, usage patterns, and churn indicators

### 2. **AI-Powered Churn Prediction**
- Machine learning model predicting customer churn probability
- Risk scoring based on usage patterns, payment history, and engagement
- Proactive identification of at-risk customers

### 3. **Dynamic Customer Segmentation**
- Visual segment builder with drag-and-drop interface
- Real-time segment population counts
- Telco-specific segments (prepaid/postpaid, data users, high-value customers)

### 4. **No-Code Campaign Designer**
- Intuitive campaign builder for SMS marketing
- Template-based message creation
- Audience targeting with segment integration

### 5. **Automated Campaign Triggering**
- Rule-based campaign automation
- Scheduled campaign execution
- Event-triggered campaigns (low balance, data expiry)

### 6. **Real-Time Monitoring & Reporting**
- Live dashboard with key CVM metrics
- Campaign performance tracking
- Customer behavior analytics and churn rate monitoring

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   Database      │
│   (React/TS)    │◄──►│   (FastAPI)     │◄──►│  (PostgreSQL)   │
│   + Tailwind    │    │   + ML Models   │    │   + Redis       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Tech Stack
- **Frontend**: React 18 + TypeScript + Tailwind CSS + Vite
- **Backend**: Python 3.9+ + FastAPI + SQLAlchemy + Pydantic
- **Database**: PostgreSQL 14+ + Redis (caching)
- **ML**: scikit-learn + pandas + numpy
- **Real-time**: WebSockets for live updates

## 🚀 Quick Start

### 🐳 Docker Setup (Recommended for Windows)

#### Prerequisites
- Docker Desktop for Windows
- 4GB+ RAM available for Docker

#### One-Click Launch
```batch
# Double-click or run from command prompt
launch-engagehub.bat
```

**That's it!** The script will:
- ✅ Check Docker availability
- 🏗️ Build all containers (first run only)
- 🗄️ Setup PostgreSQL database
- 📊 Generate 10,000+ demo customers
- 🚀 Launch all services
- 🌐 Open EngageHub in your browser

#### Docker Management
```batch
# Stop all services
stop-engagehub.bat

# Reset all data and start fresh
reset-engagehub.bat

# View logs
docker-compose logs -f

# Manual commands
docker-compose up -d      # Start services
docker-compose down       # Stop services
docker-compose down -v    # Stop and remove all data
```

### 🛠️ Manual Setup (Development)

#### Prerequisites
- Python 3.9+
- Node.js 18+
- PostgreSQL 14+
- Redis (optional, for caching)

#### Automated Setup
```bash
# Make setup script executable (Linux/Mac)
chmod +x setup.sh

# Run setup script
./setup.sh
```

#### Manual Setup Steps

##### 1. Database Setup
```bash
# Create PostgreSQL database
createdb cvm_tmcel

# Run database initialization
psql -d cvm_tmcel -f db/init.sql
```

##### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Generate mock data
python generate_mock_data.py

# Start the server
uvicorn main:app --reload --port 8000
```

##### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### 🌐 Access Points

| Service | URL | Description |
|---------|-----|-------------|
| **EngageHub Frontend** | http://localhost:2020 | Main application interface |
| **Backend API** | http://localhost:3030 | REST API endpoints |
| **API Documentation** | http://localhost:3030/docs | Interactive API docs |
| **Database** | localhost:5432 | PostgreSQL database |
| **Redis Cache** | localhost:6379 | Redis cache server |

### 🔐 Demo Credentials
- **Username**: `admin`
- **Password**: `admin`

## 📊 Demo Data

The system includes comprehensive mock data representing:
- **10,000 customers** with realistic telco profiles
- **50,000 events** (recharges, data usage, calls)
- **Campaign history** with performance metrics
- **Churn predictions** based on behavioral patterns

### Sample Customer Segments
- **High-Value Customers**: ARPU > 1000 MZN
- **At-Risk Customers**: Churn score > 0.7
- **Data Heavy Users**: >5GB monthly usage
- **Prepaid Low Balance**: Balance < 50 MZN
- **New Customers**: Activated in last 30 days

## 🎨 UI/UX Highlights

### Dashboard
- Clean, executive-friendly interface
- Real-time KPI widgets
- Interactive charts and graphs
- Mobile-responsive design

### Campaign Builder
- Drag-and-drop campaign flow
- Visual segment selection
- Message template library
- A/B testing setup (mocked)

### Customer 360°
- Comprehensive customer profiles
- Interaction history timeline
- Predictive insights
- Segment membership

## 📈 Key Metrics Tracked

### Business KPIs
- **Customer Churn Rate**: Monthly churn percentage
- **ARPU**: Average Revenue Per User
- **Customer Lifetime Value**: Predicted CLV
- **Campaign ROI**: Revenue generated vs. cost

### Operational Metrics
- **Segment Population**: Real-time segment sizes
- **Campaign Performance**: Open rates, conversion rates
- **System Health**: API response times, data freshness

## 🔧 Configuration

### Environment Variables
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost/cvm_tmcel
REDIS_URL=redis://localhost:6379

# ML Models
CHURN_MODEL_PATH=./models/churn_model.pkl
NBO_MODEL_PATH=./models/nbo_model.pkl

# Campaign Settings
SMS_GATEWAY_URL=https://api.sms-gateway.com
SMS_API_KEY=your_api_key_here

# Feature Flags
ENABLE_REAL_SMS=false
ENABLE_ML_PREDICTIONS=true
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest tests/ -v
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 📁 Project Structure

```
cvm-tmcel-mvp/
├── frontend/                 # React TypeScript frontend
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/          # Main application pages
│   │   ├── hooks/          # Custom React hooks
│   │   ├── services/       # API service layer
│   │   └── types/          # TypeScript type definitions
│   ├── public/             # Static assets
│   └── package.json
├── backend/                  # FastAPI Python backend
│   ├── app/
│   │   ├── api/            # API route handlers
│   │   ├── core/           # Core business logic
│   │   ├── models/         # Database models
│   │   ├── schemas/        # Pydantic schemas
│   │   └── services/       # Business services
│   ├── ml_models/          # Machine learning models
│   └── requirements.txt
├── db/                      # Database scripts and migrations
│   ├── init.sql            # Database initialization
│   └── seed_data.sql       # Mock data insertion
├── docs/                    # Documentation
│   ├── CDP_Analysis.md     # Analysis of existing CDP
│   └── architecture.md     # System architecture
└── README.md               # This file
```

## 🎯 Next Steps (Post-MVP)

### Phase 2 Enhancements
1. **Advanced ML Models**: Deep learning for better predictions
2. **Multi-channel Campaigns**: Email, push notifications, USSD
3. **Real-time Personalization**: Dynamic offer optimization
4. **Advanced Analytics**: Cohort analysis, customer journey mapping

### Phase 3 Production
1. **Scalability**: Kubernetes deployment, load balancing
2. **Security**: OAuth2, role-based access control
3. **Integration**: Real Tmcel systems integration
4. **Monitoring**: Comprehensive logging and alerting

## 🤝 Contributing

This is a prototype for board presentation. For production development:
1. Follow the existing code patterns
2. Add comprehensive tests
3. Update documentation
4. Consider security implications

## 📄 License

Proprietary - Tmcel Internal Use Only

---

**Built for Tmcel Board Presentation** | **Powered by Tracardi CDP Foundation**