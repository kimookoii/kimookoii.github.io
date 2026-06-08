class ResponseAgent:

    def respond(self, risk):

        if risk == "LOW":
            return "Monitoring"

        elif risk == "MEDIUM":
            return "Send Warning"

        elif risk == "HIGH":
            return "Reset Password"

        elif risk == "CRITICAL":
            return "Isolate Host & Notify SOC"