"""Utility for loading pre-defined Golden Datasets for Mock Mode."""
from typing import Any

GOLDEN_DATASETS: dict[str, dict[str, Any]] = {
    "axial_flair": {
        "plane": "Axial",
        "sequence": "FLAIR",
        "depth": 0.45,
        "plane_conf": 0.99,
        "sequence_conf": 0.98,
        "depth_conf": 0.97,
        "narrative": (
            "Positive for hyperintense signal in the periventricular white matter, "
            "consistent with chronic small vessel ischemic changes. No acute "
            "intracranial hemorrhage or mass effect identified."
        ),
        "confidence": 0.99,
        "logs": [
            {
                "stage": "ID",
                "event": "PLANE_SEQUENCE_DETECTION",
                "model_id": "model_axial_cnn",
                "outcome": "Axial-FLAIR",
                "confidence": 0.99,
                "metadata": {"depth": 0.45}
            },
            {
                "stage": "GATE",
                "event": "INFERENCE_ROUTING",
                "model_id": "logic_gate",
                "outcome": "VLM_REQUIRED",
                "confidence": 1.0,
                "metadata": {"reason": "Axial-FLAIR detected"}
            },
            {
                "stage": "SYNTHESIS",
                "event": "NARRATIVE_GENERATION",
                "model_id": "model_medgemma_vlm",
                "outcome": "NARRATIVE_PRODUCED",
                "confidence": 0.95,
                "metadata": {"tokens": 42}
            }
        ]
    },
    "sagittal_t1": {
        "plane": "Sagittal",
        "sequence": "T1",
        "depth": 0.12,
        "plane_conf": 0.97,
        "sequence_conf": 0.95,
        "depth_conf": 0.90,
        "narrative": None,
        "confidence": 0.97,
        "logs": [
            {
                "stage": "ID",
                "event": "PLANE_SEQUENCE_DETECTION",
                "model_id": "model_axial_cnn",
                "outcome": "Sagittal-T1",
                "confidence": 0.97,
                "metadata": {"depth": 0.12}
            },
            {
                "stage": "GATE",
                "event": "INFERENCE_ROUTING",
                "model_id": "logic_gate",
                "outcome": "VLM_SKIPPED",
                "confidence": 1.0,
                "metadata": {"reason": "Non-Axial-FLAIR sequence"}
            }
        ]
    }
}

def get_mock_results(dataset_id: str) -> dict[str, Any]:
    """
    Retrieve mock results for a given dataset ID.

    Args:
        dataset_id: The unique identifier for the golden dataset.

    Returns:
        A dictionary containing the mock results.

    Raises:
        ValueError: If the dataset_id is not found in GOLDEN_DATASETS.
    """
    if dataset_id not in GOLDEN_DATASETS:
        raise ValueError(f"Unknown dataset ID: {dataset_id}")
    return GOLDEN_DATASETS[dataset_id]
