from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.promotion_router import router as promotion_router
from src.config.config import settings
from src.logger.logger import logger
from src.integration.redpanda.publisher import RedpandaPublisher
from src.integration.cache.cache import redis

# -------------------------
# Create FastAPI app
# -------------------------
app = FastAPI(
    title=settings.app_name,
    docs_url="/docs" if settings.service_api.docs_enabled else None,
)

# -------------------------
# CORS (for Admin Panel / frontend)
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Include Promotion Router
# -------------------------
app.include_router(promotion_router, prefix="/promotions", tags=["Promotions"])

# -------------------------
# Startup / Shutdown Events
# -------------------------
@app.on_event("startup")
async def startup_event():
    logger.info("Starting Promotion Service...")
    # Connect Redis
    await redis.ping()
    logger.info("Redis connected")
    # Initialize Redpanda publisher
    app.state.redpanda = RedpandaPublisher(settings.redpanda.bootstrap_servers)
    await app.state.redpanda.start()

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down Promotion Service...")
    # Close Redpanda publisher
    await app.state.redpanda.stop()
    # Close Redis if needed
    await redis.close()
