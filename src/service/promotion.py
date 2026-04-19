from datetime import datetime
from typing import List
from src.repository.promotion_repository import PromotionRepository
from src.models.promotion_model import PromotionModel
from src.domain.exceptions import PromotionNotEligibleException, PromotionNotFoundException
from src.integration.redpanda.publisher import RedpandaPublisher
from src.config.config import settings

class PromotionService:
    def __init__(self, repo: PromotionRepository):
        self.repo = repo
        self.publisher = RedpandaPublisher(settings.redpanda_bootstrap_servers)

    # -------------------------
    # CRUD Promotions
    # -------------------------
    async def create_promotion(self, promo: PromotionModel) -> PromotionModel:
        """
        Create promotion and publish event
        """
        promo = await self.repo.add(promo)
        # Publish event for other services (cross-feature)
        await self.publisher.publish("promotion_events", promo.dict())
        return promo

    async def list_promotions(self) -> List[PromotionModel]:
        return await self.repo.list()

    async def get_promotion(self, promo_id: str) -> PromotionModel:
        return await self.repo.get_by_id(promo_id)

    async def update_promotion(self, promo_id: str, data: dict) -> PromotionModel:
        """
        Update promotion and publish event
        """
        updated_promo = await self.repo.update(promo_id, data)
        await self.publisher.publish("promotion_events", {"event": "promotion_updated", "id": promo_id})
        return updated_promo

    async def delete_promotion(self, promo_id: str):
        """
        Soft delete promotion (set is_active=False)
        """
        await self.update_promotion(promo_id, {"is_active": False})
        await self.publisher.publish("promotion_events", {"event": "promotion_disabled", "id": promo_id})

    # -------------------------
    # Apply Promotion (single)
    # -------------------------
    async def apply_promotion(self, promo_id: str, user_data: dict) -> float:
        """
        Apply a single promotion to user data
        """
        promo = await self.get_promotion(promo_id)

        # Validate active and date
        now = datetime.now()
        if not promo.is_active or not (promo.start_date <= now <= promo.end_date):
            raise PromotionNotEligibleException("Promotion is not active or expired")

        # Validate conditions
        if not self._validate_conditions(promo, user_data):
            raise PromotionNotEligibleException("Promotion conditions not met")

        # Calculate discount
        return self._calculate_discount(promo, user_data)

    # -------------------------
    # Apply Promotions Cross-Feature
    # -------------------------
    async def apply_promotions_auto(self, feature: str, user_data: dict) -> float:
        """
        Auto-apply all active promotions for a specific feature
        """
        promos = await self.repo.list()
        total_discount = 0
        now = datetime.now()

        for promo in promos:
            if feature not in promo.cross_feature or not promo.is_active:
                continue
            if not (promo.start_date <= now <= promo.end_date):
                continue
            if not self._validate_conditions(promo, user_data):
                continue
            total_discount += self._calculate_discount(promo, user_data)

        return total_discount

    # -------------------------
    # Helper Methods
    # -------------------------
    def _validate_conditions(self, promo: PromotionModel, user_data: dict) -> bool:
        """
        Check all conditions for a promotion
        """
        for cond in promo.conditions:
            if cond.type == "user_type" and user_data.get("type") != cond.value:
                return False
            if cond.type == "min_order" and user_data.get("total", 0) < float(cond.value):
                return False
            if cond.type == "category" and cond.value not in user_data.get("categories", []):
                return False
        return True

    def _calculate_discount(self, promo: PromotionModel, user_data: dict) -> float:
        """
        Calculate discount based on type
        """
        total = user_data.get("total", 0)
        if promo.discount_type == "percentage":
            return total * promo.discount / 100
        elif promo.discount_type == "fixed":
            return promo.discount
        return 0.0
