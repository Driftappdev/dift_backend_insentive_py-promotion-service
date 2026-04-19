import asyncio
import json
from aiokafka import AIOKafkaProducer
from src.logger.logger import logger

class RedpandaPublisher:
    def __init__(self, bootstrap_servers: str):
        self.bootstrap_servers = bootstrap_servers
        self.producer: AIOKafkaProducer = None

    async def start(self):
        """
        Initialize Kafka/Redpanda producer
        """
        self.producer = AIOKafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        await self.producer.start()
        logger.info("Redpanda producer started")

    async def stop(self):
        """
        Stop Kafka/Redpanda producer
        """
        if self.producer:
            await self.producer.stop()
            logger.info("Redpanda producer stopped")

    async def publish(self, topic: str, message: dict):
        """
        Publish message to topic
        """
        if not self.producer:
            await self.start()
        try:
            await self.producer.send_and_wait(topic, message)
            logger.info(f"Published message to {topic}: {message}")
        except Exception as e:
            logger.error(f"Failed to publish message to {topic}: {e}")
