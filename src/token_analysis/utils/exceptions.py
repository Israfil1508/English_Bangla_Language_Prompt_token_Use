class ExperimentError(Exception):
    """Base exception for experiment failures."""

class DatasetError(ExperimentError):
    """Raised for malformed paired datasets."""

class ModelResponseError(ExperimentError):
    """Raised when Ollama supplies invalid or incomplete metadata."""
