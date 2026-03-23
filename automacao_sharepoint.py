#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Atribui automaticamente o responsável no campo "Responsavel Pendencia" de cada item
# da lista SharePoint, com base no valor do campo "Demanda".
# Roda em loop a cada 60s. Autenticação via Selenium + cookies salvos.

import os
import sys
import json
import logging
import pickle
import requests
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse, quote
from apscheduler.schedulers.background import BackgroundScheduler

from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.support.ui import WebDriverWait

# Configuração de caminhos
BASE_PATH = Path(__file__).parent
CONFIG_PATH = BASE_PATH / "config.json"
COOKIES_PATH = BASE_PATH / ".cookies.pkl"
LOG_DIR = BASE_PATH / "logs"
LOG_DIR.mkdir(exist_ok=True)

# Configuração de logging
log_file = LOG_DIR / f"automacao_{datetime.now().strftime('%Y%m%d')}.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Mapeamento de responsáveis
RESPONSAVEIS = {
    'alimentador': 'responsavel.a@suaempresa.com.br',
    'obras reguladas': 'responsavel.a@suaempresa.com.br',
    'default': 'responsavel.b@suaempresa.com.br'
}

# Últimos IDs processados (para evitar duplicatas)
PROCESSED_ITEMS = set()


def load_config():
    """Carrega configurações de config.json"""
    if not CONFIG_PATH.exists():
        logger.error(f"Arquivo config.json não encontrado em {CONFIG_PATH}")
        sys.exit(1)
    with open(CONFIG_PATH, encoding='utf-8') as f:
        return json.load(f)


class AutomacaoSharePoint:

    def __init__(self, config):
        self.config = config
        self.site_url = config["sharepoint_site_url"]
        self.list_title = config["sharepoint_list_title"]
        self.session = None
        self.conectar()

    def conectar(self):
        """Conecta ao SharePoint usando cookies salvos ou login via navegador"""
        try:
            logger.info(f"Conectando ao SharePoint: {self.site_url}")
            self.session = self._get_sharepoint_session()
            logger.info("conectado")
        except Exception as e:
            logger.error(f"Erro ao conectar ao SharePoint: {str(e)}")
            raise

    def _get_sharepoint_session(self):
        """Retorna uma sessão requests autenticada no SharePoint"""
        session = requests.Session()
        session.headers.update({
            "Accept": "application/json;odata=verbose",
            "Content-Type": "application/json;odata=verbose",
        })

        parsed = urlparse(self.site_url)
        sp_host = parsed.hostname

        # Tentar reutilizar cookies salvos
        if COOKIES_PATH.exists():
            logger.info("Carregando cookies salvos...")
            with open(COOKIES_PATH, "rb") as f:
                selenium_cookies = pickle.load(f)

            cookies = self._cookies_to_session(selenium_cookies)
            for name, value in cookies.items():
                session.cookies.set(name, value)

            # Testar se cookies ainda são válidos
            test_url = f"{self.site_url}/_api/web/title"
            try:
                resp = session.get(test_url, timeout=15)
                if resp.status_code == 200:
                    logger.info("Cookies válidos. Sessão reutilizada.")
                    return session
                else:
                    logger.info(f"Cookies expirados (status {resp.status_code}). Novo login necessário.")
            except Exception as e:
                logger.info(f"Erro ao testar cookies: {e}. Novo login necessário.")

        # Login via navegador (primeira vez ou cookies expirados)
        cookies = self._login_via_browser()
        session.cookies.clear()
        for name, value in cookies.items():
            session.cookies.set(name, value)

        return session

    def _login_via_browser(self):
        """Abre Edge, usuario faz login manual, captura cookies"""
        logger.info("Abrindo navegador para login no SharePoint...")
        print("\n" + "=" * 60)
        print("LOGIN NECESSÁRIO")
        print("O navegador vai abrir. Faça login normalmente.")
        print("Após chegar na página do SharePoint, o script continua automaticamente.")
        print("=" * 60 + "\n")

        options = EdgeOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Edge(options=options)

        try:
            driver.get(self.site_url)

            # Espera até que a URL contenha o domínio do SharePoint (login concluído)
            parsed = urlparse(self.site_url)
            sp_host = parsed.hostname

            WebDriverWait(driver, 300).until(
                lambda d: sp_host in d.current_url and "login" not in d.current_url.lower()
            )
            logger.info(f"Login detectado. URL atual: {driver.current_url}")

            # Captura cookies
            selenium_cookies = driver.get_cookies()

            # Salva cookies para reuso
            with open(COOKIES_PATH, "wb") as f:
                pickle.dump(selenium_cookies, f)
            logger.info(f"Cookies salvos em {COOKIES_PATH}")

            return self._cookies_to_session(selenium_cookies)

        finally:
            driver.quit()

    @staticmethod
    def _cookies_to_session(selenium_cookies):
        """Converte cookies do Selenium para um dict {name: value}"""
        cookies = {}
        for c in selenium_cookies:
            cookies[c["name"]] = c["value"]
        return cookies

    def _list_api_url(self, suffix=""):
        """Monta URL da API do SharePoint com o nome da lista codificado"""
        encoded = quote(self.list_title)
        return f"{self.site_url}/_api/web/lists/getbytitle('{encoded}'){suffix}"

    def _get_request_digest(self):
        """Obtém o request digest necessário para operações de escrita"""
        try:
            url = f"{self.site_url}/_api/contextinfo"
            resp = self.session.post(url, timeout=15)
            resp.raise_for_status()
            data = resp.json()
            return data["d"]["GetContextWebInformation"]["FormDigestValue"]
        except Exception as e:
            logger.error(f"Erro ao obter request digest: {str(e)}")
            raise

    def _get_list_item_type(self):
        """Obtém o ListItemEntityTypeFullName necessário para criar/atualizar itens"""
        try:
            url = self._list_api_url("?$select=ListItemEntityTypeFullName")
            resp = self.session.get(url, timeout=15)
            resp.raise_for_status()
            return resp.json()["d"]["ListItemEntityTypeFullName"]
        except Exception as e:
            logger.error(f"Erro ao obter ListItemEntityTypeFullName: {str(e)}")
            raise

    def obter_itens(self):
        """Busca todos os itens da lista via SharePoint REST API"""
        try:
            logger.info(f"Buscando itens da lista '{self.list_title}'...")
            items = []

            url = self._list_api_url("/items?$top=5000")

            while url:
                resp = self.session.get(url, timeout=30)
                resp.raise_for_status()
                data = resp.json()

                for item in data["d"]["results"]:
                    # ResponsavelPendencia é MultiChoice: {"results": ["valor"]}
                    resp_raw = item.get("ResponsavelPendencia") or {}
                    resp_results = resp_raw.get("results", []) if isinstance(resp_raw, dict) else []
                    responsavel_atual = resp_results[0] if resp_results else ""

                    items.append({
                        "id": item["Id"],
                        "demanda": str(item.get("Demanda") or "").strip(),
                        "responsavel_pendencia": responsavel_atual,
                    })

                # Paginação
                url = data["d"].get("__next")

            logger.info(f"Itens encontrados: {len(items)}")
            return items

        except Exception as e:
            logger.error(f"Erro ao obter itens: {str(e)}")
            return []

    def processar_item(self, item):
        try:
            item_id = item["id"]

            if item_id in PROCESSED_ITEMS:
                return

            demanda = item.get("demanda", "").strip()
            if not demanda:
                return

            responsavel = self._obter_responsavel(demanda)
            responsavel_atual = item.get("responsavel_pendencia", "")

            if responsavel_atual == responsavel:
                PROCESSED_ITEMS.add(item_id)
                return

            self._atualizar_item(item_id, responsavel)
            PROCESSED_ITEMS.add(item_id)

            logger.info(f"Item {item_id}: Demanda='{demanda}' -> {responsavel}")

        except Exception as e:
            logger.error(f"Erro ao processar item {item.get('id')}: {str(e)}")

    def _obter_responsavel(self, demanda):
        demanda_lower = demanda.lower().strip()
        if demanda_lower in ['alimentador', 'obras reguladas']:
            return RESPONSAVEIS['alimentador']
        return RESPONSAVEIS['default']

    def _atualizar_item(self, item_id, responsavel):
        try:
            url = self._list_api_url(f"/items({item_id})")
            digest = self._get_request_digest()
            list_item_type = self._get_list_item_type()

            body = {
                "__metadata": {"type": list_item_type},
                "ResponsavelPendencia": {"results": [responsavel]}
            }

            headers = {
                "X-RequestDigest": digest,
                "IF-MATCH": "*",
                "X-HTTP-Method": "MERGE",
            }

            resp = self.session.post(url, json=body, headers=headers, timeout=15)
            resp.raise_for_status()

            logger.info(f"item {item_id} atualizado")

        except Exception as e:
            logger.error(f"Erro ao atualizar item {item_id}: {str(e)}")
            raise

    def processar_todos(self):
        try:
            logger.info(f"Iniciando processamento - {datetime.now()}")

            itens = self.obter_itens()

            if not itens:
                logger.info("Nenhum item encontrado para processar")
                return

            logger.info(f"Encontrados {len(itens)} item(ns)")

            for item in itens:
                self.processar_item(item)

            logger.info("processamento concluído")

        except Exception as e:
            logger.error(f"Erro crítico no processamento: {str(e)}")


def iniciar_automacao(intervalo_segundos=60):
    try:
        config = load_config()
        logger.info("Iniciando automação SharePoint")

        automacao = AutomacaoSharePoint(config)

        # Executar uma vez na inicialização
        automacao.processar_todos()

        # Agendar execução periódica
        scheduler = BackgroundScheduler()
        scheduler.add_job(
            automacao.processar_todos,
            'interval',
            seconds=intervalo_segundos,
            id='automacao_controle_notas',
            name='Automação SharePoint'
        )

        scheduler.start()
        logger.info(f"Automação agendada para executar a cada {intervalo_segundos} segundos")

        # Manter o script rodando
        try:
            while True:
                pass
        except KeyboardInterrupt:
            logger.info("Automação encerrada pelo usuário")
            scheduler.shutdown()

    except Exception as e:
        logger.error(f"Erro ao iniciar automação: {str(e)}")
        raise


if __name__ == '__main__':
    # Intervalo padrão: 60 segundos (1 minuto)
    # Ajuste conforme necessário
    iniciar_automacao(intervalo_segundos=60)
