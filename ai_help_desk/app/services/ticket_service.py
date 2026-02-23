from app.repositories.ticket_repository import TicketRepository


class TicketService:

    def __init__(self):
        self.repo = TicketRepository()

    def list_tickets(self):
        return self.repo.get_all_tickets()

    def get_ticket(self, ticket_id):
        return self.repo.get_ticket_by_id(ticket_id)

    def assign_ticket(self, ticket_id, user_role):

        if user_role not in ["admin", "support_engineer"]:
            return False, "Not authorized"

        self.repo.assign_ticket(ticket_id, user_role)
        return True, "Ticket assigned"

    def close_ticket(self, ticket_id, user_role):

        if user_role not in ["admin", "support_engineer"]:
            return False, "Not authorized"

        self.repo.close_ticket(ticket_id, user_role)
        return True, "Ticket closed"