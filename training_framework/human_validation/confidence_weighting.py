import numpy as np
import logging
from typing import List, Tuple

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class ConfidenceWeighting:
    """
    Assigns confidence weights to model predictions, incorporating human feedback when available.
    """

    def __init__(self, model_confidence: List[float], human_feedback: List[Tuple[str, float]] = None):
        """
        Initializes the confidence weighting mechanism.

        Args:
            model_confidence (List[float]): List of model prediction confidences.
            human_feedback (List[Tuple[str, float]]): Optional human feedback in the form of (sample_id, confidence_score).
        """
        self.model_confidence = np.array(model_confidence)
        self.human_feedback = dict(human_feedback) if human_feedback else {}

    def apply_weights(self, sample_ids: List[str]) -> np.ndarray:
        """
        Computes final confidence scores, adjusting for human input if available.

        Args:
            sample_ids (List[str]): List of sample identifiers.

        Returns:
            np.ndarray: Final adjusted confidence scores.
        """
        final_confidences = []
        for idx, sample_id in enumerate(sample_ids):
            model_score = self.model_confidence[idx]
            human_score = self.human_feedback.get(sample_id, model_score)
            final_score = (0.7 * model_score) + (0.3 * human_score)
            final_confidences.append(final_score)
            logging.info(f"Sample {sample_id}: Model={model_score:.4f}, Human={human_score:.4f}, Final={final_score:.4f}")

        return np.array(final_confidences)


if __name__ == "__main__":
    sample_ids = ["sample_001", "sample_002", "sample_003"]
    model_confidences = [0.85, 0.60, 0.30]
    human_feedback = [("sample_002", 0.90), ("sample_003", 0.50)]

    weighting_system = ConfidenceWeighting(model_confidence=model_confidences, human_feedback=human_feedback)
    final_scores = weighting_system.apply_weights(sample_ids)
    logging.info(f"Final adjusted confidence scores: {final_scores}")
