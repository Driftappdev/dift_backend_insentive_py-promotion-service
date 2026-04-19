from src.db.mongo import db
from contextlib import asynccontextmanager
from src.logger.logger import logger

class UnitOfWork:
    """
    Unit of Work pattern for MongoDB (placeholder for future transaction support)
    """
    def __init__(self, collection_name: str):
        self.collection = db[collection_name]

    @asynccontextmanager
    async def start(self):
        """
        Async context manager placeholder
        """
        try:
            # ถ้าใช้ multi-document transaction, สามารถ start session ที่นี่
            yield self.collection
            # ถ้า commit transaction, ทำที่นี่
        except Exception as e:
            logger.error(f"UnitOfWork rollback due to: {e}")
            # ถ้าใช้ transaction, rollback
            raise
