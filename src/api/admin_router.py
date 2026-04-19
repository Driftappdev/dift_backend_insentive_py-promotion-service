from fastapi import APIRouter, HTTPException
from typing import List
from src.services.promotion_service import PromotionService
from src.repository.promotion_repository import PromotionRepository
from src.schemas.promotion import PromotionCreateSchema, PromotionResponseSchema
from src.domain.exceptions import PromotionNotFoundException, PromotionExpiredException

router = APIRouter(prefix="/admin", tags=["Admin Promotions"])

repo = PromotionRepository()
service = PromotionService(repo)

# -------------------------
# Create promotion
# -------------------------
@router.post("/promotions", response_model=PromotionResponseSchema)
async def create_promotion(payload: PromotionCreateSchema):
    promo = await service.create_promotion(payload)
    return promo

# -------------------------
# List all promotions
# -------------------------
@router.get("/promotions", response_model=List[PromotionResponseSchema])
async def list_promotions():
    return await service.list_promotions()

# -------------------------
# Delete promotion
# -------------------------
@router.delete("/promotions/{promo_id}")
async def delete_promotion(promo_id: str):
    try:
        await service.delete_promotion(promo_id)
        return {"promotion_id": promo_id, "message": "Promotion deleted"}
    except PromotionNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
