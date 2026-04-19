from datetime import datetime
from typing import List
from pydantic import BaseModel, Field
from src.schemas.promotion import ConditionSchema

class PromotionModel(BaseModel):
    id: str = Field(None, alias="_id")
    name: str
    discount: float
    discount_type: str = "percentage"
    start_date: datetime
    end_date: datetime
    is_active: bool = True
    conditions: List[ConditionSchema] = []
    cross_feature: List[str] = []

    class Config:
        allow_population_by_field_name = True

    # -------------------------
    # Check if promotion is currently valid
    # -------------------------
    def is_valid(self) -> bool:
        now = datetime.utcnow()
        return self.is_active and self.start_date <= now <= self.end_date

    # -------------------------
    # Check if promotion can be applied to a specific feature
    # -------------------------
    def can_apply_to_feature(self, feature_name: str) -> bool:
        if not self.cross_feature:
            return True  # applies to all features if list is empty
        return feature_name in self.cross_feature
