#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from unittest.mock import Mock, patch, MagicMock
from automacao_sharepoint import AutomacaoSharePoint, RESPONSAVEIS


class TestAtribuicaoResponsaveis(unittest.TestCase):

    def setUp(self):
        with patch('automacao_sharepoint.ClientContext'):
            with patch('automacao_sharepoint.AuthenticationContext'):
                self.automacao = AutomacaoSharePoint()

    def test_responsavel_alimentador(self):
        resultado = self.automacao._obter_responsavel('Alimentador')
        self.assertEqual(resultado, 'responsavel.a@suaempresa.com.br')

    def test_responsavel_alimentador_minusculo(self):
        resultado = self.automacao._obter_responsavel('alimentador')
        self.assertEqual(resultado, RESPONSAVEIS['alimentador'])

    def test_responsavel_obras_reguladas(self):
        resultado = self.automacao._obter_responsavel('Obras Reguladas')
        self.assertEqual(resultado, 'responsavel.a@suaempresa.com.br')

    def test_responsavel_obras_reguladas_minusculo(self):
        resultado = self.automacao._obter_responsavel('obras reguladas')
        self.assertEqual(resultado, 'responsavel.a@suaempresa.com.br')

    def test_responsavel_outro_valor(self):
        resultado = self.automacao._obter_responsavel('Manutenção Preventiva')
        self.assertEqual(resultado, 'responsavel.b@suaempresa.com.br')

    def test_responsavel_outro_valor_minusculo(self):
        resultado = self.automacao._obter_responsavel('outro tipo de demanda')
        self.assertEqual(resultado, 'responsavel.b@suaempresa.com.br')

    def test_responsavel_com_espacos(self):
        resultado = self.automacao._obter_responsavel('  Alimentador  ')
        self.assertEqual(resultado, 'responsavel.a@suaempresa.com.br')

    def test_responsavel_vazio(self):
        resultado = self.automacao._obter_responsavel('')
        self.assertEqual(resultado, 'responsavel.b@suaempresa.com.br')


class TestProcessamentoItems(unittest.TestCase):

    def setUp(self):
        with patch('automacao_sharepoint.ClientContext'):
            with patch('automacao_sharepoint.AuthenticationContext'):
                self.automacao = AutomacaoSharePoint()

    def test_processar_item_com_demanda_valida(self):
        item_mock = Mock()
        item_mock.properties = {
            'ID': 1,
            'Demanda': 'Alimentador',
            'Responsavel Pendencia': ''
        }

        with patch.object(self.automacao, '_atualizar_item') as mock_update:
            self.automacao.processar_item(item_mock)
            mock_update.assert_called_once()
            _, email = mock_update.call_args[0]
            self.assertEqual(email, 'responsavel.a@suaempresa.com.br')

    def test_processar_item_demanda_vazia(self):
        item_mock = Mock()
        item_mock.properties = {
            'ID': 2,
            'Demanda': '',
            'Responsavel Pendencia': ''
        }

        with patch.object(self.automacao, '_atualizar_item') as mock_update:
            self.automacao.processar_item(item_mock)
            mock_update.assert_not_called()

    def test_processar_item_ja_atribuido(self):
        item_mock = Mock()
        item_mock.properties = {
            'ID': 3,
            'Demanda': 'Alimentador',
            'Responsavel Pendencia': 'responsavel.a@suaempresa.com.br'
        }

        with patch.object(self.automacao, '_atualizar_item') as mock_update:
            self.automacao.processar_item(item_mock)
            mock_update.assert_not_called()

    def test_evitar_reprocessamento(self):
        item_mock = Mock()
        item_mock.properties = {
            'ID': 4,
            'Demanda': 'Alimentador',
            'Responsavel Pendencia': ''
        }

        with patch.object(self.automacao, '_atualizar_item'):
            self.automacao.processar_item(item_mock)

        with patch.object(self.automacao, '_atualizar_item') as mock_update:
            self.automacao.processar_item(item_mock)
            mock_update.assert_not_called()


class TestIntegracaoCompleta(unittest.TestCase):

    def setUp(self):
        with patch('automacao_sharepoint.ClientContext'):
            with patch('automacao_sharepoint.AuthenticationContext'):
                self.automacao = AutomacaoSharePoint()

    def test_fluxo_completo_alimentador(self):
        item_mock = Mock()
        item_mock.properties = {
            'ID': 5,
            'Demanda': 'Alimentador',
            'Responsavel Pendencia': ''
        }

        responsavel = self.automacao._obter_responsavel(item_mock.properties['Demanda'])
        self.assertEqual(responsavel, 'responsavel.a@suaempresa.com.br')

    def test_fluxo_completo_outro_tipo(self):
        item_mock = Mock()
        item_mock.properties = {
            'ID': 6,
            'Demanda': 'Inspeção',
            'Responsavel Pendencia': ''
        }

        responsavel = self.automacao._obter_responsavel(item_mock.properties['Demanda'])
        self.assertEqual(responsavel, 'responsavel.b@suaempresa.com.br')

    def test_responsaveis_configurados(self):
        self.assertIn('alimentador', [k.lower() for k in RESPONSAVEIS.keys()])
        self.assertIn('default', RESPONSAVEIS)
        self.assertEqual(RESPONSAVEIS['default'], 'responsavel.b@suaempresa.com.br')


class TestCasosEdge(unittest.TestCase):

    def setUp(self):
        with patch('automacao_sharepoint.ClientContext'):
            with patch('automacao_sharepoint.AuthenticationContext'):
                self.automacao = AutomacaoSharePoint()

    def test_case_insensitive_obras_reguladas(self):
        for valor in ['OBRAS REGULADAS', 'obras reguladas', 'Obras REGULADAS']:
            resultado = self.automacao._obter_responsavel(valor)
            self.assertEqual(resultado, 'responsavel.a@suaempresa.com.br', f"Falhou para: {valor}")

    def test_espacos_em_branco_multiplos(self):
        resultado = self.automacao._obter_responsavel('   Alimentador   ')
        self.assertEqual(resultado, 'responsavel.a@suaempresa.com.br')

    def test_valor_none(self):
        try:
            resultado = self.automacao._obter_responsavel(None or '')
            self.assertIsNotNone(resultado)
        except Exception as e:
            self.fail(f"erro ao processar None: {e}")

    def test_caracteres_especiais(self):
        resultado = self.automacao._obter_responsavel('Manutenção @#$')
        self.assertEqual(resultado, 'responsavel.b@suaempresa.com.br')


def executar_testes_com_relatorio():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(TestAtribuicaoResponsaveis))
    suite.addTests(loader.loadTestsFromTestCase(TestProcessamentoItems))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegracaoCompleta))
    suite.addTests(loader.loadTestsFromTestCase(TestCasosEdge))

    runner = unittest.TextTestRunner(verbosity=2)
    resultado = runner.run(suite)
    return resultado.wasSuccessful()


if __name__ == '__main__':
    sucesso = executar_testes_com_relatorio()
    exit(0 if sucesso else 1)
