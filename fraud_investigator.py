def investigate_claim(
    fraud_score,
    department,
    insurance,
    cost
):

    findings = []

    if cost > 5000:
        findings.append(
            "Cost significantly exceeds normal billing range."
        )

    if insurance == "Yes":
        findings.append(
            "Insurance involvement increases audit sensitivity."
        )

    if department in [
        "ICU",
        "Cardiology",
        "Radiology"
    ]:
        findings.append(
            f"{department} has elevated fraud monitoring priority."
        )

    if fraud_score >= 80:
        risk = "🔴 Critical"

    elif fraud_score >= 60:
        risk = "🟠 High"

    elif fraud_score >= 40:
        risk = "🟡 Moderate"

    else:
        risk = "🟢 Low"

    return findings, risk