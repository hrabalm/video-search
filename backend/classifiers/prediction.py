from typing import Optional

from pydantic import BaseModel


class PerFramePrediction(BaseModel):
    """Output for models that classify models in isolation."""

    score: float
    label: str
    pts: Optional[int] = None


class GroupedPerFramePrediction(BaseModel):
    label: str
    predictions: list[PerFramePrediction]

    def count(self) -> int:
        return len(self.predictions)

    def best(self) -> PerFramePrediction:
        return max(self.predictions, key=lambda p: p.score)

    def best_score(self) -> float:
        return self.best().score
