from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from typing import Optional, List
import uuid

from ..core.database import get_db
from ..models import Customer
from ..schemas import (
    CustomerCreate, CustomerUpdate, CustomerResponse, CustomerSummary,
    CustomerListResponse, CustomerMetrics
)
from ..services.customer_service import CustomerService

router = APIRouter()

@router.get("/", response_model=CustomerListResponse)
async def get_customers(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    customer_type: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    risk_level: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    """Get paginated list of customers with optional filtering"""
    service = CustomerService(db)
    return await service.get_customers(
        page=page,
        page_size=page_size,
        search=search,
        customer_type=customer_type,
        status=status,
        risk_level=risk_level
    )

@router.get("/metrics", response_model=CustomerMetrics)
async def get_customer_metrics(db: AsyncSession = Depends(get_db)):
    """Get customer metrics for dashboard"""
    service = CustomerService(db)
    return await service.get_customer_metrics()

@router.get("/{customer_id}", response_model=CustomerResponse)
async def get_customer(customer_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """Get customer by ID"""
    service = CustomerService(db)
    customer = await service.get_customer_by_id(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.post("/", response_model=CustomerResponse)
async def create_customer(customer: CustomerCreate, db: AsyncSession = Depends(get_db)):
    """Create new customer"""
    service = CustomerService(db)
    return await service.create_customer(customer)

@router.put("/{customer_id}", response_model=CustomerResponse)
async def update_customer(
    customer_id: uuid.UUID,
    customer_update: CustomerUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update customer"""
    service = CustomerService(db)
    customer = await service.update_customer(customer_id, customer_update)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.delete("/{customer_id}")
async def delete_customer(customer_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """Delete customer"""
    service = CustomerService(db)
    success = await service.delete_customer(customer_id)
    if not success:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"message": "Customer deleted successfully"}

@router.get("/{customer_id}/events")
async def get_customer_events(
    customer_id: uuid.UUID,
    limit: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db)
):
    """Get customer events/activities"""
    service = CustomerService(db)
    events = await service.get_customer_events(customer_id, limit)
    return {"customer_id": customer_id, "events": events}

@router.post("/{customer_id}/predict-churn")
async def predict_customer_churn(customer_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """Predict churn for specific customer"""
    service = CustomerService(db)
    prediction = await service.predict_churn(customer_id)
    if prediction is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return prediction

@router.get("/{customer_id}/next-best-offer")
async def get_next_best_offer(customer_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """Get next best offer for customer"""
    service = CustomerService(db)
    offer = await service.get_next_best_offer(customer_id)
    if not offer:
        raise HTTPException(status_code=404, detail="No suitable offer found")
    return offer