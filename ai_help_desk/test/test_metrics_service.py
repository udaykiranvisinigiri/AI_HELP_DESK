from app.services.metrics_service import MetricsService


class MockRepo:
    def get_total_sessions(self):
        return 10

    def get_total_tickets(self):
        return 3

    def get_guardrail_count(self):
        return 2

    def get_tickets_by_tier(self):
        return {"TIER_2": 3}


def test_deflection_rate_calculation():
    service = MetricsService()
    service.repo = MockRepo()

    summary = service.get_summary()

    assert summary["totalSessions"] == 10
    assert summary["totalTickets"] == 3
    assert summary["guardrailActivations"] == 2
    assert summary["deflectionRate"] == 0.7
