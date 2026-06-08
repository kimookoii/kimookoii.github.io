import pandas as pd

from detection_agent import DetectionAgent
from analysis_agent import AnalysisAgent
from response_agent import ResponseAgent

detector = DetectionAgent()
analyzer = AnalysisAgent()
responder = ResponseAgent()

logs = pd.read_csv("logs.csv")

print("=" * 60)
print("CYBER AI ORCHESTRATOR")
print("=" * 60)

for index, row in logs.iterrows():

    user = row["user"]
    host = row["host"]
    failed_login = row["failed_login"]

    detected = detector.detect(failed_login)

    if detected:

        risk = analyzer.analyze(failed_login)

        action = responder.respond(risk)

        print(f"""
User      : {user}
Host      : {host}
Failed    : {failed_login}
Risk      : {risk}
Response  : {action}
        """)