class TierService:

    def classify(self, message: str, user_role: str, context=None):

        msg = message.lower()

        if "kernel panic" in msg:
            return "TIER_2", "HIGH", True

        if "vm froze" in msg or "lost my work" in msg:
            return "TIER_2", "HIGH", True

        if "container init failed" in msg or "missing /opt/startup.sh" in msg:
            return "TIER_2", "HIGH", True

        if "wrong environment" in msg or "wrong toolset" in msg:
            if user_role.lower() in ["instructor", "operator"]:
                return "TIER_2", "HIGH", True
            return "TIER_1", "MEDIUM", False

        if "login" in msg or "redirected" in msg:
            if user_role.lower() == "instructor":
                return "TIER_1", "HIGH", False
            return "TIER_0", "MEDIUM", False

        if "clock" in msg or "time drift" in msg:
            return "TIER_1", "MEDIUM", False

        if "dns" in msg or "cannot resolve" in msg:
            return "TIER_1", "MEDIUM", False

        if "reset all user environments" in msg:
            return "TIER_2", "HIGH", True

        return "TIER_0", "LOW", False
