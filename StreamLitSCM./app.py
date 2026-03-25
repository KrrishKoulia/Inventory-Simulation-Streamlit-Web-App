import sys
import os

# Fix import paths for Streamlit Cloud
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set matplotlib backend before importing
import matplotlib
matplotlib.use('Agg')

import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from inventory.inventory_analysis import InventorySimulation 
from inventory.inventory_models import InventoryParams

# Fixed seed for reproducibility
seed = 2006
np.random.seed(seed)

# Setup state variable for run
if 'has_run' not in st.session_state:
    st.session_state.has_run = False

st.set_page_config(page_title='Inventory Simulation - Streamlit', layout='wide')

# Sidebar
with st.sidebar:
    st.markdown('**Inventory Parameters**')
    D = st.number_input("Annual Demand D (Units/year)", min_value=1, value=2000, step=50)
    T_total = st.number_input("Horizon T_total (Days)", min_value=1, value=365, step=1)
    LD = st.number_input("Lead Time LD (Days)", min_value=0, value=0, step=1)
    T = st.number_input("Cycle Time T (Days)", min_value=1, value=10, step=1)
    Q = st.number_input("Order Quantity Q (Units)", min_value=0.0, value=55.0, step=1.0, format='%.2f')
    initial_ioh = st.number_input('Initial Inventory on Hand', min_value=0.0, value=55.0, step=1.0, format='%.2f')
    sigma = st.number_input('Daily demand std.dev (units/day)', min_value=0.0, value=0.0, step=0.1, format='%.2f')
    method = st.radio(
        'Ordering Method',
        options=['Simple Ordering', 'Lead-Time Ordering'],
        index=0
    )

    run = st.button('Run Simulation', type='primary')

    if run:
        st.session_state.has_run = True

# Main Page
st.title('Inventory Simulation Web Application')

# Daily Demand
D_day = D / T_total

# Formatting of input parameters cards
st.markdown("""
<style>
.quick-card{padding:.9rem 1rem;border:1px solid #eaeaea;border-radius:12px;background:#fff;box-shadow:0 1px 2px rgba(0,0,0,.03)}
.quick-card .label{font-size:.85rem;color:#5f6b7a;margin:0}
.quick-card .value{font-size:1.25rem;font-weight:700;margin:.15rem 0 0 0;color:#111}
.quick-card .unit{font-size:.8rem;color:#8a95a3;margin:0}
</style>
""", unsafe_allow_html=True)

def quick_card(label, value, unit=""):
    unit_html = f'<p class="unit">{unit}</p>' if unit else ""
    st.markdown(f'<div class="quick-card"><p class="label">{label}</p><p class="value">{value}</p>{unit_html}</div>', unsafe_allow_html=True)

c1, c2, c3, c4, c5, c6 = st.columns(6)
with c1:
    quick_card('Average daily demand', f"{D_day:,.2f}", 'units/day')
with c2:
    quick_card('Lead Time', f"{LD:,.2f}", 'days')
with c3:
    quick_card('Cycle Time', f"{T}", 'days')
with c4:
    quick_card('Order Quantity', f"{Q:,.2f}", 'units')
with c5:
    quick_card('Initial IOH', f"{initial_ioh:,.2f}", 'units')
with c6:
    quick_card('Demand Std Dev', f"{sigma:,.2f}", 'units/day')

if st.session_state.has_run:
    # Do the calculation
    params = InventoryParams(
        D=float(D),
        T_total=int(T_total),
        LD=int(LD),
        T=int(T),
        Q=float(Q),  # Changed to float to match input
        initial_ioh=float(initial_ioh),
        sigma=float(sigma)
    )
    
    # Create simulation
    sim_engine = InventorySimulation(params)

    # Define the logic - FIXED: now properly differentiates methods
    if method == 'Lead-Time Ordering':
        df = sim_engine.simulation_2()  # Lead-time aware ordering
    else:
        df = sim_engine.simulation_1()  # Simple ordering

    # Calculate key parameters
    stockouts = (df["ioh"] < 0).sum()
    min_ioh = df["ioh"].min()
    avg_ioh = df["ioh"].mean()

    # Plot
    fig, axes = plt.subplots(3, 1, figsize=(9, 4), sharex=True)

    # Plot demand
    df.plot(x='time', y='demand', ax=axes[0], color='red', legend=False, grid=True)
    axes[0].set_ylabel('Demand', fontsize=8)

    # Orders
    df.plot.scatter(x='time', y='order', ax=axes[1], color='blue', legend=False, grid=True)
    axes[1].set_ylabel('Orders (units)', fontsize=8)

    # Inventory on Hand
    df.plot(x='time', y='ioh', ax=axes[2], color='green', legend=False, grid=True)
    axes[2].set_ylabel('Inventory On Hand (Units)', fontsize=8)

    # Format x axis
    axes[2].set_xlim(0, int(df['time'].max()))
    for ax in axes:
        ax.tick_params(axis='x', rotation=90, labelsize=6)
        ax.tick_params(axis='y', labelsize=6)

    plt.tight_layout()
    st.pyplot(fig, clear_figure=True, use_container_width=True)

    # Key parameters
    kpi_cols = st.columns(3)
    kpi_cols[0].metric("Stockout days", f"{stockouts}")
    kpi_cols[1].metric("Min IOH (units)", f"{min_ioh:,.0f}")
    kpi_cols[2].metric("Avg IOH (units)", f"{avg_ioh:,.0f}")

    st.success("Simulation completed.")

else:
    st.info('Set your parameters on the left and click Run Simulation')
