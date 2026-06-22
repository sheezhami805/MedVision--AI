def generate_alert(result, fraud_score, department):

    if result == "Fraud":

        return f"""
🚨 HIGH RISK FRAUD ALERT

Department: {department}

Risk Score: {fraud_score:.2f}%

Immediate investigation recommended.
"""

    return None