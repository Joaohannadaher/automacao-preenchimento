# 🚀 QUICKSTART - Automação em Python

## Início Rápido em 5 Minutos

### 1. Preparar Autenticação

```bash
# Copie o arquivo .env.example
cp .env.example .env

# Edite o .env com suas credenciais Azure AD ou Usuário/Senha
# Opção A: Azure AD (RECOMENDADO)
# - Vá para https://portal.azure.com/
# - Create App Registration
# - Copie Client ID e Client Secret

# Opção B: Usuário/Senha (Menos seguro)
# - Use email e senha do Office 365
```

### 2. Instalar Dependências

**Windows:**
```bash
setup.bat
```

**Linux/Mac:**
```bash
bash setup.sh
```

**Manual:**
```bash
# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows

# Instalar pacotes
pip install -r requirements.txt
```

### 3. Executar

```bash
python automacao_sharepoint.py
```

**Esperado:**
```
Conectando ao SharePoint: https://suaempresa.sharepoint.com/sites/SeuSite
Conectado ao SharePoint com sucesso!
Buscando itens modificados após: 2026-03-10T...
Item 1: Demanda='Alimentador' → Responsável='responsavel.a@...'
```

### 4. Verificar Logs

```bash
# Windows
type automacao.log

# Linux/Mac
tail -f automacao.log
```

---

## 🧪 Testar sem SharePoint Real

```bash
# Executar apenas testes unitários
python test_automacao.py
```

Testes cobrem:
- ✅ Atribuição correta de responsáveis
- ✅ Case-insensitive (ALIMENTADOR, alimentador, Alimentador)
- ✅ Tratamento de campos vazios
- ✅ Evitar reprocessamento

---

## ⚙️ Configurações

**Arquivo: `automacao_sharepoint.py`**

Alterar intervalo de execução:
```python
# Padrão: 60 segundos
iniciar_automacao(intervalo_segundos=30)
```

Alterar intervalo de monitoramento:
```python
# Padrão: últimos 5 minutos
itens = self.obter_itens_nao_processados(minutos=10)
```

---

## 🔒 Segurança

### Azure AD (Melhor Prática)

1. Acesse https://portal.azure.com/
2. Vá para **Azure Active Directory** > **App registrations**
3. **+ New registration**
   - Name: `Automacao-SharePoint`
   - Supported account types: `Accounts in any organizational directory`
4. Na página do app, copie:
   - **Application (Client) ID**
   - **Directory (Tenant) ID**
5. Vá para **Certificates & secrets** > **+ New client secret**
   - Copie o **Value** (não ID)
6. No SharePoint, dê permissões ao app:
   - Vá para Site Settings > App permissions
   - Ou use PowerShell: `Grant-PnPAzureADAppSitePermission`

### No arquivo `.env`:
```env
AZURE_CLIENT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
AZURE_CLIENT_SECRET=seu-secret-aqui
```

---

## 📊 Estrutura de Pastas

```
.
├── automacao_sharepoint.py     # Script principal
├── test_automacao.py           # Testes unitários
├── requirements.txt            # Dependências Python
├── .env.example               # Template de configuração
├── .env                       # Suas credenciais (NÃO COMMIT!)
├── setup.bat                  # Setup para Windows
├── setup.sh                   # Setup para Linux/Mac
├── automacao.log             # Logs gerados
├── README_PYTHON.md          # Documentação completa
└── QUICKSTART.md             # Este arquivo
```

---

## 🐛 Solução de Problemas

| Erro | Solução |
|------|---------|
| `ModuleNotFoundError: No module named 'office365'` | Execute `pip install -r requirements.txt` |
| Erro de autenticação | Verifique `.env`; Teste credenciais no Azure Portal |
| `Lista não encontrada` | Verifique nome exato em `LIST_NAME` |
| Nenhum item atualizado | Crie novo item em SharePoint; Verifique nome dos campos |
| Script trava | Aumente `intervalo_segundos`; Verifique logs |

---

## 📝 Próximos Passos

1. ✅ Configurar `.env`
2. ✅ Executar `setup.bat` ou `setup.sh`
3. ✅ Testar com `python test_automacao.py`
4. ✅ Executar `python automacao_sharepoint.py`
5. ✅ Agendar em Task Scheduler (Windows) ou Cron (Linux)

---

## 💡 Dicas

- Use `tail -f automacao.log` para ver logs em tempo real
- Crie itens de teste no SharePoint para validar
- Monitore a primeira execução
- Defina alertas para erros críticos

---

## 📞 Precisa de Ajuda?

Verifique:
1. `README_PYTHON.md` - Documentação completa
2. `automacao.log` - Logs detalhados
3. `test_automacao.py` - Testes de validação

Bom uso! 🎉
