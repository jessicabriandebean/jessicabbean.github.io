#!/bin/bash

# Color codes for better visibility
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

case "$1" in
    econ|economic)
        cd envs/economic_indicators
        source .venv/bin/activate
        echo -e "${GREEN}✅ Economic Indicators environment activated${NC}"
        echo -e "${BLUE}📂 Code: projects/economic_indicators/${NC}"
        echo -e "${BLUE}🐍 Python: $(python --version)${NC}"
        ;;
    kpi)
        cd envs/kpi_recommender_system
        source .venv/bin/activate
        echo -e "${GREEN}✅ KPI Recommender environment activated${NC}"
        echo -e "${BLUE}📂 Code: projects/kpi_recommender_system/${NC}"
        echo -e "${BLUE}🐍 Python: $(python --version)${NC}"
        ;;
    portfolio|port)
        cd envs/portfolio_optimization
        source .venv/bin/activate
        echo -e "${GREEN}✅ Portfolio Optimization environment activated${NC}"
        echo -e "${BLUE}📂 Code: projects/portfolio_optimization/${NC}"
        echo -e "${BLUE}🐍 Python: $(python --version)${NC}"
        ;;
    analytics|product)
        cd envs/product_analytics
        source .venv/bin/activate
        echo -e "${GREEN}✅ Product Analytics environment activated${NC}"
        echo -e "${BLUE}📂 Code: projects/product_analytics/${NC}"
        echo -e "${BLUE}🐍 Python: $(python --version)${NC}"
        ;;
    *)
        echo "Usage: source activate_project.sh [PROJECT]"
        echo ""
        echo "Available projects:"
        echo "  econ       - Economic Indicators"
        echo "  kpi        - KPI Recommender System"
        echo "  portfolio  - Portfolio Optimization"
        echo "  analytics  - Product Analytics"
        return 1
        ;;
esac
