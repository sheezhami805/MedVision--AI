def generate_executive_report(
    result,
    fraud_score,
    department,
    insurance
):

    if result == "Fraud":

        return f"""
The claim was analyzed by the MedVision AI Fraud Intelligence Engine.

The claim received a fraud risk score of {fraud_score:.2f}%.

The selected department is {department} and the insurance status is {insurance}.

Multiple fraud indicators were detected during analysis.

Recommendation:
Escalate this claim for immediate compliance review before approval.
"""

    else:

        return f"""
The claim was analyzed by the MedVision AI Fraud Intelligence Engine.

The claim received a fraud risk score of {fraud_score:.2f}%.

The selected department is {department} and the insurance status is {insurance}.

No significant fraud indicators were detected.

Recommendation:
Proceed with standard claim processing procedures.
"""