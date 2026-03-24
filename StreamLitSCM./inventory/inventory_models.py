from pydantic import BaseModel, Field

class InventoryParams(BaseModel):
    """ Basic parameters for inventory operations. """
    D: float = Field(2000, gt=0, description="Annual Demand (units per year)")
    T_total: int = Field(365, ge=1, description="Days in the simulation horizon")
    LD: int = Field(0, ge=0, description="Lead Time (days)")
    T: int = Field(10, ge=1, description="Review Period (days)")
    Q: float = Field(0, ge=0, description="Order Quantity (units)")
    initial_ioh: float = Field(0, ge=0, description="Initial Inventory on Hand (units)")
    sigma: float = Field(0, ge=0, description="Standard Deviation of Daily Demand (units)")