#!/bin/bash

# 🚀 Technical Documentation Generator - Setup & Run Script

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║   📚 Technical Documentation Generator - Setup Helper          ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}📋 Checking requirements...${NC}"
echo ""

# Check Python
if command -v python3 &> /dev/null; then
    PY_VERSION=$(python3 --version)
    echo -e "${GREEN}✅ Python found: $PY_VERSION${NC}"
else
    echo -e "${YELLOW}❌ Python not found. Please install Python 3.8+${NC}"
    exit 1
fi

# Check pip
if command -v pip3 &> /dev/null; then
    echo -e "${GREEN}✅ pip found${NC}"
else
    echo -e "${YELLOW}❌ pip not found. Please install pip${NC}"
    exit 1
fi

echo ""
echo -e "${BLUE}📦 Installing dependencies...${NC}"
pip3 install -q -r requirements.txt
echo -e "${GREEN}✅ Dependencies installed${NC}"

echo ""
echo -e "${BLUE}🧪 Running basic validation...${NC}"
python3 -c "
import sys
try:
    from flask import Flask
    print('✅ Flask imported successfully')
    from openai import OpenAI
    print('✅ OpenAI SDK imported successfully')
    print('✅ All dependencies verified')
except Exception as e:
    print(f'❌ Error: {e}')
    sys.exit(1)
"

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                        🎉 Ready to Go!                         ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

echo -e "${YELLOW}📖 Quick Start:${NC}"
echo ""
echo "1. Run the API server:"
echo -e "   ${BLUE}python3 api_server.py${NC}"
echo ""
echo "2. In another terminal, test the API:"
echo -e "   ${BLUE}curl http://localhost:5000/health${NC}"
echo ""
echo "3. Run the example client:"
echo -e "   ${BLUE}python3 example_client.py${NC}"
echo ""
echo "4. Or use Docker:"
echo -e "   ${BLUE}docker-compose up${NC}"
echo ""

echo -e "${YELLOW}📚 Documentation:${NC}"
echo ""
echo "  • ${BLUE}INDEX.md${NC}                    - Mapa del proyecto"
echo "  • ${BLUE}README.md${NC}                   - Documentación completa"
echo "  • ${BLUE}QUICK_REFERENCE.md${NC}         - Referencia rápida"
echo "  • ${BLUE}N8N_INTEGRATION.md${NC}         - Integración n8n"
echo "  • ${BLUE}PROJECT_SUMMARY.md${NC}         - Resumen ejecutivo"
echo "  • ${BLUE}VALIDATION.md${NC}              - Validación del sistema"
echo "  • ${BLUE}openapi.json${NC}               - Especificación OpenAPI"
echo ""

echo -e "${YELLOW}🧪 Testing:${NC}"
echo -e "   ${BLUE}python3 test_generators.py${NC}"
echo ""

echo -e "${GREEN}¡Todo listo para comenzar! 🚀${NC}"
echo ""
