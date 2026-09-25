import unittest
from unittest.mock import patch

from services.passo_service import PassoService


class PassoFake:
    def __init__(
        self,
        id,
        tarefa_id,
        texto,
        ordem,
        concluido=False
    ):
        self.id = id
        self.tarefa_id = tarefa_id
        self.texto = texto
        self.ordem = ordem
        self.concluido = concluido


class PassoRepositoryFake:
    def __init__(self):
        self.passos = {}
        self.proximo_id = 1

    def listar_por_tarefa(self, tarefa_id):
        return sorted(
            [
                passo
                for passo in self.passos.values()
                if passo.tarefa_id == tarefa_id
            ],
            key=lambda passo: passo.ordem
        )

    def criar_passo(self, tarefa_id, texto, ordem):
        passo = PassoFake(
            id=self.proximo_id,
            tarefa_id=tarefa_id,
            texto=texto,
            ordem=ordem
        )

        self.passos[self.proximo_id] = passo
        self.proximo_id += 1

        return passo

    def alternar_concluido(self, passo_id, modo="None"):
        passo = self.passos.get(passo_id)

        if passo is None:
            return None

        if modo.casefold() == "true":
            passo.concluido = True
        elif modo.casefold() == "false":
            passo.concluido = False
        else:
            passo.concluido = not passo.concluido

        return passo.concluido

    def excluir_por_id(self, id):
        if id not in self.passos:
            return False

        del self.passos[id]
        return True


class TestPassoService(unittest.TestCase):

    def setUp(self):
        self.repo = PassoRepositoryFake()
        self.service = PassoService(self.repo)

        # A listagem de passos exige que a tarefa exista.
        self.buscar_tarefa_mock = patch(
            "services.passo_service.tarefaservice.buscar_por_id",
            return_value={
                "id": 1,
                "titulo": "Tarefa de teste"
            }
        )

        self.buscar_tarefa_mock.start()
        self.addCleanup(self.buscar_tarefa_mock.stop)

    def adicionar_passo_inicial(self):
        return self.repo.criar_passo(
            tarefa_id=1,
            texto="Primeiro passo",
            ordem=1
        )

    def test_lista_passos_de_uma_tarefa(self):
        self.repo.criar_passo(
            tarefa_id=1,
            texto="Primeiro passo",
            ordem=1
        )

        self.repo.criar_passo(
            tarefa_id=1,
            texto="Segundo passo",
            ordem=2
        )

        passos = self.service.listar_por_tarefa(1)

        self.assertEqual(len(passos), 2)
        self.assertEqual(passos[0]["texto"], "Primeiro passo")
        self.assertEqual(passos[1]["texto"], "Segundo passo")
        self.assertEqual(passos[0]["ordem"], 1)
        self.assertEqual(passos[1]["ordem"], 2)

    def test_nao_aceita_id_da_tarefa_vazio(self):
        with self.assertRaisesRegex(ValueError, "não pode ser vazio"):
            self.service.listar_por_tarefa(None)

    def test_nao_aceita_id_da_tarefa_com_letras(self):
        with self.assertRaisesRegex(ValueError, "só pode conter números"):
            self.service.listar_por_tarefa("abc")

    def test_nao_aceita_id_da_tarefa_menor_ou_igual_a_zero(self):
        with self.assertRaisesRegex(ValueError, "maior que zero"):
            self.service.listar_por_tarefa(0)

    def test_informa_quando_tarefa_nao_possui_passos(self):
        with self.assertRaisesRegex(
            ValueError,
            "Tarefa ainda não possui passos"
        ):
            self.service.listar_por_tarefa(1)

    def test_cria_passo_valido(self):
        self.adicionar_passo_inicial()

        resultado = self.service.criar_passo(
            tarefa_id=1,
            texto="Segundo passo"
        )

        self.assertEqual(resultado["tarefa_id"], 1)
        self.assertEqual(resultado["texto"], "Segundo passo")
        self.assertEqual(resultado["ordem"], 2)

        passos = self.repo.listar_por_tarefa(1)

        self.assertEqual(len(passos), 2)
        self.assertEqual(passos[-1].texto, "Segundo passo")
        self.assertEqual(passos[-1].ordem, 2)

    def test_nao_cria_passo_com_texto_vazio(self):
        with self.assertRaisesRegex(
            ValueError,
            "Texto não pode ser vazio"
        ):
            self.service.criar_passo(1, "")

    def test_cria_passo_com_ordem_sequencial(self):
        self.repo.criar_passo(1, "Primeiro passo", 1)
        self.repo.criar_passo(1, "Segundo passo", 2)

        resultado = self.service.criar_passo(
            tarefa_id=1,
            texto="Terceiro passo"
        )

        self.assertEqual(resultado["ordem"], 3)

    def test_alterna_passo_para_concluido(self):
        passo = self.adicionar_passo_inicial()

        self.assertFalse(passo.concluido)

        self.service.alternar_concluido(
            id=passo.id,
            modo="true"
        )

        self.assertTrue(self.repo.passos[passo.id].concluido)

    def test_alterna_passo_para_nao_concluido(self):
        passo = self.adicionar_passo_inicial()
        passo.concluido = True

        self.service.alternar_concluido(
            id=passo.id,
            modo="false"
        )

        self.assertFalse(self.repo.passos[passo.id].concluido)

    def test_alterna_concluido_quando_modo_nao_e_informado(self):
        passo = self.adicionar_passo_inicial()

        self.service.alternar_concluido(passo.id)

        self.assertTrue(self.repo.passos[passo.id].concluido)

        self.service.alternar_concluido(passo.id)

        self.assertFalse(self.repo.passos[passo.id].concluido)

    def test_nao_aceita_modo_invalido(self):
        passo = self.adicionar_passo_inicial()

        with self.assertRaisesRegex(
            ValueError,
            "O modo deve ser True, False ou Vazio"
        ):
            self.service.alternar_concluido(
                passo.id,
                "qualquer"
            )

    def test_nao_alterna_passo_com_id_invalido(self):
        with self.assertRaisesRegex(
            ValueError,
            "só pode conter números"
        ):
            self.service.alternar_concluido("abc")

    def test_exclui_passo_por_id(self):
        passo = self.adicionar_passo_inicial()

        self.service.excluir_por_id(passo.id)

        self.assertNotIn(passo.id, self.repo.passos)

    def test_nao_exclui_passo_inexistente(self):
        with self.assertRaisesRegex(
            ValueError,
            "Passo não encontrado"
        ):
            self.service.excluir_por_id(999)

    def test_nao_exclui_passo_com_id_invalido(self):
        with self.assertRaisesRegex(
            ValueError,
            "só pode conter números"
        ):
            self.service.excluir_por_id("abc")


if __name__ == "__main__":
    unittest.main()