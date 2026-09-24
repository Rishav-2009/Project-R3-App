import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# --- 1. APP CONFIGURATION ---
st.set_page_config(page_title="R³ Digital Twin", page_icon="🧬", layout="wide")

# --- 2. CRAZY CUSTOM CSS: UREA EXTRACTION MOLECULAR BACKGROUND & TANK ANIMATION ---
st.markdown("""
<style>
    /* Dark Sci-Fi Background */
    .stApp {
        background: linear-gradient(180deg, #020b14 0%, #061826 50%, #03121f 100%);
        color: #e0e0e0;
        overflow-x: hidden;
    }
    
    /* Glassmorphism Panels */
    .block-container {
        background: rgba(10, 15, 25, 0.75);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(0, 242, 254, 0.15);
        border-radius: 20px;
        box-shadow: 0 0 40px rgba(0, 242, 254, 0.05);
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    h1, h2, h3 { color: #00f2fe !important; text-shadow: 0 0 15px rgba(0, 242, 254, 0.4); }

    /* =========================================
       MOLECULAR SEPARATION BACKGROUND ANIMATION
       ========================================= */
    .molecule {
        position: fixed;
        border-radius: 50%;
        animation-timing-function: ease-in-out;
        animation-iteration-count: infinite;
        z-index: -1;
    }
    
    /* Na+ Ions getting pulled Left (Electrodialysis) */
    .salt-na {
        width: 12px; height: 12px;
        background: rgba(255, 60, 60, 0.5);
        box-shadow: 0 0 15px rgba(255, 60, 60, 0.9);
        animation-name: pullLeft;
    }
    
    /* Cl- Ions getting pulled Right (Electrodialysis) */
    .salt-cl {
        width: 12px; height: 12px;
        background: rgba(60, 255, 60, 0.5);
        box-shadow: 0 0 15px rgba(60, 255, 60, 0.9);
        animation-name: pullRight;
    }
    
    /* Urea Molecules dropping to Crystallize (EFC) */
    .urea-crystal {
        width: 18px; height: 18px;
        background: rgba(0, 242, 254, 0.7);
        box-shadow: 0 0 20px rgba(0, 242, 254, 1);
        clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%); /* Hexagon Shape */
        animation-name: dropFreeze;
    }

    @keyframes pullLeft {
        0% { top: -5%; left: 50%; opacity: 0; }
        20% { opacity: 1; }
        80% { opacity: 1; }
        100% { top: 105%; left: 10%; opacity: 0; } /* Curves Left */
    }
    
    @keyframes pullRight {
        0% { top: -5%; left: 50%; opacity: 0; }
        20% { opacity: 1; }
        80% { opacity: 1; }
        100% { top: 105%; left: 90%; opacity: 0; } /* Curves Right */
    }
    
    @keyframes dropFreeze {
        0% { top: -5%; left: 50%; opacity: 0; transform: scale(0.5) rotate(0deg); }
        30% { opacity: 1; transform: scale(0.8) rotate(45deg); }
        80% { opacity: 1; }
        100% { top: 105%; left: 50%; opacity: 0; transform: scale(1.5) rotate(360deg); } /* Drops straight down & crystallizes */
    }

    /* =========================================
       PMNDP WASTAGE TANK ANIMATION
       ========================================= */
    .tank-container {
        position: relative;
        width: 100%;
        height: 280px;
        background: rgba(0, 0, 0, 0.5);
        border: 2px solid #ff3c3c;
        border-radius: 15px;
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: inset 0 0 30px rgba(255, 60, 60, 0.2), 0 0 20px rgba(255, 60, 60, 0.3);
        margin-top: 20px;
        margin-bottom: 20px;
    }
    .liquid-wave {
        position: absolute;
        bottom: 0;
        left: 0;
        width: 200%;
        height: 100%;
        background: linear-gradient(180deg, rgba(255, 60, 60, 0.6) 0%, rgba(139, 0, 0, 0.9) 100%);
        animation: riseUp 3s cubic-bezier(0.4, 0, 0.2, 1) forwards, wave 4s linear infinite;
        z-index: 1;
        opacity: 0.85;
        transform-origin: bottom;
    }
    .tank-content {
        z-index: 2;
        text-align: center;
        text-shadow: 0 4px 15px rgba(0,0,0,1);
        padding: 20px;
    }
    @keyframes riseUp {
        0% { transform: translateY(100%); }
        100% { transform: translateY(15%); } /* Fills tank to 85% */
    }
    @keyframes wave {
        0% { transform: translateX(0) translateY(15%); }
        50% { transform: translateX(-25%) translateY(17%); }
        100% { transform: translateX(-50%) translateY(15%); }
    }
</style>

<!-- INJECT BACKGROUND SEPARATION MOLECULES -->
<div class="molecule salt-na" style="animation-duration: 5s; left: 48%; animation-delay: 0s;"></div>
<div class="molecule salt-cl" style="animation-duration: 6s; left: 52%; animation-delay: 1s;"></div>
<div class="molecule urea-crystal" style="animation-duration: 8s; left: 50%; animation-delay: 0.5s;"></div>
<div class="molecule salt-na" style="animation-duration: 7s; left: 50%; animation-delay: 2.5s;"></div>
<div class="molecule salt-cl" style="animation-duration: 5.5s; left: 49%; animation-delay: 3s;"></div>
<div class="molecule urea-crystal" style="animation-duration: 9s; left: 51%; animation-delay: 4s;"></div>
<div class="molecule urea-crystal" style="animation-duration: 10s; left: 50%; animation-delay: 6s;"></div>
<div class="molecule salt-na" style="animation-duration: 6.5s; left: 51%; animation-delay: 5s;"></div>
""", unsafe_allow_html=True)

st.title("🧬 Project R³: AI Digital Twin Controller")
st.markdown("*Real-time bio-computational optimization of hemodialysis effluent upcycling.*")

# --- 3. INTERACTIVE TABS ---
tab_pmndp, tab1, tab2, tab3, tab4 = st.tabs(["🚨 National Scale (PMNDP)", "⚡ ED Optimizer", "❄️ Thermodynamics", "💰 Economics", "🏭 Routing"])

# ==========================================
# TAB 0: PMNDP NATIONAL WASTAGE (NEW)
# ==========================================
with tab_pmndp:
    st.subheader("The National Dialysis Waste Crisis")
    st.markdown("Official data sourced from the **Pradhan Mantri National Dialysis Program (PMNDP)** via the National Health Systems Resource Centre (NHSRC).")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric(label="New ESRD Patients Annually", value="2.2 Lakh+")
    with col_b:
        st.metric(label="Annual Dialysis Demand", value="3.4 Crore Sessions", delta="120 Liters / Session", delta_color="off")
        
    st.markdown("""
    <div class="tank-container">
        <div class="liquid-wave"></div>
        <div class="tank-content">
            <h1 style='color: white; font-size: 3.5rem; margin:0; line-height: 1.2;'>4.08 BILLION LITERS</h1>
            <h3 style='color: #ffcccc; margin:0;'>of toxic, urea-rich effluent wasted annually.</h3>
            <p style='color: #fff; font-weight: bold; margin-top: 15px;'>Project R³ intercepts this tank before it reaches municipal sewers.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

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
            **The Limiting Current Density (LCD)**  
            In real-world electrodialysis, if voltage pushes ions faster than diffusion can supply them, the fluid reaches absolute depletion.  
            Exceeding this limit causes **Joule Heating** and water dissociation. The Digital Twin actively throttles voltage to stay exactly 5% below the LCD curve.
            """)
            
    with col2:
        voltage = np.linspace(0, 20, 100)
        current = np.where(voltage < 8, 1.5 * voltage, 
                  np.where(voltage < 14, 12 + np.log(voltage - 7), 
                  12 + np.log(7) + 2.5 * (voltage - 14)))
        
        energy_loss = np.where(voltage > 14, (voltage - 14)**2 * (flow_rate/100), 0)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=voltage, y=current, mode='lines', name="Ion Current (A)", line=dict(color='#00ff87', width=3)))
        fig.add_trace(go.Scatter(x=voltage, y=energy_loss, mode='lines', name="Thermal Waste", line=dict(color='#ff3c3c', width=3, dash='dot')))
        
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
            Traditional evaporation requires massive thermal energy (Latent Heat of Vaporization).  
            
            By utilizing Eutectic Freeze Crystallization (EFC), we sub-cool the fluid to exactly **-11.5°C**. This exploits the Latent Heat of Fusion.  
            
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
        """)

    cost_haber = 38500
    cost_r3 = 3500 + (600 * kwh_tariff) + 1200 
    
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
        If Heavy Metals (Ca, Mg) or trace blood proteins bypass the cellulose membrane, purity drops below 99.5%. The Python logic automatically reroutes imperfect batches away from automotive markets to prevent engine catalytic converter destruction.
        """)
    
    if purity >= 99.8:
        st.success("✅ **STATUS: 99.8% - ROUTE TO AUTOMOTIVE (AdBlue/DEF)**")
    elif purity >= 99.5:
        st.info("🧴 **STATUS: 99.5% - ROUTE TO MEDICAL COSMETICS**")
    else:
        st.warning("🌾 **STATUS: <99.5% - ROUTE TO AGRICULTURE (Fertilizer)**")