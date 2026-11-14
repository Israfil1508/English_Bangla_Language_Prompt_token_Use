import random
import statistics


def bootstrap_mean_interval(values: list[float], confidence: float = 0.95,
                            repetitions: int = 10000, seed: int = 2026) -> tuple[float, float]:
    if not values or not 0 < confidence < 1 or repetitions < 2:
        raise ValueError("Nonempty values, valid confidence, and >=2 resamples required")
    rng = random.Random(seed)
    means = sorted(statistics.fmean(rng.choices(values, k=len(values))) for _ in range(repetitions))
    lower = int(((1 - confidence) / 2) * (repetitions - 1))
    upper = int(((1 + confidence) / 2) * (repetitions - 1))
    return means[lower], means[upper]
