import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression

# =====================================
# PAGE SETTINGS
# =====================================

st.set_page_config(
    page_title="AI Textile Dashboard",
    page_icon="🧵",
    layout="wide"
)

# =====================================
# LOGIN SESSION
# =====================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# =====================================
# LOGIN PAGE
# =====================================

if not st.session_state.logged_in:

    st.title("🧵 Textile Dashboard Login")

    username = st.text_input("👤 Username")

    password = st.text_input(
        "🔒 Password",
        type="password"
    )

    if st.button("Login"):

        if username == "admin" and password == "1234":

            st.session_state.logged_in = True
            st.rerun()

        else:

            st.error("❌ Wrong username or password")

# =====================================
# MAIN APPLICATION
# =====================================

else:

    st.sidebar.title("🧵 Textile Dashboard")

    # ---------------------------------
    # Upload CSV
    # ---------------------------------

    uploaded_file = st.sidebar.file_uploader(
        "📁 Upload CSV File",
        type=["csv"]
    )

    if uploaded_file is None:

        st.title("📁 Upload Sales Data")

        st.info(
            "Please upload a CSV file from the sidebar to continue."
        )

        if st.sidebar.button("🚪 Logout"):

            st.session_state.logged_in = False
            st.rerun()

        st.stop()

    # ---------------------------------
    # Read Data
    # ---------------------------------

    data = pd.read_csv(uploaded_file)

    # ---------------------------------
    # Machine Learning Model
    # ---------------------------------

    X = data[["Month"]]
    y = data["Sales"]

    model = LinearRegression()

    model.fit(X, y)

    next_month = data["Month"].max() + 1

    prediction = int(
        model.predict([[next_month]])[0]
    )

    # ---------------------------------
    # Dynamic Profit
    # ---------------------------------

    profit = int(data["Sales"].sum() * 10)

    # ---------------------------------
    # Sidebar Menu
    # ---------------------------------

    menu = st.sidebar.selectbox(
        "Choose Page",
        [
            "🏠 Home",
            "📈 Prediction",
            "📦 Inventory",
            "📄 Reports"
        ]
    )

    if st.sidebar.button("🚪 Logout"):

        st.session_state.logged_in = False
        st.rerun()

    # =====================================
    # HOME PAGE
    # =====================================

    if menu == "🏠 Home":

        st.title("🧵 AI Textile Dashboard")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "📦 Total Stock",
            "1120"
        )

        col2.metric(
            "📈 Predicted Demand",
            prediction
        )

        col3.metric(
            "💰 Estimated Profit",
            f"₹{profit}"
        )

        st.subheader("📈 Monthly Sales Chart")

        st.line_chart(data["Sales"])

        st.subheader("📋 Sales Data")

        st.dataframe(data)

    # =====================================
    # PREDICTION PAGE
    # =====================================

    elif menu == "📈 Prediction":

        st.title("📈 Demand Prediction")

        future_month = st.number_input(
            "Enter Future Month",
            min_value=1,
            value=int(next_month),
            step=1
        )

        future_prediction = model.predict(
            [[future_month]]
        )

        st.success(
            f"Predicted Sales: {int(future_prediction[0])}"
        )

    # =====================================
    # INVENTORY PAGE
    # =====================================

    elif menu == "📦 Inventory":

        st.title("📦 Inventory Management")

        st.subheader("Enter Stock Values")

        cotton = st.number_input(
            "Cotton Fabric Stock",
            min_value=0,
            value=250
        )

        silk = st.number_input(
            "Silk Fabric Stock",
            min_value=0,
            value=150
        )

        denim = st.number_input(
            "Denim Fabric Stock",
            min_value=0,
            value=300
        )

        polyester = st.number_input(
            "Polyester Fabric Stock",
            min_value=0,
            value=200
        )

        rayon = st.number_input(
            "Rayon Fabric Stock",
            min_value=0,
            value=100
        )

        wool = st.number_input(
            "Wool Fabric Stock",
            min_value=0,
            value=120
        )

        stock = (
            cotton
            + silk
            + denim
            + polyester
            + rayon
            + wool
        )

        st.subheader("📊 Inventory Analysis")

        st.write(
            f"📦 Total Stock = {stock}"
        )

        st.write(
            f"📈 Predicted Demand = {prediction}"
        )

        # Alert System

        if stock >= prediction + 200:

            st.success(
                "✅ Stock Sufficient"
            )

        elif stock >= prediction:

            st.warning(
                "⚠ Reorder Soon"
            )

        else:

            st.error(
                "🚨 Urgent Restock Needed"
            )

    # =====================================
    # REPORTS PAGE
    # =====================================

    elif menu == "📄 Reports":

        st.title("📄 Sales Reports")

        total_sales = data["Sales"].sum()

        average_sales = data["Sales"].mean()

        highest_sales = data["Sales"].max()

        lowest_sales = data["Sales"].min()

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "💰 Total Sales",
                total_sales
            )

            st.metric(
                "📈 Highest Sales",
                highest_sales
            )

        with col2:

            st.metric(
                "📊 Average Sales",
                round(average_sales, 2)
            )

            st.metric(
                "📉 Lowest Sales",
                lowest_sales
            )

        st.subheader("📋 Dataset Used")

        st.dataframe(data)

        st.subheader("📊 Sales Bar Chart")

        st.bar_chart(data["Sales"])

        # Download CSV

        st.download_button(
            label="⬇ Download Dataset",
            data=data.to_csv(index=False),
            file_name="sales_report.csv",
            mime="text/csv"
        )