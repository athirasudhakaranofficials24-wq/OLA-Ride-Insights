
import streamlit as st
import pandas as pd
import mysql.connector
from pathlib import Path
import plotly.express as px

# ---------------------------------
# PAGE CONFIGURATION
# ---------------------------------

st.set_page_config(
    page_title="OLA Ride Insights",
    page_icon="🚕",
    layout="wide"
)

st.title("🚕 OLA RIDE INSIGHTS")
st.subheader("Ride Booking Analytics Dashboard")

# ---------------------------------
# DATABASE CONNECTION
# ---------------------------------

st.sidebar.header("Database Connection")

host = st.sidebar.text_input("Host", "localhost")
user = st.sidebar.text_input("Username", "root")
password = st.sidebar.text_input(
    "Password",
    type="password"
)
database = st.sidebar.text_input(
    "Database",
    "ola_project"
)

if st.sidebar.button("Connect to Database"):

    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        query = "SELECT * FROM ola_cleaned_data"

        df = pd.read_sql(query, conn)

        conn.close()

        st.session_state["ola_data"] = df

        st.success("Database Connected Successfully!")

    except Exception as e:
        st.error(f"Connection Error: {e}")


# ---------------------------------
# DISPLAY DATA
# ---------------------------------

if "ola_data" in st.session_state:

    df = st.session_state["ola_data"].copy()

    # Date format
    df["Date"] = pd.to_datetime(
        df["Date"],
        errors="coerce"
    )

    st.divider()

    # ---------------------------------
    # KPI CARDS
    # ---------------------------------

    st.header("Ride Booking Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Bookings",
        f"{df['Booking_ID'].nunique():,}"
    )

    col2.metric(
        "Total Revenue",
        f"₹{df['Booking_Value'].sum():,.2f}"
    )

    col3.metric(
        "Total Ride Distance",
        f"{df['Ride_Distance'].sum():,.2f} KM"
    )

    col4.metric(
        "Average Booking Value",
        f"₹{df['Booking_Value'].mean():,.2f}"
    )

    st.divider()

    # ---------------------------------
    # INTERACTIVE FILTERS
    # ---------------------------------

    st.header("Interactive Filters")

    c1, c2, c3 = st.columns(3)

    with c1:
        vehicle = st.selectbox(
            "Vehicle Type",
            ["All"] + sorted(
                df["Vehicle_Type"].dropna().unique().tolist()
            )
        )

    with c2:
        status = st.selectbox(
            "Booking Status",
            ["All"] + sorted(
                df["Booking_Status"].dropna().unique().tolist()
            )
        )

    with c3:
        payment = st.selectbox(
            "Payment Method",
            ["All"] + sorted(
                df["Payment_Method"].dropna().unique().tolist()
            )
        )

    filtered_df = df.copy()

    if vehicle != "All":
        filtered_df = filtered_df[
            filtered_df["Vehicle_Type"] == vehicle
        ]

    if status != "All":
        filtered_df = filtered_df[
            filtered_df["Booking_Status"] == status
        ]

    if payment != "All":
        filtered_df = filtered_df[
            filtered_df["Payment_Method"] == payment
        ]

    # ---------------------------------
    # SEARCH BOOKING
    # ---------------------------------

    st.divider()

    st.header("Search Booking")

    search_id = st.text_input("Enter Booking ID")

    if search_id:
        filtered_df = filtered_df[
            filtered_df["Booking_ID"].astype(str).str.contains(
                search_id,
                case=False,
                na=False
            )
        ]

    st.subheader("SQL Query Results")

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

    st.write("Total Records:", len(filtered_df))

    # ---------------------------------
    # ANALYTICS TABS
    # ---------------------------------

    st.divider()

    st.title("OLA RIDE INSIGHTS - ANALYTICS")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Overall",
        "Vehicle Type",
        "Revenue",
        "Cancellation",
        "Ratings"
    ])

    # ---------------------------------
    # TAB 1 - OVERALL
    # ---------------------------------

    with tab1:

        st.header("Overall Analysis")

        # Ride Volume Over Time

        ride_volume = (
            filtered_df.groupby("Date")["Booking_ID"]
            .nunique()
            .reset_index(name="Total Bookings")
            .sort_values("Date")
        )

        fig1 = px.line(
            ride_volume,
            x="Date",
            y="Total Bookings",
            title="Ride Volume Over Time",
            markers=True
        )

        st.plotly_chart(
            fig1,
            use_container_width=True
        )

        # Booking Status Breakdown

        status_data = (
            filtered_df["Booking_Status"]
            .value_counts()
            .reset_index()
        )

        status_data.columns = [
            "Booking Status",
            "Bookings"
        ]

        fig2 = px.pie(
            status_data,
            names="Booking Status",
            values="Bookings",
            hole=0.5,
            title="Booking Status Breakdown"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    # ---------------------------------
    # TAB 2 - VEHICLE TYPE
    # ---------------------------------

    with tab2:

        st.header("Vehicle Type Analysis")

        vehicle_data = (
            filtered_df.groupby("Vehicle_Type")["Ride_Distance"]
            .sum()
            .reset_index()
            .sort_values(
                "Ride_Distance",
                ascending=False
            )
            .head(5)
        )

        fig3 = px.bar(
            vehicle_data,
            x="Ride_Distance",
            y="Vehicle_Type",
            orientation="h",
            title="Top 5 Vehicle Types by Ride Distance"
        )

        st.plotly_chart(
            fig3,
            use_container_width=True
        )

    # ---------------------------------
    # TAB 3 - REVENUE
    # ---------------------------------

    with tab3:

        st.header("Revenue Analysis")

        # Revenue by Payment Method

        revenue_data = (
            filtered_df.groupby("Payment_Method")["Booking_Value"]
            .sum()
            .reset_index()
        )

        fig4 = px.bar(
            revenue_data,
            x="Payment_Method",
            y="Booking_Value",
            title="Revenue by Payment Method"
        )

        st.plotly_chart(
            fig4,
            use_container_width=True
        )

        # Top 5 Customers

        customer_data = (
            filtered_df.groupby("Customer_ID")["Booking_Value"]
            .sum()
            .reset_index()
            .sort_values(
                "Booking_Value",
                ascending=False
            )
            .head(5)
        )

        fig5 = px.bar(
            customer_data,
            x="Customer_ID",
            y="Booking_Value",
            title="Top 5 Customers by Total Booking Value"
        )

        st.plotly_chart(
            fig5,
            use_container_width=True
        )

        # Ride Distance Distribution Per Day

        daily_distance = (
            filtered_df.groupby("Date")["Ride_Distance"]
            .sum()
            .reset_index()
            .sort_values("Date")
        )

        fig6 = px.line(
            daily_distance,
            x="Date",
            y="Ride_Distance",
            markers=True,
            title="Ride Distance Distribution Per Day"
        )

        st.plotly_chart(
            fig6,
            use_container_width=True
        )

    # ---------------------------------
    # TAB 4 - CANCELLATION
    # ---------------------------------

    with tab4:

        st.header("Cancellation Analysis")

        st.info(
            "Cancellation reason charts require the actual "
            "reason values in the dataset. The following "
            "charts show customer and driver cancellation counts."
        )

        # Customer Cancellations

        if "Canceled_Rides_by_Customer" in filtered_df.columns:

            customer_cancel = (
                filtered_df["Canceled_Rides_by_Customer"]
                .value_counts()
                .reset_index()
            )

            customer_cancel.columns = [
                "Cancellation Value",
                "Count"
            ]

            fig7 = px.pie(
                customer_cancel,
                names="Cancellation Value",
                values="Count",
                title="Customer Cancellations"
            )

            st.plotly_chart(
                fig7,
                use_container_width=True
            )

        # Driver Cancellations

        if "Canceled_Rides_by_Driver" in filtered_df.columns:

            driver_cancel = (
                filtered_df["Canceled_Rides_by_Driver"]
                .value_counts()
                .reset_index()
            )

            driver_cancel.columns = [
                "Cancellation Value",
                "Count"
            ]

            fig8 = px.pie(
                driver_cancel,
                names="Cancellation Value",
                values="Count",
                title="Driver Cancellations"
            )

            st.plotly_chart(
                fig8,
                use_container_width=True
            )

    # ---------------------------------
    # TAB 5 - RATINGS
    # ---------------------------------

    with tab5:

        st.header("Ratings Analysis")

        # Driver Ratings

        driver_rating = (
            filtered_df["Driver_Ratings"]
            .dropna()
            .value_counts()
            .sort_index()
            .reset_index()
        )

        driver_rating.columns = [
            "Driver Rating",
            "Count"
        ]

        fig9 = px.bar(
            driver_rating,
            x="Driver Rating",
            y="Count",
            title="Driver Ratings Distribution"
        )

        st.plotly_chart(
            fig9,
            use_container_width=True
        )

        # Customer Ratings

        customer_rating = (
            filtered_df["Customer_Rating"]
            .dropna()
            .value_counts()
            .sort_index()
            .reset_index()
        )

        customer_rating.columns = [
            "Customer Rating",
            "Count"
        ]

        fig10 = px.bar(
            customer_rating,
            x="Customer Rating",
            y="Count",
            title="Customer Ratings Distribution"
        )

        st.plotly_chart(
            fig10,
            use_container_width=True
        )

    # ---------------------------------
    # POWER BI DASHBOARD IMAGES
    # ---------------------------------

    st.divider()

    st.header("Power BI Dashboard")

    folder = Path(__file__).parent

    image1 = folder / "ola_ride_analysis dashboard-1.png"
    image2 = folder / "ola_ride_analysis dashboard-2.png"

    if image1.exists():

        st.subheader("OLA Ride Overview")

        st.image(
            str(image1),
            use_container_width=True
        )

    else:
        st.warning("Overview dashboard image not found.")

    if image2.exists():

        st.subheader("OLA Ride Analysis")

        st.image(
            str(image2),
            use_container_width=True
        )

    else:
        st.warning("Analysis dashboard image not found.")

else:

    st.info("Please connect to MySQL using the sidebar.")
