import streamlit as st
import pandas as pd
import plotly.express as px
from code import AIRoITracker  # Importing your logic

# Page Config
st.set_page_config(page_title="AI Feature ROI Tracker", layout="wide")

st.title("Feature-Level AI ROI Tracker")
st.markdown("""
This dashboard monitors the **Return on Investment** of deployed AI features by comparing 
API token costs against human labor hours saved.
""")

# Load Data
try:
    tracker = AIRoITracker('ai_feature_logs.csv')
    df_report = tracker.get_feature_report()
    
    # --- TOP LEVEL METRICS ---
    col1, col2, col3 = st.columns(3)
    with col1:
        total_cost = df_report['api_cost_usd'].sum()
        st.metric("Total AI Cost", f"${total_cost:,.2f}")
    with col2:
        total_savings = df_report['labor_savings_usd'].sum()
        st.metric("Total Labor Savings", f"${total_savings:,.2f}")
    with col3:
        avg_roi = (df_report['net_savings'].sum() / total_cost) * 100
        st.metric("Aggregate ROI", f"{avg_roi:,.0f}%", delta=f"{avg_roi/100:.1f}x")

    st.divider()

    # --- VISUALIZATIONS ---
    left_chart, right_chart = st.columns(2)

    with left_chart:
        st.subheader("ROI Percentage by Feature")
        fig_roi = px.bar(
            df_report, 
            x='feature_name', 
            y='ROI_percent',
            color='ROI_percent',
            labels={'ROI_percent': 'ROI (%)', 'feature_name': 'Feature'},
            color_continuous_scale='RdYlGn'
        )
        st.plotly_chart(fig_roi, use_container_width=True)

    with right_chart:
        st.subheader("Cost vs. Savings Comparison")
        fig_comp = px.bar(
            df_report, 
            x='feature_name', 
            y=['api_cost_usd', 'labor_savings_usd'],
            barmode='group',
            labels={'value': 'USD ($)', 'variable': 'Metric'}
        )
        st.plotly_chart(fig_comp, use_container_width=True)

    # --- RAW DATA TABLE ---
    st.subheader("Detailed Feature Performance")
    st.dataframe(df_report, use_container_width=True, hide_index=True)

except FileNotFoundError:
    st.error("Dataset not found. Please run 'generator.py' first to create the logs!")