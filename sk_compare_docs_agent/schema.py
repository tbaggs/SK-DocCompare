from pydantic import BaseModel, Field
from typing import List


class PolicyDocumentComparison(BaseModel):
    documentSimilarity: bool = Field(
        description="Indicates whether the two documents are considered similar (true) or not (false)."
    )
    documentSimilarityDescription: str = Field(
        description="Explains how the documents are similar, for example, they are both expense related policy document."
    )
    documentDifferences: List[str] = Field(
        default_factory=list,
        description="List of differences between the two documents.",
    )
    documentIntegrationSteps: List[str] = Field(
        default_factory=list,
        description="Step-by-step actions to integrate or reconcile the two documents.",
    )

    class Config:
        extra = "forbid"
