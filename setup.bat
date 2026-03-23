@echo off
REM Script de Setup - Automação SharePoint
REM Executa instalação inicial e configuração (Windows)

setlocal enabledelayedexpansion

echo.
echo ======================================================
echo   SETUP - Automacao SharePoint
echo   Version 1.0
echo ======================================================
echo.

REM Verificar Python
echo Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado. Instale Python 3.8+
    pause
    exit /b 1
)
python --version

echo.
echo Criando ambiente virtual...
python -m venv venv

echo.
echo Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo.
echo Instalando dependencias...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo Criando arquivo .env...
if not exist .env (
    copy .env.example .env
    echo [OK] Arquivo .env criado. EDITE com suas credenciais!
) else (
    echo [OK] Arquivo .env ja existe (nao sobrescrito)
)

echo.
echo Executando testes...
python test_automacao.py

echo.
echo ======================================================
echo   Setup Concluido!
echo ======================================================
echo.
echo Proximos passos:
echo 1. Edite o arquivo .env com suas credenciais
echo 2. Execute: python automacao_sharepoint.py
echo 3. Verifique logs em: automacao.log
echo.

pause
