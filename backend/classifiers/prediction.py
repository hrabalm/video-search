from typing import Optional

from pydantic import BaseModel


class Prediction(BaseModel):
    score: float
    label: str
    pts: Optional[int] = None


class GroupedPrediction(BaseModel):
    label: str
    predictions: list[Prediction]

    def count(self) -> int:
        return len(self.predictions)

    def best(self) -> Prediction:
        return max(self.predictions, key=lambda p: p.score)

    def best_score(self) -> float:
        return self.best().score
