from token_analysis.analysis.bootstrap import bootstrap_mean_interval


def test_bootstrap_deterministic():
    values = [1.0, 2.0, 3.0, 4.0]
    a = bootstrap_mean_interval(values, repetitions=100, seed=11)
    assert a == bootstrap_mean_interval(values, repetitions=100, seed=11)
    assert a[0] <= 2.5 <= a[1]
