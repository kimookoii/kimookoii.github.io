class AnalysisAgent:

    def analyze(self, failed_login):

        if failed_login < 5:
            return "LOW"

        elif failed_login < 10:
            return "MEDIUM"

        elif failed_login < 15:
            return "HIGH"

        else:
            return "CRITICAL"