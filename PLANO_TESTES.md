# PLANO DE TESTES - AUTOMAÇÃO SHAREPOINT

**Data**: 2026-03-10
**Sistema**: Microsoft SharePoint Online + Power Automate
**Lista**: Nome da Lista SharePoint

---

## 1. OBJETIVOS DOS TESTES

- ✅ Validar que a automação executa corretamente em TODOS os cenários
- ✅ Garantir que o campo "Responsavel Pendencia" é preenchido automaticamente sem erros
- ✅ Confirmar que nenhum outro campo é afetado
- ✅ Validar tratamento de casos extremos
- ✅ Documentar qualquer comportamento inesperado

---

## 2. CASOS DE TESTE

### CASO DE TESTE 01: Demanda = "Alimentador"

**Pré-condição:**
- Ambiente de teste/staging disponível
- Lista com acesso de edição

**Passos:**
1. Criar novo item na lista
2. Preencher campo "Demanda" com: `Alimentador`
3. Preencher campos obrigatórios conforme necessário
4. Salvar item

**Resultado Esperado:**
- Campo "Responsavel Pendencia" é preenchido automaticamente com: `responsavel.a@suaempresa.com.br`
- Nenhum outro campo é alterado
- Histórico de alterações mostra a atualização

**Status**: ☐ Passou | ☐ Falhou | ☐ Não Testado

**Observações:**
```
[Espaço para notas do teste]
```

---

### CASO DE TESTE 02: Demanda = "Obras Reguladas"

**Pré-condição:**
- Ambiente de teste/staging disponível
- Lista com acesso de edição

**Passos:**
1. Criar novo item na lista
2. Preencher campo "Demanda" com: `Obras Reguladas`
3. Preencher campos obrigatórios conforme necessário
4. Salvar item

**Resultado Esperado:**
- Campo "Responsavel Pendencia" é preenchido automaticamente com: `responsavel.a@suaempresa.com.br`
- Nenhum outro campo é alterado
- Histórico de alterações mostra a atualização

**Status**: ☐ Passou | ☐ Falhou | ☐ Não Testado

**Observações:**
```
[Espaço para notas do teste]
```

---

### CASO DE TESTE 03: Demanda = Outro Valor

**Pré-condição:**
- Ambiente de teste/staging disponível
- Lista com acesso de edição

**Passos:**
1. Criar novo item na lista
2. Preencher campo "Demanda" com: `Manutenção Preventiva` (ou outro valor não listado)
3. Preencher campos obrigatórios conforme necessário
4. Salvar item

**Resultado Esperado:**
- Campo "Responsavel Pendencia" é preenchido automaticamente com: `responsavel.b@suaempresa.com.br`
- Nenhum outro campo é alterado
- Histórico de alterações mostra a atualização

**Status**: ☐ Passou | ☐ Falhou | ☐ Não Testado

**Observações:**
```
[Espaço para notas do teste]
```

---

### CASO DE TESTE 04: Demanda = Campo Vazio

**Pré-condição:**
- Ambiente de teste/staging disponível
- Lista com acesso de edição

**Passos:**
1. Criar novo item na lista
2. Deixar campo "Demanda" em branco
3. Preencher campos obrigatórios conforme necessário
4. Salvar item

**Resultado Esperado:**
- Campo "Responsavel Pendencia" NÃO é modificado
- Fluxo é executado mas nenhuma ação é tomada
- Nenhum erro é registrado

**Status**: ☐ Passou | ☐ Falhou | ☐ Não Testado

**Observações:**
```
[Espaço para notas do teste]
```

---

### CASO DE TESTE 05: Modificação de Item Existente

**Pré-condição:**
- Item existente com Demanda vazia
- Campo "Responsavel Pendencia" vazio ou com valor anterior

**Passos:**
1. Abrir item existente
2. Alterar campo "Demanda" de vazio para: `Alimentador`
3. Salvar alteração

**Resultado Esperado:**
- Campo "Responsavel Pendencia" é atualizado para: `responsavel.a@suaempresa.com.br`
- Histórico mostra a nova alteração

**Status**: ☐ Passou | ☐ Falhou | ☐ Não Testado

**Observações:**
```
[Espaço para notas do teste]
```

---

### CASO DE TESTE 06: Sensibilidade a Maiúsculas/Minúsculas

**Pré-condição:**
- Ambiente de teste/staging disponível

**Passos:**
1. Criar novo item
2. Preencher "Demanda" com: `alimentador` (minúsculo)
3. Salvar item

**Resultado Esperado:**
- Sistema reconhece corretamente (case-insensitive)
- Campo "Responsavel Pendencia" é preenchido com o responsável correto

**Status**: ☐ Passou | ☐ Falhou | ☐ Não Testado

**Observações:**
```
[Espaço para notas do teste]
```

---

### CASO DE TESTE 07: Valores com Espaços em Branco

**Pré-condição:**
- Ambiente de teste/staging disponível

**Passos:**
1. Criar novo item
2. Preencher "Demanda" com: ` Alimentador ` (com espaços antes/depois)
3. Salvar item

**Resultado Esperado:**
- Sistema reconhece corretamente (ignora espaços em branco)
- Campo "Responsavel Pendencia" é preenchido com o responsável correto

**Status**: ☐ Passou | ☐ Falhou | ☐ Não Testado

**Observações:**
```
[Espaço para notas do teste]
```

---

### CASO DE TESTE 08: Tempo de Execução

**Pré-condição:**
- Fluxo ativo
- Monitoramento habilitado

**Passos:**
1. Verificar tempo de execução no histórico de execuções
2. Confirmar que execução não demora mais de 30 segundos
3. Testar múltiplos itens simultaneamente

**Resultado Esperado:**
- Execução rápida (< 30 segundos)
- Sem timeout ou erros de performance
- Múltiplas execuções simultâneas não causam conflito

**Status**: ☐ Passou | ☐ Falhou | ☐ Não Testado

**Observações:**
```
[Espaço para notas do teste]
```

---

### CASO DE TESTE 09: Nenhum Outro Campo é Afetado

**Pré-condição:**
- Item com múltiplos campos preenchidos

**Passos:**
1. Criar item com vários campos preenchidos (título, descrição, etc)
2. Deixar "Demanda" vazio
3. Salvar item
4. Adicionar "Demanda" = "Alimentador"
5. Salvar alteração

**Resultado Esperado:**
- Apenas "Responsavel Pendencia" é alterado
- Todos os outros campos mantêm seus valores originais
- Nenhum campo é zerado ou alterado indesejadamente

**Status**: ☐ Passou | ☐ Falhou | ☐ Não Testado

**Observações:**
```
[Espaço para notas do teste]
```

---

### CASO DE TESTE 10: Permissões e Acesso

**Pré-condição:**
- Usuários com diferentes níveis de permissão

**Passos:**
1. Usuário com permissão de leitura cria/modifica item
2. Usuário com permissão de edição cria/modifica item
3. Usuário externo tenta criar item

**Resultado Esperado:**
- Automação funciona corretamente para usuários com permissão
- Erros apropriados para usuários sem permissão

**Status**: ☐ Passou | ☐ Falhou | ☐ Não Testado

**Observações:**
```
[Espaço para notas do teste]
```

---

## 3. MATRIZ DE TESTES

| ID | Caso de Teste | Valor Demanda | Responsável Esperado | Status |
|----|----|----|----|:-:|
| CT-01 | Alimentador | Alimentador | responsavel.a@... | ☐ |
| CT-02 | Obras Reguladas | Obras Reguladas | responsavel.a@... | ☐ |
| CT-03 | Outro Valor | Manutenção Preventiva | responsavel.b@... | ☐ |
| CT-04 | Vazio | (vazio) | Sem ação | ☐ |
| CT-05 | Modificação | Alimentador | responsavel.a@... | ☐ |
| CT-06 | Case-Insensitive | alimentador | responsavel.a@... | ☐ |
| CT-07 | Espaços | " Alimentador " | responsavel.a@... | ☐ |
| CT-08 | Performance | - | < 30 seg | ☐ |
| CT-09 | Outros Campos | Alimentador | Sem alteração | ☐ |
| CT-10 | Permissões | - | Conforme acesso | ☐ |

---

## 4. CRITÉRIOS DE ACEITAÇÃO

- [ ] Todos os 10 casos de teste devem passar
- [ ] Tempo de execução deve ser < 30 segundos
- [ ] Nenhum campo não intencional deve ser modificado
- [ ] Nenhum erro crítico durante a execução
- [ ] Histórico de alterações deve estar correto
- [ ] Responsáveis devem receber e-mails de notificação (se configurado)

---

## 5. ASSINATURA E APROVAÇÃO

**Testado por:** _____________________ **Data:** _______

**Aprovado por:** _____________________ **Data:** _______

**Observações Finais:**
```
[Espaço para conclusões dos testes]
```

---

## 6. PRÓXIMOS PASSOS

- [ ] Corrigir falhas (se houver)
- [ ] Re-testar casos que falharam
- [ ] Obter aprovação dos stakeholders
- [ ] Preparar documentação final
- [ ] Agendar go-live em produção
