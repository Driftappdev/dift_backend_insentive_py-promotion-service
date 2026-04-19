from fastapi import APIRouter, HTTPException
from typing import List
from src.services.promotion_service import PromotionService
from src.repository.promotion_repository import PromotionRepository
from src.schemas.promotion import PromotionCreateSchema, PromotionResponseSchema
from src.domain.exceptions import PromotionNotFoundException

router = APIRouter(tags=["Promotions"])

repo = PromotionRepository()
service = PromotionService(repo)

# -------------------------
# List all active promotions
# -------------------------
@router.get("/", response_model=List[PromotionResponseSchema])
async def list_promotions():
    return await service.list_promotions()

# -------------------------
# Apply a promotion to a user / feature
# -------------------------
@router.post("/apply/{promo_id}")
async def apply_promotion(promo_id: str, user_data: dict):
    try:
        discount = await service.apply_promotion(promo_id, user_data)
        return {"promotion_id": promo_id, "discount": discount}
    except PromotionNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
