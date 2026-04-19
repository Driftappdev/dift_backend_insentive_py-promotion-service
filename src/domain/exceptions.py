from src.logger.logger import logger

class PromotionException(Exception):
    """Base class for promotion-related exceptions"""
    def __init__(self, message: str):
        super().__init__(message)
        logger.error(f"PromotionException: {message}")

class PromotionNotFoundException(PromotionException):
    """Raised when a promotion is not found"""
    pass

class PromotionExpiredException(PromotionException):
    """Raised when a promotion is expired"""
    pass

class PromotionNotEligibleException(PromotionException):
    """Raised when a promotion is not eligible for the user or feature"""
    pass

class PromotionAlreadyAppliedException(PromotionException):
    """Raised when a promotion has already been applied"""
    pass
