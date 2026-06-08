class DetectionAgent:

    def detect(self, failed_login):
        if failed_login >= 5:
            return True
        return False