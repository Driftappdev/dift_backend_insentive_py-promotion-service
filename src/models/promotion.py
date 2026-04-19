from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class ConditionModel(BaseModel):
    type: str
    value: str

class PromotionModel(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    name: str
    discount: float
    discount_type: str = "percentage"
    start_date: datetime
    end_date: datetime
    is_active: bool = True
    conditions: List[ConditionModel] = []
    cross_feature: List[str] = []

    class Config:
        allow_population_by_field_name = True
