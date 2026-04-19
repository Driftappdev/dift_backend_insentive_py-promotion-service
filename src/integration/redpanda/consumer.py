import asyncio
import json
from aiokafka import AIOKafkaConsumer
from src.logger.logger import logger

class RedpandaConsumer:
    def __init__(self, bootstrap_servers: str, topic: str, group_id: str = "promotion_service"):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.group_id = group_id
        self.consumer: AIOKafkaConsumer = None
        self.running = False

    async def start(self):
        """
        Initialize Kafka/Redpanda consumer
        """
        self.consumer = AIOKafkaConsumer(
            self.topic,
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id,
            value_deserializer=lambda v: json.loads(v.decode('utf-8'))
        )
        await self.consumer.start()
        self.running = True
        logger.info(f"Redpanda consumer started for topic {self.topic}")

    async def stop(self):
        """
        Stop Kafka/Redpanda consumer
        """
        if self.consumer:
            self.running = False
            await self.consumer.stop()
            logger.info(f"Redpanda consumer stopped for topic {self.topic}")

    async def consume(self, callback):
        """
        Consume messages and call callback(message)
        """
        if not self.consumer:
            await self.start()

        try:
            async for msg in self.consumer:
                message = msg.value
                logger.info(f"Consumed message from {self.topic}: {message}")
                await callback(message)
                if not self.running:
                    break
        except Exception as e:
            logger.error(f"Error consuming from {self.topic}: {e}")
        finally:
            await self.stop()
