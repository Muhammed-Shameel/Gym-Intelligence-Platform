from abc import ABC, abstractmethod
from typing import Any
from app.services.context.base import SharedWorkflowContext

class DeterministicAgent(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def run(self, context: SharedWorkflowContext) -> dict[str, Any]:
        # Return a structured deterministic output without external AI services.
        raise NotImplementedError
