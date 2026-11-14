from token_analysis.experiment.cache_controller import caching_protocol


def test_protocol_does_not_claim_cold_cache():
    assert "cannot be guaranteed cold" in caching_protocol()
