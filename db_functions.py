import sqlite3

def save_prediction(
    procedure,
    lab_test,
    insurance,
    cost,
    department,
    prediction,
    fraud_score
):

    conn = sqlite3.connect("fraud_detection.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO fraud_history
    (
        procedure_code,
        lab_test,
        insurance_claim,
        cost,
        department,
        prediction,
        fraud_score
    )
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
    (
        procedure,
        lab_test,
        insurance,
        cost,
        department,
        prediction,
        fraud_score
    ))

    conn.commit()
    conn.close()