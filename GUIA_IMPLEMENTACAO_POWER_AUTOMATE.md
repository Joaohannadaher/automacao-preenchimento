# GUIA DE IMPLEMENTAÇÃO - AUTOMAÇÃO DE ATRIBUIÇÃO DE RESPONSÁVEIS

## 1. PRÉ-REQUISITOS

- ✅ Acesso ao Microsoft Power Automate (https://make.powerautomate.com)
- ✅ Acesso à lista SharePoint "Nome da Lista SharePoint"
- ✅ Permissões de edição na lista
- ✅ Conta de admin ou permissões de edição no Power Automate

---

## 2. PASSO A PASSO DE IMPLEMENTAÇÃO

### PASSO 1: Criar o Fluxo (Cloud Flow)

1. Acesse **Power Automate** → **Meus fluxos**
2. Clique em **+ Novo fluxo** → **Fluxo de nuvem automatizado**
3. Nome do fluxo: `Atribuir Responsável - Nome da Lista SharePoint`
4. Gatilho: Procure por **"SharePoint"** → Selecione **"Quando um item é criado ou modificado"**

### PASSO 2: Configurar o Gatilho (Trigger)

```
Tipo: Quando um item é criado ou modificado
Local do site: https://suaempresa.sharepoint.com/sites/SeuSite
Lista: Nome da Lista SharePoint
```

**Campos a preencher:**
- **Site Address**: `https://suaempresa.sharepoint.com/sites/SeuSite`
- **List Name**: `Nome da Lista SharePoint`

---

### PASSO 3: Adicionar Ação - Obter Item

Vamos buscar os dados completos do item para trabalhar com eles.

1. Clique em **+ Nova etapa**
2. Procure por **"SharePoint"** → Selecione **"Obter item"**
3. Configure:
   - **Site Address**: `https://suaempresa.sharepoint.com/sites/SeuSite`
   - **List Name**: `Nome da Lista SharePoint`
   - **ID do Item**: `ID` (do trigger)

---

### PASSO 4: Adicionar Ação - Condição (IF/ELSE)

1. Clique em **+ Nova etapa**
2. Procure por **"Controle"** → Selecione **"Condição"**

Aqui vamos verificar se o campo "Demanda" está preenchido (não vazio).

**Configurar a primeira condição:**

```
Escolha um valor: [Demanda]  (do item obtido em PASSO 3)
é igual a: (deixar em branco ou selecionar "não contém")
```

Na verdade, vamos fazer assim:

```
Escolha um valor: Demanda
Operador: é igual a
Valor: (deixar vazio)
```

E usar **"não é igual a"** para verificar se NÃO está vazio.

**Melhor abordagem:**
```
Escolha um valor: Demanda
Operador: não é igual a
Valor: (deixar em branco)
```

---

### PASSO 5: Configurar o Ramo "SIM" (Demanda não está vazio)

1. No ramo **"Sim"** da condição, adicione outra condição aninhada
2. Esta condição vai verificar se Demanda = "Alimentador" OU "Obras Reguladas"

```
Escolha um valor: Demanda
Operador: é igual a
Valor: Alimentador
```

**Usar operador "ou":**

```
Condição 1: Demanda é igual a "Alimentador"
OU
Condição 2: Demanda é igual a "Obras Reguladas"
```

---

### PASSO 6: Ações no Ramo "SIM" da Segunda Condição

Se Demanda = "Alimentador" OU "Obras Reguladas":

1. Clique em **Adicionar uma ação** dentro do ramo "Sim"
2. Procure por **"SharePoint"** → **"Atualizar item"**

Configure:
```
Site Address: https://suaempresa.sharepoint.com/sites/SeuSite
List Name: Nome da Lista SharePoint
ID: ID (do item original)
Responsavel Pendencia: responsavel.a@suaempresa.com.br
```

---

### PASSO 7: Ações no Ramo "NÃO" (Outro valor para Demanda)

Se Demanda = qualquer outro valor:

1. Clique em **Adicionar uma ação** dentro do ramo "Não"
2. Procure por **"SharePoint"** → **"Atualizar item"**

Configure:
```
Site Address: https://suaempresa.sharepoint.com/sites/SeuSite
List Name: Nome da Lista SharePoint
ID: ID (do item original)
Responsavel Pendencia: responsavel.b@suaempresa.com.br
```

---

### PASSO 8: Tratamento de Erros

1. Adicione uma ação **"Enviar um email"** após a segunda condição para tratamento de erro
2. Configure a notificação de falha (opcional, mas recomendado)

```
Destinatário: [admin email]
Assunto: Erro na Automação - Nome da Lista SharePoint
Corpo: Falha ao atualizar item ID: @{triggerOutputs()?['body/ID']}
```

---

## 3. ESTRUTURA VISUAL DO FLUXO

```
[GATILHO] Quando um item é criado ou modificado
    ↓
[AÇÃO] Obter item
    ↓
[CONDIÇÃO 1] Demanda ≠ (vazio)?
    ├─ SIM → [CONDIÇÃO 2] Demanda = "Alimentador" OU "Obras Reguladas"?
    │         ├─ SIM → [AÇÃO] Atualizar item: responsavel.a@suaempresa.com.br
    │         └─ NÃO → [AÇÃO] Atualizar item: responsavel.b@suaempresa.com.br
    └─ NÃO → [FIM] Nenhuma ação (Demanda está vazio)
```

---

## 4. EXPRESSÕES E FORMULAS

### Para verificar se campo está vazio (se necessário usar expressão):

```
empty(triggerBody()?['Demanda'])
```

### Para comparação de texto (case-insensitive):

```
equals(toLower(triggerBody()?['Demanda']), 'alimentador')
```

---

## 5. TESTE E VALIDAÇÃO

### Checklist de Testes:

- [ ] Criar item com Demanda = "Alimentador" → Deve atribuir responsavel.a@...
- [ ] Criar item com Demanda = "Obras Reguladas" → Deve atribuir responsavel.a@...
- [ ] Criar item com Demanda = "Outro valor" → Deve atribuir responsavel.b@...
- [ ] Criar item com Demanda = (em branco) → Não deve atualizar responsável
- [ ] Modificar item existente → Regras devem se aplicar novamente
- [ ] Verificar histórico de alterações no SharePoint

---

## 6. ATIVAÇÃO

1. Clique em **Salvar** no Power Automate
2. Clique em **Ligar** para ativar o fluxo
3. Monitore os primeiros testes na aba **"Execuções"**

---

## 7. MONITORAMENTO

- Acesse **Power Automate** → **Meus fluxos** → Clique no fluxo
- Abra **"Análise"** para ver estatísticas de execução
- Verifique **"Execuções"** para ver histórico de cada execução (sucesso/falha)

---

## 8. TROUBLESHOOTING

| Problema | Solução |
|----------|---------|
| Fluxo não é acionado | Verifique se o fluxo está ativado; Teste criar um novo item |
| Campo "Responsavel Pendencia" não é atualizado | Verifique nome exato do campo; Confirme permissões de escrita |
| Erro na ação "Atualizar item" | Verifique se ID está correto; Tente obter item primeiro |
| Fluxo executa infinitamente | Adicione condição para ignorar se o campo já está preenchido |

---

## 9. PRÓXIMOS PASSOS

1. ✅ Implementar conforme este guia
2. ✅ Testar com casos de teste fornecidos
3. ✅ Validar com stakeholders
4. ✅ Ativar em produção
5. ✅ Monitorar por 7 dias
6. ✅ Documentar conclusões
