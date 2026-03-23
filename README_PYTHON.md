# AUTOMAÇÃO SHAREPOINT - Python

## Visão Geral

Script Python que automatiza a atribuição de responsáveis na lista SharePoint "Nome da Lista SharePoint" conforme regras de negócio predefinidas.

**Versão**: 1.0
**Última Atualização**: 2026-03-10

---

## 📋 Pré-requisitos

- Python 3.8+
- Acesso ao SharePoint Online
- Permissões de leitura e escrita na lista "Nome da Lista SharePoint"
- Credenciais de autenticação (Azure AD ou Usuário/Senha)

---

## 🚀 Instalação

### 1. Clonar ou baixar os arquivos

```bash
cd "C:\caminho\para\Automação preenchimento"
```

### 2. Criar ambiente virtual (recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar autenticação

**Opção A: Azure AD (RECOMENDADO)**

1. Acesse [Azure Portal](https://portal.azure.com/)
2. Navegue para **Azure Active Directory** → **App registrations**
3. Clique em **+ New registration**
4. Nome: `Automacao-SharePoint`
5. Selecione **Accounts in any organizational directory**
6. Clique em **Register**
7. Copie o **Application (client) ID** e **Tenant ID**
8. Vá para **Certificates & secrets** → **+ New client secret**
9. Copie o valor do secret

**Arquivo `.env`:**
```env
AZURE_CLIENT_ID=seu-client-id
AZURE_CLIENT_SECRET=seu-client-secret
SHAREPOINT_SITE_URL=https://suaempresa.sharepoint.com/sites/SeuSite
```

**Opção B: Autenticação Básica (Menos seguro)**

Copie `.env.example` para `.env` e preencha:

```env
SHAREPOINT_USERNAME=seu-usuario@suaempresa.com.br
SHAREPOINT_PASSWORD=sua-senha
SHAREPOINT_SITE_URL=https://suaempresa.sharepoint.com/sites/SeuSite
```

---

## ▶️ Como Usar

### Executar manualmente

```bash
python automacao_sharepoint.py
```

### Executar em background (Windows)

```bash
start /B python automacao_sharepoint.py
```

### Executar com agendamento (Windows Task Scheduler)

1. Abra **Task Scheduler**
2. **Create Basic Task**
3. Nome: `Automacao Controle Notas CM`
4. Trigger: **Daily** às 8:00 AM
5. Action:
   - Program: `C:\caminho\para\python.exe`
   - Arguments: `C:\caminho\para\Automação preenchimento\automacao_sharepoint.py`
   - Start in: `C:\caminho\para\Automação preenchimento`

---

## 📊 Como Funciona

### Fluxo de Execução

```
1. Conecta ao SharePoint
2. Obtém itens modificados nos últimos 5 minutos
3. Para cada item:
   a. Verifica valor do campo "Demanda"
   b. Aplica regras de negócio
   c. Atualiza campo "Responsavel Pendencia"
4. Registra log de execução
5. Aguarda próxima execução
```

### Regras de Negócio

| Valor de "Demanda" | Responsável | Email |
|---|---|---|
| Alimentador | Responsável A | responsavel.a@suaempresa.com.br |
| Obras Reguladas | Responsável A | responsavel.a@suaempresa.com.br |
| Outro valor | Responsável B | responsavel.b@suaempresa.com.br |
| (vazio) | Nenhuma ação | — |

### Intervalo de Execução

Por padrão, a automação executa a cada **60 segundos**.

Para alterar, modifique no final do arquivo `automacao_sharepoint.py`:

```python
if __name__ == '__main__':
    iniciar_automacao(intervalo_segundos=30)  # 30 segundos
```

---

## 📝 Logging

Os logs são salvos em `automacao.log` e também exibidos no console.

**Formato:**
```
2026-03-10 14:23:45,123 - INFO - Item 42: Demanda='Alimentador' → Responsável='responsavel.a@...'
```

**Exemplo de visualizar logs:**
```bash
# Windows
type automacao.log

# Linux/Mac
tail -f automacao.log
```

---

## 🔧 Configurações Avançadas

### Alterar Intervalo de Monitoramento

Modifique o parâmetro `minutos` em `obter_itens_nao_processados()`:

```python
def obter_itens_nao_processados(self, minutos=10):  # Agora verifica últimos 10 minutos
    # ...
```

### Adicionar Novos Responsáveis

Edite o dicionário `RESPONSAVEIS` em `automacao_sharepoint.py`:

```python
RESPONSAVEIS = {
    'alimentador': 'responsavel.a@suaempresa.com.br',
    'obras reguladas': 'responsavel.a@suaempresa.com.br',
    'novo tipo': 'novo.responsavel@suaempresa.com.br',
    'default': 'responsavel.b@suaempresa.com.br'
}
```

### Customizar Filtro de Itens

Modifique a query CAML em `obter_itens_nao_processados()` para filtrar por outros critérios.

---

## 🐛 Troubleshooting

| Problema | Solução |
|----------|---------|
| Erro de autenticação | Verifique credenciais em `.env`; Teste a conexão |
| Lista não encontrada | Verifique nome exato da lista: `LIST_NAME` |
| Campo não atualizado | Confirme nomes dos campos em SharePoint (case-sensitive) |
| Script trava | Aumente `intervalo_segundos` ou reduza `minutos` em `obter_itens_nao_processados()` |
| Erro de permissão | Verifique permissões de escrita na lista |

**Teste de conexão:**

```python
from automacao_sharepoint import AutomacaoSharePoint

try:
    automacao = AutomacaoSharePoint()
    print("✅ Conectado com sucesso!")
except Exception as e:
    print(f"❌ Erro: {e}")
```

---

## 📈 Monitoramento

### Verificar execução

1. Abra arquivo `automacao.log`
2. Procure por mensagens de sucesso:
   ```
   Item XX atualizado com sucesso!
   ```

### Alertas de Erro

Se houver erro crítico, será registrado em `automacao.log`:

```
ERROR - Erro ao conectar ao SharePoint: [detalhes]
```

---

## 🔒 Segurança

- ✅ Use **Azure AD** para autenticação (mais seguro)
- ✅ Nunca commit `.env` no Git
- ✅ Adicione `.env` ao `.gitignore`
- ✅ Rotacione secrets regularmente
- ✅ Use HTTPS apenas
- ✅ Monitore logs para atividades suspeitas

---

## 📞 Suporte

Para dúvidas ou problemas:

1. Verifique os logs em `automacao.log`
2. Teste a conexão com o SharePoint
3. Valide as regras de negócio
4. Contacte o administrador do SharePoint

---

## 📜 Histórico de Mudanças

### v1.0 (2026-03-10)
- ✅ Implementação inicial
- ✅ Suporte a Azure AD e autenticação básica
- ✅ Logging detalhado
- ✅ Agendamento periódico

---

## 📄 Licença

Uso interno
