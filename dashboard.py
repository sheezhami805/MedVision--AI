import streamlit as st
import pandas as pd
import joblib
import sqlite3
import matplotlib.pyplot as plt
from fraud_explainer import explain_fraud
from db_functions import save_prediction
from alerts import generate_alert
from pdf_generator import generate_report
from email_alert import send_alert
from fraud_investigator import investigate_claim
from executive_report import generate_executive_report



st.set_page_config(
    page_title="MedVision AI",
    page_icon="🏥",
    layout="wide"
)

st.markdown("""
<style>

.main {
    background-color: #0f172a;
}

.stApp {
    background-color: #0f172a;
}

h1,h2,h3,h4,h5,h6 {
    color: white;
}

[data-testid="stSidebar"] {
    background-color: #111827;
}

</style>
""", unsafe_allow_html=True)
#==========================
#Threat Level
#==========================
def get_threat_level():

    try:

        conn = sqlite3.connect(
            "fraud_detection.db"
        )

        df = pd.read_sql(
            "SELECT * FROM fraud_history",
            conn
        )

        conn.close()

        total_cases = len(df)

        fraud_cases = len(
            df[
                df["prediction"] == "Fraud"
            ]
        )

        if total_cases == 0:

            return "🟢 LOW", 0

        fraud_percentage = (
            fraud_cases / total_cases
        ) * 100

        if fraud_percentage >= 50:

            return "🔴 CRITICAL", fraud_percentage

        elif fraud_percentage >= 20:

            return "🟠 ELEVATED", fraud_percentage

        else:

            return "🟢 LOW", fraud_percentage

    except:

        return "🟢 LOW", 0
#==========================
#Dept Risk Ranking
#==========================

def get_department_ranking():

    try:

        conn = sqlite3.connect(
            "fraud_detection.db"
        )

        df = pd.read_sql(
            "SELECT * FROM fraud_history",
            conn
        )

        conn.close()

        ranking = (
            df.groupby("department")["fraud_score"]
            .mean()
            .reset_index()
            .sort_values(
                by="fraud_score",
                ascending=False
            )
        )

        return ranking

    except Exception as e:

        print("Department Ranking Error:", e)

        return pd.DataFrame()






#==========================
#Fraud Leaderboard
#==========================



def get_top_fraud_cases():

    try:

        conn = sqlite3.connect(
            "fraud_detection.db"
        )

        df = pd.read_sql(
            """
            SELECT *
            FROM fraud_history
            ORDER BY fraud_score DESC
            LIMIT 10
            """,
            conn
        )

        conn.close()

        return df

    except Exception as e:

        print("Leaderboard Error:", e)

        return pd.DataFrame()



#==========================
#same cases
#==========================


def find_similar_cases(
    department,
    fraud_score
):

    try:

        conn = sqlite3.connect(
            "fraud_detection.db"
        )

        df = pd.read_sql(
            "SELECT * FROM fraud_history",
            conn
        )

        conn.close()

        fraud_cases = df[
            df["prediction"] == "Fraud"
        ]

        similar = fraud_cases[
            fraud_cases["department"].str.lower()
            ==
            department.lower()
        ]

        similar = similar.sort_values(
            by="fraud_score",
            ascending=False
        )

        return similar.head(5)

    except Exception as e:

        print("Error:", e)

        return pd.DataFrame()


# Load model
import joblib

print("Loading model...")
model = joblib.load("models/fraud_model.pkl")

print("Loading encoders...")
encoders = joblib.load("models/encoders.pkl")

print("Loading label encoder...")
label_encoder = joblib.load("models/label_encoder.pkl")

print("All files loaded successfully!")

# Dataset
df = pd.read_csv("dataset/Hospital_billing_fraud_detection.csv")

st.set_page_config(
    page_title="Hospital Billing Fraud Detection",
    layout="wide"
)


# ==========================
# SIMPLE LOGIN SYSTEM
# ==========================

ADMIN_PASSWORD = "admin123"
AUDITOR_PASSWORD = "auditor123"

st.sidebar.title("🔐 Login")

role = st.sidebar.radio(
    "Select Role",
    ["Auditor", "Admin"]
)

password = st.sidebar.text_input(
    "Password",
    type="password"
)

if role == "Admin":

    if password != ADMIN_PASSWORD:
        st.warning("🔒 Enter Admin Password")
        st.stop()

elif role == "Auditor":

    if password != AUDITOR_PASSWORD:
        st.warning("🔒 Enter Auditor Password")
        st.stop()


st.markdown("""
<style>

/* Navigation title */
[data-testid="stSidebar"] label {
    color: #A855F7 !important;
    font-weight: 900 !important;
    font-size: 20px !important;
}

/* Radio text */
[data-testid="stSidebar"] .stRadio label {
    font-weight: 700 !important;
    color: #14B8A6 !important;
    font-size: 16px !important;
}

</style>
""", unsafe_allow_html=True)





st.markdown("""
<style>

/* Main App */
.stApp{
    background-color:#F8FAFC;
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background: linear-gradient(
        180deg,
        #111827 0%,
        #1F2937 100%
    );
}

section[data-testid="stSidebar"] *{
    color:white;
}

/* Buttons */
.stButton>button{
    border-radius:15px;
    border:none;
    font-weight:bold;
    padding:12px;
}

/* Metrics */
[data-testid="metric-container"]{
    background:white;
    border-radius:18px;
    padding:20px;
    box-shadow:0 4px 12px rgba(0,0,0,0.08);
}

/* Dataframes */
[data-testid="stDataFrame"]{
    border-radius:15px;
}

</style>
""", unsafe_allow_html=True)








st.markdown("""
<div style="
padding:25px;
border-radius:20px;
background:linear-gradient(
90deg,
#2563eb,
#06b6d4
);
color:white;
text-align:center;
">

<h1>🏥 MedVision AI Enterprise</h1>

<p>
Healthcare Fraud Intelligence Platform
</p>

</div>
""", unsafe_allow_html=True)

st.sidebar.image(
    "https://img.icons8.com/fluency/96/hospital.png",
    width=100
)

st.sidebar.title("🧠 MedVision AI")



if role == "Auditor":

    menu = st.sidebar.radio(
        "Navigation",
        [
        
            "🏠 Command Center",
            "🔍 AI Audit Engine",
            "📂 Bulk Investigation",
            "📊 Intelligence Nexus",
            "📜 Audit Vault",
            "🎯 Executive Command"

        ]
    )

elif role == "Admin":

    menu = st.sidebar.radio(
        "Navigation",
        [
            "🏠 Command Center",
            "🔍 AI Audit Engine",
            "📂 Bulk Investigation",
            "📊 Intelligence Nexus",
            "📜 Audit Vault",
            "⚙ Admin Center"
        ]
    )

st.sidebar.success(f"Logged in as: {role}")
    

# =========================
#Admin Center
# =========================

if menu == "⚙ Admin Center":

    st.title("⚙ MedVision AI Admin Center")

    st.metric(
        "Total Claims",
        len(df)
    )

    st.metric(
        "Fraud Cases",
        len(df[df["Label"] == "Fraud"])
    )

    st.metric(
        "Genuine Cases",
        len(df[df["Label"] == "Genuine"])
    )

    st.success(
        "System Status: Operational"
    )




# =========================
# DASHBOARD
# =========================

if menu == "🏠 Command Center":

    st.subheader("Dataset Overview")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("📋 Total Records", len(df))

    with col2:
        st.metric(
            "🚨 Fraud Cases",
            len(df[df["Label"] == "Fraud"])
        )

    st.dataframe(df.head())
# =========================
# SINGLE BILL DETECTION
# =========================

elif menu == "🔍 AI Audit Engine":

    st.subheader("🔍 Check Hospital Bill")

    procedure = st.selectbox(
        "Procedure Code",
        sorted(df["Procedure_Code"].unique())
    )

    lab_test = st.selectbox(
        "Lab Test",
        sorted(df["Lab_Test"].unique())
    )

    insurance = st.selectbox(
        "Insurance Claim",
        ["Yes", "No"]
    )

    cost = st.number_input(
        "Cost",
        min_value=0.0,
        value=1000.0
    )

    department = st.selectbox(
        "Department",
        sorted(df["Hospital_Department"].unique())
    )

    if st.button("🚨 Detect Fraud", key="detect_btn"):

        data = pd.DataFrame([{
            "Procedure_Code": procedure,
            "Lab_Test": lab_test,
            "Insurance_Claim": insurance,
            "Cost": cost,
            "Hospital_Department": department
        }])

    # Encode categorical columns
        for col in [
            "Procedure_Code",
            "Lab_Test",
            "Insurance_Claim",
            "Hospital_Department"
        ]:
            data[col] = encoders[col].transform(data[col])

    # Prediction
        prediction = model.predict(data)
        probability = model.predict_proba(data)

        fraud_score = probability[0][1] * 100


        result = label_encoder.inverse_transform(prediction)
        result = label_encoder.inverse_transform(prediction)



        alert = generate_alert(
            result[0],
            fraud_score,
            department
        )

        if alert:
            st.error(alert)


            if alert:

                st.markdown(f"""
                    <div style="
                    background:#FEF2F2;
                    padding:20px;
                    border-radius:15px;
                    border-left:8px solid #DC2626;
                    ">
                    </div>
                    """, unsafe_allow_html=True)

    # AI Explanation
        reasons, risk_points = explain_fraud(
            cost,
            insurance,
            department
        )

        findings, risk_level = investigate_claim(
            fraud_score,
            department,
            insurance,
            cost
        )


        executive_report = generate_executive_report(
            result[0],
            fraud_score,
            department,
            insurance
        )

        #Generate the report

        pdf_file = generate_report(
            procedure,
            lab_test,
            insurance,
            cost,
            department,
            result[0],
            fraud_score,
            reasons,
            findings,
            executive_report
        )


        with open(pdf_file, "rb") as file:

            st.download_button(
                "📄 Download Investigation Report",
                file,
                file_name="MedVision_AI_Report.pdf",
                mime="application/pdf"
            )

        

    # Risk Score
        st.metric(
            "📊 Fraud Risk Score",
            f"{fraud_score:.2f}%"
        )

    # Risk Meter
        st.subheader("📈 Risk Meter")

        st.progress(min(fraud_score / 100, 1.0))

        if fraud_score >= 80:
            st.error("🔴 Critical Risk")
        elif fraud_score >= 60:
            st.warning("🟠 Moderate Risk")
        else:
            st.success("🟢 Low Risk")

        st.caption(
            f"🤖 AI Confidence Level: {fraud_score:.2f}%"
        )

    # AI Risk Breakdown
        st.subheader("🧠 AI Risk Breakdown")

        for reason in reasons:
            st.info(reason)

        st.metric(
            "⚡ Risk Factors Score",
            f"{risk_points}/100"
        )

    # Save Prediction
        save_prediction(
            procedure,
            lab_test,
            insurance,
            cost,
            department,
            result[0],
            round(fraud_score, 2)
        )

    # Result Display
        if result[0] == "Fraud":

            send_alert(
                department,
                fraud_score
            )

            st.error("🚨 Fraudulent Bill Detected")

            st.subheader("🤖 Executive AI Findings")

            st.markdown(f"""
### 🚨 Fraud Investigation Result

The AI detected suspicious billing indicators.

**Estimated Risk:** {fraud_score:.2f}%

**Recommended Action:**
Manual review before approval.
""")

        else:

            st.success("✅ Genuine Bill Detected")

            st.subheader("🤖 Executive AI Findings")

            st.markdown(f"""
### ✅ Genuine Claim Assessment

The AI found no significant fraud indicators.

**Estimated Risk:** {fraud_score:.2f}%

**Recommended Action:**
Proceed with normal claim processing.
""")

    # Investigation Summary
        st.subheader("📋 Investigation Summary")

        if result[0] == "Fraud":

            st.markdown(f"""
**Status:** High Risk Claim

- Risk Score: {fraud_score:.2f}%
- Department: {department}
- Insurance: {insurance}

**Recommendation:** Manual audit recommended.
""")

        else:

            st.markdown(f"""
**Status:** Low Risk Claim

- Risk Score: {fraud_score:.2f}%
- Department: {department}
- Insurance: {insurance}

**Recommendation:** Claim appears legitimate.
""")
            


        
# ==================================
# AI FRAUD INVESTIGATOR
# ==================================

        st.subheader("🤖 AI Fraud Investigator")

        st.markdown("""
            ### Investigation Findings
            """)

        for item in findings:
            st.info(item)

        st.markdown(f"""
            ### Risk Classification
            {risk_level}
            """)

        if result[0] == "Fraud":

            st.error("""
Recommended Action:

Escalate claim for manual compliance review.
""")

        else:

            st.success("""
Recommended Action:

Proceed with normal claim processing.
""")

# =========================
#Executive AI Report
# =========================

        st.subheader("🏛 Compliance Intelligence Report")

        st.markdown(f"""
<div style="
background:#F8FAFC;
padding:20px;
border-radius:15px;
border-left:8px solid #7C3AED;
">

{executive_report}

</div>
""", unsafe_allow_html=True)
        
        st.subheader("🕵️ Similar Fraud Cases")

        similar_cases = find_similar_cases(
            department,
            fraud_score
        )

        if not similar_cases.empty:

            for _, row in similar_cases.iterrows():

                st.warning(
            f"""
🆔 Case ID: {row['id']}

🏥 Department: {row['department']}

💰 Cost: ₹{row['cost']}

🚨 Risk Score: {row['fraud_score']:.2f}%
"""
        )

        else:

            st.info(
                "No similar fraud cases found."
            )

# =========================
# ANALYTICS
# =========================

elif menu == "📂 Bulk Investigation":

    st.subheader("📂 Upload Bills CSV")

    uploaded_file = st.file_uploader(
        "Upload CSV File",
        type=["csv"]
    )

    if uploaded_file is not None:

        data = pd.read_csv(uploaded_file)

        original_data = data.copy()

        for col in [
            "Procedure_Code",
            "Lab_Test",
            "Insurance_Claim",
            "Hospital_Department"
        ]:

            data[col] = encoders[col].transform(data[col])

        predictions = model.predict(data)

        probabilities = model.predict_proba(data)

        original_data["Prediction"] = (
            label_encoder.inverse_transform(predictions)
        )

        original_data["Fraud_Risk_%"] = (
            probabilities[:, 1] * 100
        ).round(2)

        st.success(
            f"{len(original_data)} Bills Processed"
        )

        st.dataframe(original_data.head())

        fraud_bills = original_data[
            original_data["Prediction"] == "Fraud"
        ]

        st.metric(
            "Fraud Bills Found",
            len(fraud_bills)
        )

        csv = fraud_bills.to_csv(index=False)

        st.download_button(
            "⬇ Download Fraud Report",
            csv,
            "fraud_report.csv",
            "text/csv"
        )

elif menu == "📊 Intelligence Nexus":


    

    st.markdown("""
<div style="
background: linear-gradient(135deg, #6D28D9, #0EA5E9);
padding: 25px;
border-radius: 20px;
text-align: center;
color: white;
margin-bottom: 20px;
">

<h1>📊 Intelligence Hub</h1>
<h4>AI-Powered Healthcare Fraud Monitoring Center</h4>

</div>
""", unsafe_allow_html=True)
    


       
    total_claims = len(df)
    fraud_claims = len(df[df["Label"] == "Fraud"])
    genuine_claims = len(df[df["Label"] == "Genuine"])

    fraud_rate = (fraud_claims / total_claims) * 100

    col1, col2, col3, col4 = st.columns(4)

                
    import sqlite3

    conn = sqlite3.connect("fraud_detection.db")

    history = pd.read_sql(
        "SELECT * FROM fraud_history",
        conn
    )

    conn.close()

    total_audits = len(history)

    fraud_cases = len(
        history[history["prediction"] == "Fraud"]
    )

    genuine_cases = len(
        history[history["prediction"] == "Genuine"]
    )

    avg_risk = history["fraud_score"].mean()

#Create KPI Cards
    col1,col2,col3,col4 = st.columns(4)

    with col1:
        st.metric(
            "📋 Claims Audited",
            total_claims
        )

    with col2:
        st.metric(
            "🚨 High Risk",
            fraud_claims
        )

    with col3:
        st.metric(
            "✅ Approved",
            genuine_claims
        )

    with col4:
        st.metric(
            "⚡ Fraud Rate",
            f"{fraud_rate:.1f}%"
        )


#Top Risk Departments
    st.subheader("🏆 Top Risk Departments")

    dept_counts = (history.groupby("department").size().sort_values(ascending=False))

    st.bar_chart(dept_counts)

    # Pie Chart
    fraud_counts = df["Label"].value_counts()

    fig1, ax1 = plt.subplots()

    ax1.pie(
        fraud_counts.values,
        labels=fraud_counts.index,
        autopct="%1.1f%%"
    )

    ax1.set_title("Fraud vs Genuine")

    st.pyplot(fig1)

    st.markdown("## 📊 Fraud Analytics Dashboard")



    # Department Fraud Chart
    dept_fraud = (
        df[df["Label"] == "Fraud"]
        .groupby("Hospital_Department")
        .size()
        .sort_values(ascending=False)
    )

    fig2, ax2 = plt.subplots(figsize=(10, 5))

    dept_fraud.plot(
        kind="bar",
        ax=ax2
    )


    ax2.set_title("Fraud Cases by Department")
    ax2.set_ylabel("Fraud Count")

    st.pyplot(fig2)

elif menu == "📜 Audit Vault":

    import sqlite3

    st.subheader("📜 Fraud Audit History")

    conn = sqlite3.connect("fraud_detection.db")

    history = pd.read_sql(
        "SELECT * FROM fraud_history ORDER BY id DESC",
        conn
    )
    st.write(history.columns)

    conn.close()

    st.dataframe(
        history,
        use_container_width=True
    )
    

elif menu == "🎯 Executive Command":


    st.subheader("🥇 Department Risk Ranking")

    dept_ranking = get_department_ranking()

    if not dept_ranking.empty:

        medals = ["🥇", "🥈", "🥉"]

        st.bar_chart(
            dept_ranking.set_index(
            "department"
            )["fraud_score"]
        )

        for i in range(
            min(3, len(dept_ranking))
        ):

            row = dept_ranking.iloc[i]

            st.success(
                f"""
                {medals[i]} {row['department']}

                Average Risk Score:
                {row['fraud_score']:.2f}%
                """)


    st.markdown("""
    <div style="
    background:#ECFDF5;
    padding:15px;
    border-radius:15px;
    border-left:8px solid #059669;
    margin-bottom:15px;
    ">

    <b>System Status:</b> Operational

    <br>

    <b>AI Engine:</b> Active

    <br>

    <b>Database:</b> Connected

    </div>
    """, unsafe_allow_html=True)

    st.title("🎯 Executive Command")

    threat_level, fraud_percentage = get_threat_level()

    st.markdown(
    f"""
<div style="
background:#111827;
padding:25px;
border-radius:15px;
text-align:center;
">

<h2>🌡️ Hospital Threat Level</h2>

<h1>{threat_level}</h1>

<h3>Fraud Activity: {fraud_percentage:.1f}%</h3>

</div>
""",
unsafe_allow_html=True
)

    st.progress(
        int(fraud_percentage)
    )
    conn = sqlite3.connect("fraud_detection.db")

    history = pd.read_sql(
        "SELECT * FROM fraud_history",
        conn
    )



    conn.close()

    # Executive KPI Cards

    total_claims = len(history)

    fraud_cases = len(
        history[history["prediction"] == "Fraud"]
    )

    genuine_cases = len(
        history[history["prediction"] == "Genuine"]
    )

    departments = history["department"].nunique()

    avg_risk = history["fraud_score"].mean()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "📋 Total Claims",
            total_claims
        )

    with col2:
        st.metric(
            "🚨 Fraud Cases",
            fraud_cases
        )

    with col3:
        st.metric(
            "🏥 Departments",
            departments
        )

    with col4:
        st.metric(
            "📈 Avg Risk",
            f"{avg_risk:.1f}%"
        )

        st.markdown(f"""
<div style="
background:rgba(255,255,255,0.1);
backdrop-filter:blur(10px);
padding:20px;
border-radius:20px;
text-align:center;
">

<h2>🌡️ Threat Level</h2>

<h1>{threat_level}</h1>

</div>
""", unsafe_allow_html=True)
    fraud_by_dept = (
        df[df["Label"] == "Fraud"]
            .groupby("Hospital_Department")
            .size()
        )

    most_risky = fraud_by_dept.idxmax()

    st.metric(
        "🏥 Most Risky Department",
        most_risky
    )

    st.subheader("📈 Investigation Activity")


    st.line_chart(history["fraud_score"])

    st.subheader("📜 Latest Audits")

    st.dataframe(
        history.tail(10),
        use_container_width=True
    )


    st.subheader("🔥 Top 5 High-Risk Claims")

    top5 = df.sort_values(
        by="Cost",
        ascending=False
    ).head(5)

    st.dataframe(
        top5,
        use_container_width=True
    )   

    st.subheader("🏆 Fraud Leaderboard")

    leaderboard = get_top_fraud_cases()

    st.dataframe(
        leaderboard[
            [
                "id",
                "department",
                "fraud_score"
            ]
        ],
    use_container_width=True
)

    if not leaderboard.empty:

        top_case = leaderboard.iloc[0]

        st.success(
            f"""
            🥇 Highest Risk Claim

            Case ID: {top_case['id']}

            Risk Score: {top_case['fraud_score']:.2f}%
            """
            )

        for index, row in leaderboard.iterrows():

            st.warning(
            f"""
🏅 Rank #{index + 1}

🆔 Case ID: {row['id']}

🏥 Department: {row['department']}

🚨 Risk Score: {row['fraud_score']:.2f}%
"""
            )

        

else:

    st.info(
        "No fraud cases available."
    )

    




    import sqlite3

    conn = sqlite3.connect("fraud_detection.db")

    alerts = pd.read_sql(
        """
        SELECT *
        FROM fraud_history
        WHERE prediction='Fraud'
        ORDER BY id DESC
        LIMIT 5
        """,
        conn
    )

    conn.close()

    st.subheader("🚨 Latest Alerts")

    st.dataframe(
    alerts,
    use_container_width=True
    )




    st.divider()




    st.markdown("""
<hr>

<div style="
text-align:center;
color:gray;
">

🧠 MedVision AI Enterprise Edition

Healthcare Fraud Intelligence Platform

</div>
""", unsafe_allow_html=True)
    







