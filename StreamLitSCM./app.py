import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from inventory.inventory_analysis import InventorySimulation 
from inventory.inventory_models import InventoryParams
seed = 2006
np.random.seed(seed)

st.set_page_config(page_title = 'Inventory Simulation - Streamlit',layout = 'wide')


# Sidebar
with st.sidebar:
        st.markdown('**Inventory Parameters**')
        D = st.number_input("Annual Demand D ( Units/year)", min_value= 1, value = 2000 , step = 50)
        T_total = st.number_input("Horizon T_total ( Days)", min_value= 1, value = 365 , step = 1)
        LD = st.number_input("Lead Time LD (Days)", min_value= 0, value = 0 , step = 1)
        T = st.number_input("Cycle Time T (Days)", min_value= 1, value = 10 , step = 1)
        Q = st.number_input("Order Quantity Q (Units)", min_value= 0.0, value = 55.0 , step = 1.0,
                            format= '%.2f')
        initial_ioh = st.number_input('Initial Inventory on Hand ', min_value=0.0 , value=55.0 , step = 1.0,
                                      format= '%.2f')
        Daily_demand_std = st.number_input('Daily demand std.dev (units/day) ', min_value=0.0 , value=0.0 , step = 0.1,
                                      format= '%.2f')
