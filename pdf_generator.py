from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet

def generate_report(
    procedure,
    lab_test,
    insurance,
    cost,
    department,
    result,
    fraud_score,
    reasons,
    findings,
    executive_report
):

    pdf_file = "Fraud_Report.pdf"

    doc = SimpleDocTemplate(pdf_file)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            "MedVision AI Investigation Report",
            styles["Title"]
        )
    )

    elements.append(Spacer(1,12))

    elements.append(
        Paragraph(
            f"<b>Procedure:</b> {procedure}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"<b>Lab Test:</b> {lab_test}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"<b>Department:</b> {department}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"<b>Insurance:</b> {insurance}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"<b>Cost:</b> ₹{cost}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"<b>Prediction:</b> {result}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"<b>Risk Score:</b> {fraud_score:.2f}%",
            styles["Normal"]
        )
    )

    elements.append(Spacer(1,12))

    elements.append(
        Paragraph(
            "AI Findings",
            styles["Heading2"]
        )
    )

    for reason in reasons:
        elements.append(
            Paragraph(
                f"• {reason}",
                styles["Normal"]
            )
        )

    elements.append(Spacer(1,12))

    elements.append(
        Paragraph(
            "AI Fraud Investigator",
            styles["Heading2"]
        )
    )

    for item in findings:

        elements.append(
            Paragraph(
                f"• {item}",
                styles["Normal"]
            )
        )

    elements.append(Spacer(1,12))

    elements.append(
        Paragraph(
            "Executive AI Assessment",
            styles["Heading2"]
        )
    )

    elements.append(
        Paragraph(
            executive_report,
            styles["Normal"]
        )
    )

    doc.build(elements)

    return pdf_file