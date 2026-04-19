# Central Coupon Service

ระบบคูปองแบบ Centralized สำหรับใช้ร่วมกับหลาย Service เช่น Travel Service

## Features
- CRUD คูปอง
- Async PostgreSQL + SQLAlchemy
- FastAPI REST API
- Validation ด้วย Pydantic
- Logging พร้อมใช้งาน Production
- Alembic Migration

## Run Locally
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
