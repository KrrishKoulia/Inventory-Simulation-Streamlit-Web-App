import pandas as pd
from inventory.inventory_models import InventoryParams
from typing import Optional
import numpy as np

class InventorySimulation:
    """ Class to run inventory simulations and analyze results. """

    def __init__(self, params: InventoryParams):
        self.D = params.D
        self.T_total = params.T_total
        self.LD = params.LD
        self.T = params.T
        self.Q = params.Q
        self.initial_ioh = params.initial_ioh
        self.sigma = params.sigma
        
        # Daily demand rate
        self.D_day = self.D / self.T_total
        
        # Initialize DataFrame to store simulation results
        self.sim = pd.DataFrame({
            'time': np.array(range(1, self.T_total + 1))
        })
    
    def order(self, t, T, Q, start_day = 1):
        """ Simple Ordering Policy: Order Q units every T days starting from start_day. """
        return Q if (t>start_day and (t - start_day) % T == 0) else 0
    
    def order_leadtime(self, t, T, Q, LD, start_day = 1):
        """ Simple Ordering Policy: Order Q units every T days starting from start_day. """
        return Q if (t>start_day and ((t - start_day) + (LD-1)) % T == 0) else 0
    
    def simulation_1(self):
        """ Simple Fixed-cycle ordering policy simulation not considering lead time. """
        sim_1 = self.sim.copy()
        
        # Daily Demand
        sim_1['demand'] = self.D_day
        
        # Orders Placed
        T = int(self.T)
        Q = float(self.Q)
        sim_1['order'] = sim_1['time'].apply(lambda t: self.order(t, T, Q))
        
        # Orders Received (considering lead time)
        LD = int(self.LD)
        sim_1['receipt'] = sim_1['order'].shift(LD).fillna(0)
        
        # Inventory on Hand (IOH)
        ioh = [self.initial_ioh]
        for t in range(1, len(sim_1)):
            # substract demand
            new_ioh = ioh[-1] - sim_1.loc[t, 'demand']
            # add received orders
            new_ioh += sim_1.loc[t, 'receipt']
            # record new IOH
            ioh.append(new_ioh)
        sim_1['ioh'] = ioh
        
        return sim_1
    
    def simulation_2(self):
        """ Fixed-cycle ordering policy simulation considering lead time. """
        sim_1 = self.sim.copy()
        LD = int(self.LD)
        
        # Daily Demand
        sim_1['demand'] = self.D_day
        
        # Orders Placed
        T = int(self.T)
        Q = float(self.Q)
        sim_1['order'] = sim_1['time'].apply(lambda t: self.order_leadtime(t, T, Q, LD))
        
        # Orders Received (considering lead time)
        sim_1['receipt'] = sim_1['order'].shift(LD).fillna(0)
        
        # Inventory on Hand (IOH)
        ioh = [self.initial_ioh]
        for t in range(1, len(sim_1)):
            # substract demand
            new_ioh = ioh[-1] - sim_1.loc[t, 'demand']
            # add received orders
            new_ioh += sim_1.loc[t, 'receipt']
            # record new IOH
            ioh.append(new_ioh)
        sim_1['ioh'] = ioh
        
        return sim_1

    def simulation_3(self):
        """ Fixed-cycle ordering policy simulation considering lead time. """
        sim_1 = self.sim.copy()
        LD = int(self.LD)
        sigma = float(self.sigma)
        D_day = self.D_day
        T_total = int(self.T_total)
        
        # Daily Demand
        # sim_1['demand'] = self.D_day
        sim_1['demand'] = np.random.normal(loc=D_day, scale=sigma, size=T_total)
        
        # Orders Placed
        T = int(self.T)
        Q = float(self.Q)
        sim_1['order'] = sim_1['time'].apply(lambda t: self.order_leadtime(t, T, Q, LD))
        
        # Orders Received (considering lead time)
        sim_1['receipt'] = sim_1['order'].shift(LD).fillna(0)
        
        # Inventory on Hand (IOH)
        ioh = [self.initial_ioh]
        for t in range(1, len(sim_1)):
            # substract demand
            new_ioh = ioh[-1] - sim_1.loc[t, 'demand']
            # add received orders
            new_ioh += sim_1.loc[t, 'receipt']
            # record new IOH
            ioh.append(new_ioh)
        sim_1['ioh'] = ioh
        
        return sim_1
        
        
        
        