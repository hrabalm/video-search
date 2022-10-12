from pydantic import BaseModel


class Prediction(BaseModel):
    score: float
    label: str
    # TODO: add frame index


class GroupedPrediction(BaseModel):
    label: str
    predictions: list[Prediction]

    def count(self) -> int:
        return len(self.predictions)

    def best_score(self) -> float:
        return float(max(p.score for p in self.predictions))
