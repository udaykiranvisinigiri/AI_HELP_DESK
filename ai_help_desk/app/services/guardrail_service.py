class GuardrailService:

    def check(self, message: str, user_role: str):

        msg = message.lower()

        logging_patterns = [
            "disable logging",
            "turn off logging",
            "hide activity",
            "test quietly",
            "bypass monitoring"
        ]

        host_patterns = [
            "host machine",
            "hypervisor",
            "access host",
            "host os",
            "vm host access"
        ]

        destructive_patterns = [
            "reset all user environments",
            "delete all environments",
            "wipe all labs",
            "remove all users"
        ]

        override_patterns = [
            "don't escalate",
            "do not escalate",
            "skip escalation",
            "avoid escalation"
        ]

        etc_hosts_patterns = [
            "/etc/hosts",
            "modify hosts file",
            "edit hosts file"
        ]

        if any(p in msg for p in logging_patterns):
            return True, "Logging cannot be disabled as per security policy."

        if any(p in msg for p in host_patterns):
            return True, "Access to host/hypervisor is strictly prohibited."

        if any(p in msg for p in destructive_patterns):
            return True, "Destructive system-wide actions are not allowed."

        if any(p in msg for p in override_patterns):
            return True, "Escalation policy cannot be overridden."

        if any(p in msg for p in etc_hosts_patterns) and user_role.lower() in ["trainee", "instructor"]:
            return True, "Modifying system files is not allowed for your role."

        if ("time" in msg or "clock" in msg) and user_role.lower() in ["trainee", "instructor"]:
            return True, "You are not allowed to modify system time."

        return False, None
