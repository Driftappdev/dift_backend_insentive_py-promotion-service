from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

# -------------------------
# Condition Schema
# -------------------------
class ConditionSchema(BaseModel):
    type: str           # user_type, min_order, category, etc.
    value: str

# -------------------------
# Promotion Create Schema
# -------------------------
class PromotionCreateSchema(BaseModel):
    name: str
    discount: float
    discount_type: str = "percentage"          # default percentage
    start_date: datetime
    end_date: datetime
    conditions: List[ConditionSchema] = []     # optional conditions
    cross_feature: List[str] = []              # features / services allowed
    is_active: bool = True

# -------------------------
# Promotion Update Schema
# -------------------------
class PromotionUpdateSchema(BaseModel):
    name: Optional[str]
    discount: Optional[float]
    discount_type: Optional[str]
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    conditions: Optional[List[ConditionSchema]]
    cross_feature: Optional[List[str]]
    is_active: Optional[bool]

# -------------------------
# Promotion Response Schema
# -------------------------
class PromotionResponseSchema(BaseModel):
    id: str = Field(..., alias="_id")         # MongoDB ObjectId
    name: str
    discount: float
    discount_type: str
    start_date: datetime
    end_date: datetime
    conditions: List[ConditionSchema] = []
    cross_feature: List[str] = []
    is_active: bool

    class Config:
        allow_population_by_field_name = True
