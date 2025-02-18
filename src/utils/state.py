from enum import Enum
from dataclasses import dataclass

class TaskStatus(Enum):
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class GenerationState:
    status: TaskStatus
    progress: float
    message: str 