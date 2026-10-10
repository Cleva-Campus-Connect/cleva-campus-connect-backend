from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, status
from app.database import supabase
from app.dependencies import require_role
from app.schema.job_schemas import JobCreate, JobOut

router = APIRouter(prefix="/job", tags=["jobs"])

supported_currency = {"NGN", "GHS", "KES", "USD", }

@router.post("", response_model=JobOut, status_code=status.HTTP_201_CREATED)
def create_job(body:JobCreate, user:dict = Depends(require_role("freelancer"))):
    currency = body.currency.upper()
    if currency not in supported_currency:
        raise HTTPException(status_code=400, detail=f"Unsupported currency: {currency}")
    total = sum((m.amount for m in body.milestone), Decimal("0"))
    job_result = (
        supabase.table("jobs").insert({
            "freelancer_id": user["id"],
            "title": body.title,
            "description": body.description,
            "currency": currency,
            "total_amount": str(total),
            "auto_release_days": body.auto_release_days,

        }).execute()
    )
    job = job_result.data[0
    ]
    milestone_rows = [
        {
            "job_id": job["id"],
            "position":position,
            "title": m.title,
            "amount": str(m.amount),
        }
        for position, m in enumerate(body.milestone, start=1)
    ]
    try:
        milestone_result = supabase.table("milestones").insert(milestone_rows).execute()
    except Exception:
        supabase.table("jobs").delete().eq("id", job["id"]).execute()
        raise HTTPException(
            status_code=500, detail="Could not create milestone"
        )
    milestones = sorted(milestone_result.data, key=lambda m: m["position"])
    return JobOut(**job, milestones = milestones)



