
# Inventory Simulation — Streamlit Web App

Turn a Python inventory simulation into a **single-page web app** your team can use.  
The app lets you test **fixed-cycle replenishment** under deterministic and stochastic demand, visualize **Demand / Orders / IOH**, and compare simple vs **lead-time-aware** ordering.

- Click **Run simulation** once; after that, any parameter change **auto-recomputes** and redraws.
- Results are **reproducible** (fixed random seed).
- Engine modules remain **as-is**, wrapped with a minimal Streamlit UI.

- ## Features

- Deterministic and stochastic demand simulations
- Simple Ordering vs Lead-time Ordering (receipt timing aligned with cycle end)
- Compact **3-panel chart** (Demand / Orders / IOH)
- Inline **Quick Context** cards (core inputs at a glance)
- KPIs: **Stockout days**, **Min IOH**, **Avg IOH**
- Auto re-run after initial click


## Architecture

```
Streamlit UI (app.py)
↓
Inventory Models (pydantic) — inventory_models.py
↓
Simulation Engine (pandas / numpy) — inventory_analysis.py
```

- The UI only orchestrates inputs, rendering, and calling the existing engine.
- You can later expose the engine via **FastAPI** or integrate with other frontends.

## Prerequisites

- **Python 3.10+**
- Git (optional)

- ## Project structure

```
StreamLitSCM/
├─ app.py
├─ main.py
├─ requirements.txt
├─ README.md
├─ pyproject.toml
├─ .gitignore
├─ .python-version
├─ uv.lock
├─ fun.
└─ inventory/
   ├─ __init__.py
   ├─ inventory_analysis.py
   └─ inventory_models.py
```


- Inventory Management Tutorial Source Code: https://github.com/samirsaci/tuto_inventory
- One of:
  - **Linux**: `uv` (recommended) or `pip`
 
