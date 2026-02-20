from app.services.tier_service import TierService


def test_kernel_panic_classification():
    service = TierService()
    tier, severity, escalate = service.classify(
        "My VM shows a kernel panic stack trace"
    )

    assert tier == "TIER_2"
    assert severity == "HIGH"
    assert escalate is True


def test_login_classification():
    service = TierService()
    tier, severity, escalate = service.classify(
        "I keep getting redirected to login page"
    )

    assert tier == "TIER_0"
    assert escalate is False
