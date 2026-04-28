#!/bin/bash

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

case "$1" in
    econ|economic)
        cd envs/economic_indicators
        source .venv/bin/activate
        cd ../../projects/economic_indicators
        echo -e "${GREEN}✅ Economic Indicators environment activated${NC}"
        echo -e "${BLUE}📂 Current directory: $(pwd)${NC}"
        echo -e "${BLUE}🐍 Python: $(python --version)${NC}"
        echo -e "${YELLOW}💡 Run 'jupyter notebook' to start working${NC}"
        ;;
    kpi)
        cd envs/kpi_recommender_system
        source .venv/bin/activate
        cd ../../projects/kpi_recommender_system
        echo -e "${GREEN}✅ KPI Recommender environment activated${NC}"
        echo -e "${BLUE}📂 Current directory: $(pwd)${NC}"
        echo -e "${BLUE}🐍 Python: $(python --version)${NC}"
        echo -e "${YELLOW}💡 Run 'jupyter notebook' to start working${NC}"
        ;;
    portfolio|port)
        cd envs/portfolio_optimization
        source .venv/bin/activate
        cd ../../projects/portfolio_optimization
        echo -e "${GREEN}✅ Portfolio Optimization environment activated${NC}"
        echo -e "${BLUE}📂 Current directory: $(pwd)${NC}"
        echo -e "${BLUE}🐍 Python: $(python --version)${NC}"
        echo -e "${YELLOW}💡 Run 'jupyter notebook' to start working${NC}"
        ;;
    analytics|product)
        cd envs/product_analytics
        source .venv/bin/activate
        cd ../../projects/product_analytics
        echo -e "${GREEN}✅ Product Analytics environment activated${NC}"
        echo -e "${BLUE}📂 Current directory: $(pwd)${NC}"
        echo -e "${BLUE}🐍 Python: $(python --version)${NC}"
        echo -e "${YELLOW}💡 Run 'jupyter notebook' to start working${NC}"
        ;;
    roof|roofmaxx)
        cd envs/roof_maxx_analytics
        source .venv/bin/activate
        cd ../../projects/roof_maxx_analytics
        echo -e "${GREEN}✅ Roof Maxx Analytics environment activated${NC}"
        echo -e "${BLUE}📂 Current directory: $(pwd)${NC}"
        echo -e "${BLUE}🐍 Python: $(python --version)${NC}"
        echo -e "${YELLOW}💡 Run 'jupyter notebook' or 'streamlit run app/streamlit_dashboard.py'${NC}"
        ;;
    nlp|tickets)
        cd envs/nlp_ticket_classifier
        source .venv/bin/activate
        cd ../../projects/nlp_ticket_classifier
        echo -e "${GREEN}✅ NLP Ticket Classifier environment activated${NC}"
        echo -e "${BLUE}📂 Current directory: $(pwd)${NC}"
        echo -e "${BLUE}🐍 Python: $(python --version)${NC}"
        echo -e "${YELLOW}💡 Run 'jupyter notebook' or 'streamlit run app/streamlit_dashboard.py'${NC}"
        ;;
    *)
        echo "Usage: source activate_project.sh [PROJECT]"
        echo ""
        echo "Available projects:"
        echo "  econ       - Economic Indicators"
        echo "  kpi        - KPI Recommender System"
        echo "  portfolio  - Portfolio Optimization"
        echo "  analytics  - Product Analytics"
        echo "  roof       - Roof Maxx Analytics"
        echo "  nlp        - NLP Ticket Classifier"
        return 1
        ;;
esac

chmod +x activate_project.sh