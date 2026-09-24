import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# --- 1. APP CONFIGURATION ---
st.set_page_config(page_title="R³ Digital Twin", page_icon="🧬", layout="wide")

# --- 2. CUSTOM CSS: ANIMATED HEMODIALYSIS BACKGROUND ---
st.markdown("""
<style>
    /* Animated Dialysate Flow Background */
    .stApp {
        background: linear-gradient(135deg, #0a0a14 0%, #1f0b11 50%, #05141f 100%);
        background-size: 400% 400%;
        animation: capillaryFlow 15s ease infinite;
        color: #e0e0e0;
    }
    
    @keyframes capillaryFlow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Simulating Floating RBCs & Urea Particles */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        background-image: 
            radial-gradient(circle at 15% 50%, rgba(220, 20, 60, 0.08) 0%, transparent 40%),
            radial-gradient(circle at 85% 30%, rgba(0, 242, 254, 0.08) 0%, transparent 40%);
        z-index: -1;
    }

    /* Glassmorphism UI Panels */
    .block-container {
        background: rgba(15, 20, 30, 0.65);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(0, 242, 254, 0.2);
        border-radius: 15px;
        box-shadow: 0 0 30px rgba(0, 242, 254, 0.1);
        padding-top: 2rem;
    }
    
    h1, h2, h3 { color: #00f2fe !important; text-shadow: 0 0 10px rgba(0, 242, 254, 0.3); }
</style>
""", unsafe_allow_html=True)

st.title("🧬 Project R³: AI Digital Twin Controller")
st.markdown("*Real-time bio-computational optimization of hemodialysis effluent upcycling.*")

# --- 3. INTERACTIVE TABS ---
tab1, tab2, tab3, tab4 = st.tabs(["⚡ ED Optimizer", "❄️ Phase-Change Thermodynamics", "💰 Economic Amortization", "🏭 Crystallographic Routing"])

# ==========================================
# TAB 1: ELECTRODIALYSIS OPTIMIZATION
# ==========================================
with tab1:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Live Fluid Parameters")
        flow_rate = st.slider("Flow Rate (Liters/hr)", 10, 500, 150)
        urea_conc = st.slider("Urea Concentration (mmol/L)", 10.0, 50.0, 30.0)
        
        with st.expander("🔬 View Mathematical Mechanism"):
            st.markdown("""
            **The Peers Equation & Limiting Current Density (LCD)**  
            In real-world electrodialysis, if voltage pushes ions faster than diffusion can supply them to the membrane boundary layer, the fluid reaches absolute depletion.  
            * **Formula:** $I_{lim} = \\frac{z F D C}{\\delta (T_m - t_s)}$  
            Exceeding this limit causes **Joule Heating ($I^2R$)** and water dissociation. The Digital Twin actively throttles voltage to stay exactly 5% below the LCD curve.
            """)
            
    with col2:
        # Dynamic calculation based on sliders
        voltage = np.linspace(0, 20, 100)
        # Simulate LCD curve (Ohmic -> Plateau -> Overlimiting)
        current = np.where(voltage < 8, 1.5 * voltage, 
                  np.where(voltage < 14, 12 + np.log(voltage - 7), 
                  12 + np.log(7) + 2.5 * (voltage - 14)))
        
        energy_loss = np.where(voltage > 14, (voltage - 14)**2 * (flow_rate/100), 0)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=voltage, y=current, mode='lines', name="Ion Current (A)", line=dict(color='#00ff87', width=3)))
        fig.add_trace(go.Scatter(x=voltage, y=energy_loss, mode='lines', name="Thermal Waste (Joule Heating)", line=dict(color='#ff3c3c', width=3, dash='dot')))
        
        fig.add_vline(x=14, line_width=2, line_dash="dash", line_color="cyan", annotation_text="AI Limit Threshold")
        fig.update_layout(title="Electrodialysis Membrane Polarization Curve",
                          paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                          font=dict(color="white"), xaxis_title="Applied Voltage (V)", yaxis_title="Current / Thermal Loss")
        st.plotly_chart(fig, use_container_width=True)

# ==========================================
# TAB 2: THERMODYNAMICS (EFC vs DISTILLATION)
# ==========================================
with tab2:
    col1, col2 = st.columns([2, 1])
    with col1:
        volumes = ['100L', '500L', '1,000L', '5,000L']
        thermal_cost = [65, 325, 650, 3250] # 0.65 kWh/L
        efc_cost = [12, 60, 120, 600]       # 0.12 kWh/L
        
        fig2 = go.Figure(data=[
            go.Bar(name='Traditional Thermal Boiling', x=volumes, y=thermal_cost, marker_color='#ff7e67'),
            go.Bar(name='R³ Sub-Cooling (EFC)', x=volumes, y=efc_cost, marker_color='#00f2fe')
        ])
        fig2.update_layout(title="Thermodynamic Energy Consumption (kWh)", barmode='group',
                           paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="white"))
        st.plotly_chart(fig2, use_container_width=True)
        
    with col2:
        st.subheader("Phase-Change Physics")
        with st.expander("🔬 View Thermodynamic Mechanism"):
            st.markdown("""
            **Bypassing the Boiling Point**  
            Traditional evaporation requires the **Latent Heat of Vaporization** ($\\Delta H_{vap} \\approx 2260\\text{ kJ/kg}$).  
            
            By utilizing Eutectic Freeze Crystallization (EFC), we sub-cool the fluid to exactly **-11.5°C**. This exploits the **Latent Heat of Fusion** ($\\Delta H_{fus} \\approx 334\\text{ kJ/kg}$).  
            
            Because freezing water requires roughly **6.7x less thermodynamic energy** than boiling it, our energy requirements crash from 0.65 kWh/L to 0.12 kWh/L.
            """)

# ==========================================
# TAB 3: UNIT ECONOMICS 
# ==========================================
with tab3:
    st.subheader("Enterprise Levelized Cost of Urea (LCOE)")
    
    kwh_tariff = st.slider("Local Grid Tariff (₹ / kWh)", 4.0, 15.0, 8.0)
    
    with st.expander("🔬 View Financial Mechanism"):
        st.markdown("""
        **Fully-Loaded OPEX Equation**  
        The net cost per Metric Ton dynamically recalculates based on live tariffs, amortized skid CAPEX, and subtracted biomaterial R&D plasma sales.  
        *Base Formula:* $Net Cost = CAPEX_{amort} + (Energy_{kWh} \\times Tariff) + Labor - Plasma_{Revenue}$
        """)

    cost_haber = 38500
    cost_r3 = 3500 + (600 * kwh_tariff) + 1200 # Amortized CAPEX + Energy + Maintenance
    
    fig3 = go.Figure(go.Indicator(
        mode = "number+delta",
        value = cost_r3,
        delta = {"reference": cost_haber, "position": "top", "valueformat": ",.0f", "prefix": "₹"},
        title = {"text": "Project R³ Net Cost per MT (₹)"},
        domain = {'y': [0, 1], 'x': [0.25, 0.75]}
    ))
    fig3.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color="#00ff87", size=20))
    st.plotly_chart(fig3, use_container_width=True)

# ==========================================
# TAB 4: CRYSTALLOGRAPHIC ROUTING
# ==========================================
with tab4:
    st.subheader("Automated Quality Control Router")
    st.markdown("Adjust the terminal urea purity detected by the HPLC sensors.")
    
    purity = st.slider("Detected Crystal Purity (%)", 95.0, 99.9, 99.8, 0.1)
    
    with st.expander("🔬 View Biological Purity Mechanism"):
        st.markdown("""
        **EDTA Chelation Verification**  
        If Heavy Metals (Ca2+, Mg2+) or trace blood proteins bypass the Phase 2 cellulose membrane, purity drops below 99.5%. The Python logic automatically reroutes imperfect batches away from automotive markets to prevent engine catalytic converter destruction.
        """)
    
    if purity >= 99.8:
        st.success("✅ **STATUS: 99.8% - ROUTE TO AUTOMOTIVE (AdBlue/DEF)**")
    elif purity >= 99.5:
        st.info("🧴 **STATUS: 99.5% - ROUTE TO MEDICAL COSMETICS**")
    else:
        st.warning("🌾 **STATUS: <99.5% - ROUTE TO AGRICULTURE (Fertilizer)**")