# Development Workflow Guide

## 🚀 Quick Start

### Activate a Project Environment
```bash
# Activate environment
source activate_project.sh [PROJECT_NAME]

# Options:
# - econ       (Economic Indicators)
# - kpi        (KPI Recommender)
# - portfolio  (Portfolio Optimization)
# - analytics  (Product Analytics)
```

### When Done Working
```bash
deactivate
```

---

## 📝 Daily Tasks

### Run Jupyter Notebooks
```bash
# 1. Activate environment
source activate_project.sh econ

# 2. Start Jupyter
jupyter notebook

# 3. When done
deactivate
```

### Run Streamlit App Locally
```bash
# 1. Activate environment
source activate_project.sh portfolio

# 2. Navigate to project code
cd ../../projects/portfolio_optimization

# 3. Run Streamlit
streamlit run app.py

# 4. When done (Ctrl+C to stop server)
deactivate
```

### Edit Code in VS Code
```bash
# Just open VS Code - it will auto-detect environments
code .

# Or open the multi-project workspace
code portfolio-projects.code-workspace
```

---

## 📦 Managing Dependencies

### Add a New Library
```bash
# 1. Activate environment
source activate_project.sh econ

# 2. Add the library
uv add library-name

# 3. This automatically updates pyproject.toml and uv.lock
```

### Update Existing Libraries
```bash
# 1. Activate environment
source activate_project.sh econ

# 2. Update all dependencies
uv sync

# Or update specific library
uv add library-name@latest
```

### Remove a Library
```bash
# 1. Activate environment
source activate_project.sh econ

# 2. Remove it
uv remove library-name
```

---

## 🐳 Docker Deployment

### Build Docker Image Locally
```bash
# Build for specific project
docker build --build-arg PROJECT_NAME=economic_indicators -t econ-app .

# Test it
docker run -p 8501:8501 econ-app
```

### Deploy to GitHub (Auto-builds via Actions)
```bash
git add .
git commit -m "Your update message"
git push
```

---

## 🔍 Troubleshooting

### Environment Not Activating
```bash
# Manually activate
cd envs/economic_indicators
source .venv/bin/activate
```

### VS Code Can't Find Python

1. Press `Cmd + Shift + P`
2. Type: `Python: Select Interpreter`
3. Choose: `./envs/PROJECT_NAME/.venv/bin/python`

### Libraries Not Found
```bash
# Resync environment
cd envs/economic_indicators
uv sync
```

### Start Fresh
```bash
# Delete environment and recreate
cd envs/economic_indicators
rm -rf .venv
uv venv
uv sync
```

---

## 📋 Project Structure
```
portfolio.github.io/
├── envs/                          # Virtual environments
│   ├── economic_indicators/
│   │   ├── .venv/                # Python environment (local only)
│   │   ├── pyproject.toml        # Dependencies
│   │   └── uv.lock              # Locked versions
│   ├── kpi_recommender_system/
│   ├── portfolio_optimization/
│   └── product_analytics/
├── projects/                      # Actual code
│   ├── economic_indicators/
│   ├── kpi_recommender_system/
│   ├── portfolio_optimization/
│   └── product_analytics/
├── docs/                         # GitHub Pages
├── activate_project.sh           # Helper script
└── Dockerfile                    # Docker build
```

---

## ✅ Best Practices

1. **Always activate environment before working**
2. **Use `uv add` to add dependencies** (not pip)
3. **Commit `pyproject.toml` and `uv.lock`** (not `.venv/`)
4. **Test locally before pushing**
5. **Use descriptive commit messages**

