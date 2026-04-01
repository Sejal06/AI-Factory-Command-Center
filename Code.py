import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Factory Command Center", layout="wide")

st.title("🏭 AI Factory Command Center")
st.markdown("Unified Decision Intelligence Dashboard")

# -----------------------------
# SIDEBAR INPUTS
# -----------------------------
st.sidebar.header("⚙️ Factory Inputs")

# OEE Inputs
speed = st.sidebar.slider("Machine Speed", 800, 1200, 1000)
downtime = st.sidebar.slider("Downtime", 0, 120, 60)
defect = st.sidebar.slider("Defect Rate (%)", 0.0, 10.0, 5.0)
operator = st.sidebar.slider("Operator Efficiency (%)", 70, 100, 85)

# Production Inputs
cutting = st.sidebar.slider("Cutting Capacity", 50, 200, 120)
welding = st.sidebar.slider("Welding Capacity", 50, 200, 90)
assembly = st.sidebar.slider("Assembly Capacity", 50, 200, 110)

# Demand Inputs
price = st.sidebar.slider("Product Price", 100, 1000, 500)
base_demand = st.sidebar.slider("Base Demand", 100, 1000, 500)

# -----------------------------
# OEE CALCULATION
# -----------------------------
availability = 1 - (downtime / 480)
performance = speed / 1200
quality = 1 - (defect / 100)

oee = availability * performance * quality * operator/100

# -----------------------------
# PRODUCTION BOTTLENECK
# -----------------------------
capacities = [cutting, welding, assembly]
stations = ["Cutting", "Welding", "Assembly"]

bottleneck_value = min(capacities)
bottleneck_station = stations[capacities.index(bottleneck_value)]

# -----------------------------
# DEMAND MODEL
# -----------------------------
demand = base_demand * np.exp(-0.01 * price)

# -----------------------------
# REVENUE
# -----------------------------
production = bottleneck_value * oee
sales = min(production, demand)

revenue = sales * price

# -----------------------------
# DASHBOARD OUTPUT
# -----------------------------
st.subheader("📊 Executive Summary")

c1, c2, c3, c4 = st.columns(4)

c1.metric("OEE (%)", round(oee*100,2))
c2.metric("Throughput", round(production,2))
c3.metric("Demand", round(demand,2))
c4.metric("Revenue", round(revenue,2))

# -----------------------------
# VISUALIZATION
# -----------------------------
st.subheader("📈 Capacity vs Demand")

fig, ax = plt.subplots()
ax.bar(stations, capacities)
ax.axhline(y=demand, linestyle='--')
st.pyplot(fig)

# -----------------------------
# AI INSIGHTS
# -----------------------------
st.subheader("🧠 AI Recommendations")

if oee < 0.7:
    st.error("Low OEE → Improve machine efficiency")

if bottleneck_value < max(capacities):
    st.warning(f"Bottleneck at {bottleneck_station}")

if demand > production:
    st.warning("Demand exceeds production → Increase capacity")

if production > demand:
    st.info("Overproduction risk → Adjust pricing or production")

if revenue > 200000:
    st.success("High revenue scenario")