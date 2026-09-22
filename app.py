import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# --- App Configuration & UI Design ---
st.set_page_config(page_title="Project R³ Digital Twin", page_icon="🧬", layout="centered")
st.title("Project R³: Digital Twin Engine 🚀")
st.markdown("Live thermodynamic and financial optimization for hemodialysis effluent upcycling.")

# Create Mobile-Friendly Tabs
tab1, tab2, tab3, tab4 = st.tabs(["⚡ ED Optimizer", "💰 Unit Economics", "❄️ EFC vs Thermal", "🏭 Market Router"])

# ---------------------------------------------------------
# TAB 1: UREA EXTRACTION VIA ELECTRODIALYSIS
# ---------------------------------------------------------
with tab1:
    st.header("Electrodialysis (ED) Optimization")
    st.markdown("Adjust the parameters to see how the Digital Twin balances extraction vs. energy.")
    
    # Interactive Inputs (No fixed ranges, user decides)
    vol_input = st.number_input("Input Batch Volume (Liters)", min_value=10, max_value=10000, value=120)
    conc_input = st.slider("Urea Concentration (mmol/L)", min_value=10, max_value=60, value=30)
    
    # Simulate a range of voltages up to 15V to show the "danger zone"
    v_range = np.arange(1, 16, 1)
    
    efficiency = [100 - (100 / (0.5 * v + 1)) for v in v_range]
    energy_cost = [(v ** 2) * 0.5 * (vol_input/100) * (conc_input/30) for v in v_range]
    
    fig1, ax1 = plt.subplots(figsize=(8, 4))
    ax1.plot(v_range, efficiency, label="Extraction Efficiency (%)", color="blue", marker="o")
    ax1.plot(v_range, energy_cost, label="Energy Cost (₹)", color="red", marker="x")
    ax1.axvline(x=6, color='green', linestyle='--', label="AI Optimal Limit")
    ax1.set_xlabel("Applied Voltage (V)")
    ax1.set_ylabel("Metric Level")
    ax1.legend()
    ax1.grid(True)
    st.pyplot(fig1)

# ---------------------------------------------------------
# TAB 2: VOLTAGE AND COST PER TON
# ---------------------------------------------------------
with tab2:
    st.header("Financial Unit Economics")
    st.markdown("Input your local grid conditions to calculate the net cost per Metric Ton.")
    
    kwh_price = st.number_input("Local Electricity Cost (₹ per kWh)", value=8.00, step=0.50)
    mem_life = st.number_input("Expected Membrane Life (Hours)", value=5000, step=500)
    
    # Simple simulated optimization math for the app display
    optimal_voltage = max(2.0, 12.0 - (kwh_price * 0.5)) 
    base_cost_per_ton = 9500 # Your baseline
    adjusted_cost = base_cost_per_ton + (kwh_price * 100) - (mem_life * 0.1)
    
    st.success(f"**AI Selected Optimal Voltage:** {optimal_voltage:.2f} V")
    st.info(f"**Projected Cost to Produce 1 MT:** ₹{adjusted_cost:,.2f}")
    st.caption("Compared to ₹38,500/MT for imported Haber-Bosch urea.")

# ---------------------------------------------------------
# TAB 3: THERMAL DISTILLATION VS EUTECTIC FREEZE
# ---------------------------------------------------------
with tab3:
    st.header("Thermodynamic Cost Comparison")
    st.markdown("Compare the energy cost of boiling water vs. our sub-cooling EFC technology.")
    
    daily_volume = st.slider("Daily Hospital Effluent Processed (Liters)", 100, 10000, 5000)
    
    md_kwh_l = 0.65
    efc_kwh_l = 0.12
    
    cost_md = daily_volume * md_kwh_l * kwh_price
    cost_efc = daily_volume * efc_kwh_l * kwh_price
    savings = cost_md - cost_efc
    
    col1, col2 = st.columns(2)
    col1.metric("Thermal Distillation Cost", f"₹{cost_md:,.2f}")
    col2.metric("Project R³ (EFC) Cost", f"₹{cost_efc:,.2f}")
    
    st.success(f"🔥 Daily Savings Margin: ₹{savings:,.2f}")

# ---------------------------------------------------------
# TAB 4: PURITY PERCENTAGE ROUTING
# ---------------------------------------------------------
with tab4:
    st.header("Automated Quality Control Router")
    st.markdown("Input the final crystal purity detected by the sensors to route it to the correct market.")
    
    purity = st.slider("Detected Urea Purity (%)", min_value=95.0, max_value=99.9, value=99.8, step=0.1)
    
    if purity >= 99.8:
        st.success("✅ **ROUTE TO: Automotive / Transport**")
        st.markdown("Meets strict BS6 DEF/AdBlue specifications. Highest market value.")
    elif purity >= 99.5:
        st.info("🧴 **ROUTE TO: Medical Cosmetics**")
        st.markdown("Meets dermatological standards for high-end cosmetic formulations.")
    else:
        st.warning("🌾 **ROUTE TO: Agriculture**")
        st.markdown("Standard fertilizer grade. Safe for soil application.")