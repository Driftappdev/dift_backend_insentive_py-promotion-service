from typing import List
from bson import ObjectId
from src.db.mongo import db
from src.models.promotion_model import PromotionModel
from src.domain.exceptions import PromotionNotFoundException

class PromotionRepository:
    def __init__(self):
        self.collection = db.promotions

    # -------------------------
    # Create
    # -------------------------
    async def add(self, promo: PromotionModel) -> PromotionModel:
        result = await self.collection.insert_one(promo.dict(by_alias=True))
        promo.id = str(result.inserted_id)
        return promo

    # -------------------------
    # List all
    # -------------------------
    async def list(self) -> List[PromotionModel]:
        cursor = self.collection.find()
        return [PromotionModel(**doc) async for doc in cursor]

    # -------------------------
    # Get by ID
    # -------------------------
    async def get_by_id(self, promo_id: str) -> PromotionModel:
        doc = await self.collection.find_one({"_id": ObjectId(promo_id)})
        if not doc:
            raise PromotionNotFoundException(f"Promotion {promo_id} not found")
        return PromotionModel(**doc)

    # -------------------------
    # Update by ID
    # -------------------------
    async def update(self, promo_id: str, data: dict) -> PromotionModel:
        result = await self.collection.update_one(
            {"_id": ObjectId(promo_id)},
            {"$set": data}
        )
        if result.matched_count == 0:
            raise PromotionNotFoundException(f"Promotion {promo_id} not found")
        # Return updated promotion
        return await self.get_by_id(promo_id)

    # -------------------------
    # Soft delete (disable)
    # -------------------------
    async def disable(self, promo_id: str) -> PromotionModel:
        return await self.update(promo_id, {"is_active": False})
