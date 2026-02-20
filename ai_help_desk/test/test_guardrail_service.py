from app.services.guardrail_service import GuardrailService


def test_block_disable_logging():
    service = GuardrailService()
    blocked, reason = service.check("How do I disable logging?")

    assert blocked is True
    assert "disable logging" in reason.lower()


def test_allow_normal_question():
    service = GuardrailService()
    blocked, reason = service.check("Login not working")

    assert blocked is False
    assert reason is None
