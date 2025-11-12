"""Advisor Council for multi-advisor reviews."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Literal, Optional

from src.core.base import BaseAdvisor
from src.core.types import AgentOutput, AdvisorReview

DecisionMode = Literal["majority", "average"]


@dataclass
class AdvisorCouncil:
    """Run multiple advisors and aggregate decisions."""

    advisor_factory: Callable[[str], BaseAdvisor]
    advisors: List[str]
    decision: DecisionMode = "majority"
    min_score: float = 0.85
    name: str = "AdvisorCouncil"
    weights: Optional[Dict[str, float]] = None  # Advisor name -> weight

    def review(
        self, output: AgentOutput, task: str, context: Dict[str, Any]
    ) -> AdvisorReview:
        """Review output using multiple advisors and aggregate results."""
        reviews: List[AdvisorReview] = []
        for name in self.advisors:
            adv = self.advisor_factory(name)
            reviews.append(adv.review(output=output, task=task, context=context))

        # Aggregate
        approved_votes = sum(
            1 for r in reviews if r["approved"] and r["score"] >= self.min_score
        )
        if self.decision == "average":
            # Apply weights if provided
            if self.weights:
                weighted_sum = 0.0
                total_weight = 0.0
                for r, name in zip(reviews, self.advisors):
                    weight = float(self.weights.get(name, 1.0))
                    weighted_sum += weight * float(r["score"])
                    total_weight += weight
                avg_score = (weighted_sum / total_weight) if total_weight > 0 else sum(r["score"] for r in reviews) / max(1, len(reviews))
            else:
                avg_score = sum(r["score"] for r in reviews) / max(1, len(reviews))
            approved = avg_score >= self.min_score
        else:  # majority
            avg_score = sum(r["score"] for r in reviews) / max(1, len(reviews))
            approved = approved_votes > (len(reviews) // 2)

        # Flatten issues/suggestions (cap to keep it readable)
        critical = [i for r in reviews for i in r["critical_issues"]][:10]
        suggestions = [s for r in reviews for s in r["suggestions"]][:10]
        severity = "low"
        if critical:
            severity = "high" if len(critical) >= 5 else "medium"

        return {
            "score": round(avg_score, 2),
            "approved": approved,
            "critical_issues": critical,
            "suggestions": suggestions,
            "summary": f"Council decision via {self.decision}: {approved_votes}/{len(reviews)} approvals; avg={avg_score:.2f}",
            "severity": severity,
        }

    def gate(self, review: AdvisorReview, min_score: float) -> bool:
        """
        Gate decision: pass if approved and score >= min_score.
        
        Compatible with BaseAdvisor.gate() interface.
        """
        return review["approved"] and review["score"] >= min_score

