from app.repositories.metrics_repository import MetricsRepository


class MetricsService:

    def __init__(self):
        self.repo = MetricsRepository()

    def get_summary(self):

        total_sessions = self.repo.get_total_sessions()
        total_tickets = self.repo.get_total_tickets()
        guardrail_count = self.repo.get_guardrail_count()
        tickets_by_tier = self.repo.get_tickets_by_tier()

        deflection_rate = 0.0
        if total_sessions > 0:
            deflection_rate = round(
                (total_sessions - total_tickets) / total_sessions,
                2
            )

        return {
            "totalSessions": total_sessions,
            "totalTickets": total_tickets,
            "guardrailActivations": guardrail_count,
            "deflectionRate": deflection_rate,
            "ticketsByTier": tickets_by_tier
        }
