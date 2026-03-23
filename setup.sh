#!/bin/bash

# Script de Setup - Automação SharePoint
# Executa instalação inicial e configuração

echo "╔════════════════════════════════════════════════════╗"
echo "║  SETUP - Automação SharePoint                     ║"
echo "║  Version 1.0                                       ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

# Verificar Python
echo "✓ Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo "✗ Python 3 não encontrado. Instale Python 3.8+"
    exit 1
fi
python3 --version

echo ""
echo "✓ Criando ambiente virtual..."
python3 -m venv venv

echo ""
echo "✓ Ativando ambiente virtual..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

echo ""
echo "✓ Instalando dependências..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "✓ Criando arquivo .env..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "  → Arquivo .env criado. EDITE com suas credenciais!"
else
    echo "  → Arquivo .env já existe (não sobrescrito)"
fi

echo ""
echo "✓ Executando testes..."
python3 test_automacao.py

echo ""
echo "╔════════════════════════════════════════════════════╗"
echo "║  Setup Concluído!                                  ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""
echo "Próximos passos:"
echo "1. Edite o arquivo .env com suas credenciais"
echo "2. Execute: python automacao_sharepoint.py"
echo "3. Verifique logs em: automacao.log"
echo ""
