# Environment Catalog

## Base Environment
- Python: 3.11
- Purpose: Shared analytics + dev tooling
- Location: envs/base
- Lockfile: uv.lock

## economic_indicators
- Code: projects/economic_indicators
- Purpose: Streamlit dashboard + notebooks
- Dependencies: streamlit, altair
- Environment: envs/economic_indicators
- Lockfile: uv.lock

## kpi_recommender_system
- Code: projects/kpi_recommender_system
- Purpose: Forecasting pipeline
- Dependencies: statsmodels, prophet
- Environment: envs/kpi_recommender_system

## portfolio_optimization
- Code: projects/portfolio_optimization
- Purpose: Streamlit dashboard + notebooks
- Dependencies: streamlit, altair
- Environment: envs/portfolio_optimization
- Lockfile: uv.lock

## product analytics
- Code: projects/product analytics
- Purpose: Streamlit dashboard + notebooks
- Dependencies: streamlit, altair
- Environment: envs/product analytics
- Lockfile: uv.lock

## roof revival
- Code: projects/roof revival
- Purpose: Streamlit dashboard + notebooks
- Dependencies: streamlit, altair
- Environment: envs/roof revival
- Lockfile: uv.lock



## Regenerating Lockfiles
Run:
python scripts/regen_lockfiles.py