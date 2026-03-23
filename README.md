# Automação Preenchimento

Fica rodando em loop e preenche automaticamente o campo de responsável em itens de uma lista do SharePoint, com base no tipo de demanda.

## Como funciona

A cada 60 segundos busca os itens da lista e aplica a regra:

- `Alimentador` ou `Obras Reguladas` → atribui Responsável A
- Qualquer outro valor → atribui Responsável B
- Campo vazio → ignora

Só atualiza se o valor realmente mudou, pra não fazer chamadas à toa.

## Configuração

**1. `config.json`** — URL do site e nome da lista:

```json
{
    "sharepoint_site_url": "https://suaempresa.sharepoint.com/sites/SeuSite",
    "sharepoint_list_title": "Nome da Lista"
}
```

**2. `automacao_sharepoint.py`** — ajuste os e-mails e as regras no dicionário `RESPONSAVEIS` conforme sua necessidade.

## Instalação

```bash
pip install -r requirements.txt
```

Ou use o `setup.bat` (Windows) / `setup.sh` (Linux/Mac) que instala tudo e já roda os testes.

## Rodando

```bash
python automacao_sharepoint.py
```

Na primeira vez abre o Edge pra login. Depois fecha e fica rodando em background. Para encerrar: `Ctrl+C`.

## Observações

- Cookies salvos em `.cookies.pkl` (não sobe pro git)
- Logs em `logs/`
- Tem uma versão alternativa via Power Automate documentada em `GUIA_IMPLEMENTACAO_POWER_AUTOMATE.md`, caso não queira depender de um servidor Python rodando
