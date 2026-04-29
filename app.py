import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="SignalScope", layout="wide")

st.title("📊 SignalScope")
st.subheader("Real-Time Data Intelligence Platform")
st.sidebar.title("Filters")
st.sidebar.info("Choose settings below")

uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.success("File uploaded successfully!")

    # KPI Cards
    c1, c2, c3 = st.columns(3)

    c1.metric("Total Sales", df["Sales"].sum())
    c2.metric("Avg Temp", round(df["Temperature"].mean(), 1))
    c3.metric("Peak Visitors", df["Visitors"].max())

    st.write("## Dataset Preview")
    st.dataframe(df)
    best_day = df.loc[df["Sales"].idxmax(), "Day"]
    best_sales = df["Sales"].max()

    st.success(f"Insight: Peak sales happened on Day {best_day} with {best_sales} sales.")

    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    if numeric_cols:
        selected_col = st.selectbox("Select Metric", numeric_cols)

        avg_val = df[selected_col].mean()
        max_val = df[selected_col].max()
        min_val = df[selected_col].min()

        st.info(f"Average {selected_col}: {avg_val:.2f}")
        st.info(f"Highest {selected_col}: {max_val}")
        st.info(f"Lowest {selected_col}: {min_val}")

        fig = px.line(df, y=selected_col, markers=True,
                      title=f"{selected_col} Trend Over Time")
        st.plotly_chart(fig, use_container_width=True)

        # anomaly detection
        threshold = avg_val * 1.2
        anomalies = df[df[selected_col] > threshold]

        if not anomalies.empty:
            st.warning("Possible anomaly detected:")
            st.dataframe(anomalies)
        else:
            st.success("No anomalies detected.")
else:
    st.info("Upload a CSV file to begin.")