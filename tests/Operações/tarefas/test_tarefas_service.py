import unittest
from datetime import date
from types import SimpleNamespace
from unittest.mock import Mock, patch

from services.tarefa_service import TarefaService


class TarefaFake:
    def __init__(
        self,
        id=1,
        usuario_id=1,
        tipo="tarefas_diarias",
        titulo="Estudar Python",
        descricao="Estudar por uma hora",
        prioridade="media",
        prazo=date(2026, 10, 15),
        concluida=False,
    ):
        self.id = id
        self.usuario_id = usuario_id
        self.tipo = tipo
        self.titulo = titulo
        self.descricao = descricao
        self.prioridade = prioridade
        self.prazo = prazo
        self.concluida = concluida


class TarefaRepositoryFake:
    def __init__(self):
        self.tarefas = {}
        self.proximo_id = 1

    def listar_por_usuario(self, usuario_id):
        return [
            tarefa
            for tarefa in self.tarefas.values()
            if tarefa.usuario_id == usuario_id
        ]

    def buscar_por_id(self, tarefa_id):
        return self.tarefas.get(tarefa_id)

    def criar_tarefa(
        self,
        usuario_id,
        tipo,
        titulo,
        descricao,
        prioridade,
        prazo=None,
    ):
        tarefa = TarefaFake(
            id=self.proximo_id,
            usuario_id=usuario_id,
            tipo=tipo,
            titulo=titulo,
            descricao=descricao,
            prioridade=prioridade,
            prazo=prazo,
        )

        self.tarefas[self.proximo_id] = tarefa
        self.proximo_id += 1

        return tarefa

    def alternar_concluido(self, tarefa_id, modo="None"):
        tarefa = self.tarefas.get(tarefa_id)

        if tarefa is None:
            return None

        if modo.casefold() == "true":
            tarefa.concluida = True
        elif modo.casefold() == "false":
            tarefa.concluida = False
        else:
            tarefa.concluida = not tarefa.concluida

        return tarefa.concluida

    def excluir_por_id(self, tarefa_id):
        if tarefa_id not in self.tarefas:
            return False

        del self.tarefas[tarefa_id]
        return True


class TestTarefaService(unittest.TestCase):
    def setUp(self):
        self.repo = TarefaRepositoryFake()
        self.service = TarefaService(self.repo)

    def criar_tarefa_valida(self):
        return self.repo.criar_tarefa(
            usuario_id=1,
            tipo="tarefas_diarias",
            titulo="Estudar Python",
            descricao="Estudar por uma hora",
            prioridade="media",
            prazo=date(2026, 10, 15),
        )

    # ------------------------------------------------------------------
    # Testes de criação
    # ------------------------------------------------------------------

    def test_cria_tarefa_valida(self):
        tarefa = self.service.criar_tarefa(
            usuario_id=1,
            tipo="tarefas_diarias",
            titulo="Estudar Python",
            descricao="Estudar por uma hora",
            prioridade="media",
            prazo="15/10/2026",
        )

        self.assertEqual(tarefa.usuario_id, 1)
        self.assertEqual(tarefa.titulo, "Estudar Python")
        self.assertEqual(tarefa.prazo, date(2026, 10, 15))

    def test_cria_tarefa_sem_prazo(self):
        tarefa = self.service.criar_tarefa(
            usuario_id=1,
            tipo="tarefas_diarias",
            titulo="Ler um livro",
            descricao="Ler 20 páginas",
            prioridade="baixa",
        )

        self.assertIsNone(tarefa.prazo)

    def test_nao_aceita_usuario_id_vazio(self):
        with self.assertRaisesRegex(ValueError, "não pode ser vazio"):
            self.service.criar_tarefa(
                usuario_id=None,
                tipo="tarefas_diarias",
                titulo="Estudar",
                descricao="Descrição",
                prioridade="media",
            )

    def test_nao_aceita_usuario_id_com_letras(self):
        with self.assertRaisesRegex(ValueError, "só pode conter números"):
            self.service.criar_tarefa(
                usuario_id="abc",
                tipo="tarefas_diarias",
                titulo="Estudar",
                descricao="Descrição",
                prioridade="media",
            )

    def test_nao_aceita_usuario_id_menor_ou_igual_a_zero(self):
        for usuario_id in [0, -1]:
            with self.subTest(usuario_id=usuario_id):
                with self.assertRaisesRegex(
                    ValueError,
                    "maior que zero",
                ):
                    self.service.criar_tarefa(
                        usuario_id=usuario_id,
                        tipo="tarefas_diarias",
                        titulo="Estudar",
                        descricao="Descrição",
                        prioridade="media",
                    )

    def test_nao_aceita_tipo_vazio(self):
        with self.assertRaisesRegex(ValueError, "Tipo não pode ficar vazio"):
            self.service.criar_tarefa(
                usuario_id=1,
                tipo="",
                titulo="Estudar",
                descricao="Descrição",
                prioridade="media",
            )

    def test_nao_aceita_tipo_invalido(self):
        with self.assertRaisesRegex(
            ValueError,
            "tarefas_diarias ou tarefas_educacionais",
        ):
            self.service.criar_tarefa(
                usuario_id=1,
                tipo="tipo_invalido",
                titulo="Estudar",
                descricao="Descrição",
                prioridade="media",
            )

    def test_nao_aceita_titulo_vazio(self):
        with self.assertRaisesRegex(ValueError, "titulo não pode ficar vazio"):
            self.service.criar_tarefa(
                usuario_id=1,
                tipo="tarefas_diarias",
                titulo="",
                descricao="Descrição",
                prioridade="media",
            )

    def test_nao_aceita_titulo_com_mais_de_200_caracteres(self):
        with self.assertRaisesRegex(
            ValueError,
            "no máximo 200 caracteres",
        ):
            self.service.criar_tarefa(
                usuario_id=1,
                tipo="tarefas_diarias",
                titulo="A" * 201,
                descricao="Descrição",
                prioridade="media",
            )

    def test_nao_aceita_prioridade_vazia(self):
        with self.assertRaisesRegex(
            ValueError,
            "Prioridade não pode ficar vazia",
        ):
            self.service.criar_tarefa(
                usuario_id=1,
                tipo="tarefas_diarias",
                titulo="Estudar",
                descricao="Descrição",
                prioridade="",
            )

    def test_nao_aceita_prioridade_invalida(self):
        with self.assertRaisesRegex(
            ValueError,
            "prioridade deve ser baixa",
        ):
            self.service.criar_tarefa(
                usuario_id=1,
                tipo="tarefas_diarias",
                titulo="Estudar",
                descricao="Descrição",
                prioridade="urgente",
            )

    def test_nao_aceita_prazo_com_formato_invalido(self):
        with self.assertRaisesRegex(ValueError, "formato da data é inválido"):
            self.service.criar_tarefa(
                usuario_id=1,
                tipo="tarefas_diarias",
                titulo="Estudar",
                descricao="Descrição",
                prioridade="media",
                prazo="2026-10-15",
            )

    # ------------------------------------------------------------------
    # Testes de busca
    # ------------------------------------------------------------------

    def test_busca_tarefa_por_id(self):
        self.criar_tarefa_valida()

        resultado = self.service.buscar_por_id(1)

        self.assertEqual(resultado["usuario_id"], 1)
        self.assertEqual(resultado["tipo"], "tarefas_diarias")
        self.assertEqual(resultado["titulo"], "Estudar Python")
        self.assertEqual(resultado["prioridade"], "media")

    def test_nao_encontra_tarefa_por_id(self):
        with self.assertRaisesRegex(ValueError, "Tarefa não encontrada"):
            self.service.buscar_por_id(999)

    def test_nao_aceita_id_vazio_na_busca(self):
        with self.assertRaisesRegex(ValueError, "não pode ser vazio"):
            self.service.buscar_por_id(None)

    def test_nao_aceita_id_com_letras_na_busca(self):
        with self.assertRaisesRegex(ValueError, "só pode conter números"):
            self.service.buscar_por_id("abc")

    # ------------------------------------------------------------------
    # Testes de listagem
    # ------------------------------------------------------------------

    @patch("services.tarefa_service.usuarioservice")
    def test_lista_tarefas_por_usuario(self, usuario_service_mock):
        usuario_service_mock.buscar_por_id.return_value = SimpleNamespace(
            id=1,
            nome="Ana",
        )

        self.criar_tarefa_valida()

        resultado = self.service.listar_por_usuario(1)

        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0]["id"], 1)
        self.assertEqual(resultado[0]["usuario_id"], 1)
        self.assertEqual(resultado[0]["titulo"], "Estudar Python")
        self.assertEqual(resultado[0]["prazo"], "15/10/2026")

    @patch("services.tarefa_service.usuarioservice")
    def test_nao_lista_quando_usuario_nao_tem_tarefas(
        self,
        usuario_service_mock,
    ):
        usuario_service_mock.buscar_por_id.return_value = SimpleNamespace(
            id=1,
            nome="Ana",
        )

        with self.assertRaisesRegex(
            ValueError,
            "Usuário ainda não possui tarefas",
        ):
            self.service.listar_por_usuario(1)

    # ------------------------------------------------------------------
    # Testes de conclusão
    # ------------------------------------------------------------------

    def test_alterna_tarefa_para_concluida(self):
        self.criar_tarefa_valida()

        self.service.alternar_concluido(1, "true")

        tarefa = self.repo.buscar_por_id(1)
        self.assertTrue(tarefa.concluida)

    def test_alterna_tarefa_para_nao_concluida(self):
        tarefa = self.criar_tarefa_valida()
        tarefa.concluida = True

        self.service.alternar_concluido(1, "false")

        self.assertFalse(tarefa.concluida)

    def test_nao_aceita_modo_invalido(self):
        with self.assertRaisesRegex(
            ValueError,
            "modo deve ser True, False ou Vazio",
        ):
            self.service.alternar_concluido(1, "qualquer")

    # ------------------------------------------------------------------
    # Testes de exclusão
    # ------------------------------------------------------------------

    def test_exclui_tarefa_por_id(self):
        self.criar_tarefa_valida()

        resultado = self.service.excluir_por_id(1)

        self.assertTrue(resultado)
        self.assertIsNone(self.repo.buscar_por_id(1))

    def test_nao_exclui_tarefa_inexistente(self):
        with self.assertRaisesRegex(ValueError, "Tarefa não encontrada"):
            self.service.excluir_por_id(999)

    def test_nao_aceita_id_vazio_na_exclusao(self):
        with self.assertRaisesRegex(ValueError, "não pode ser vazio"):
            self.service.excluir_por_id(None)


if __name__ == "__main__":
    unittest.main()