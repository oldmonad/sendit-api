from enum import Enum


class Status(Enum):
    PENDING = "pending"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
