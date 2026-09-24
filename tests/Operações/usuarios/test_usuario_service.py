import unittest
from datetime import datetime

from services.usuario_service import UsuarioService


class UsuarioFake:
    def __init__(self, id, nome, estilo_instrucao="direto"):
        self.id = id
        self.nome = nome
        self.estilo_instrucao = estilo_instrucao
        self.criado_em = datetime.now()


class UsuarioRepositoryFake:
    def __init__(self):
        self.usuarios = {}
        self.proximo_id = 1

    def listar(self):
        return list(self.usuarios.values())

    def buscar_por_nome(self, nome):
        return self.usuarios.get(nome)

    def buscar_por_id(self, id):
        return next(
            (
                usuario
                for usuario in self.usuarios.values()
                if usuario.id == id
            ),
            None,
        )

    def criar(self, nome, estilo_instrucao):
        usuario = UsuarioFake(
            self.proximo_id,
            nome,
            estilo_instrucao,
        )

        self.usuarios[nome] = usuario
        self.proximo_id += 1

        return usuario

    def excluir_por_id(self, id):
        usuario = self.buscar_por_id(id)

        if usuario is None:
            return False

        del self.usuarios[usuario.nome]
        return True


class TestUsuarioService(unittest.TestCase):
    def setUp(self):
        self.repo = UsuarioRepositoryFake()
        self.service = UsuarioService(self.repo)

    # Testes de criação

    def test_cria_usuario_valido(self):
        usuario = self.service.criar_usuario(
            "Anada",
            "direto",
        )

        self.assertEqual(usuario.nome, "Anada")
        self.assertEqual(usuario.estilo_instrucao, "direto")

    def test_remove_espacos_do_nome_antes_de_criar(self):
        usuario = self.service.criar_usuario(
            "  Anada  ",
            "direto",
        )

        self.assertEqual(usuario.nome, "Anada")

    def test_nao_aceita_nome_vazio(self):
        with self.assertRaisesRegex(ValueError, "nome não pode ficar vazio"):
            self.service.criar_usuario(
                " ",
                "direto",
            )

    def test_nao_aceita_usuario_duplicado(self):
        self.service.criar_usuario(
            "Leonardo",
            "direto",
        )

        with self.assertRaisesRegex(ValueError, "Já existe um perfil"):
            self.service.criar_usuario(
                "Leonardo",
                "direto",
            )

    def test_nao_aceita_estilo_invalido(self):
        with self.assertRaisesRegex(ValueError, "direto.*detalhado"):
            self.service.criar_usuario(
                "Bia",
                "gigante",
            )

    def test_nao_aceita_nome_muito_curto(self):
        with self.assertRaisesRegex(ValueError, "pelo menos 3 caracteres"):
            self.service.criar_usuario(
                "Al",
                "direto",
            )

    def test_rejeita_nome_com_menos_de_3_caracteres(self):
        with self.assertRaisesRegex(ValueError, "pelo menos 3 caracteres"):
            self.service.criar_usuario(
                "A",
                "direto",
            )

    def test_nao_aceita_nome_com_mais_de_100_caracteres(self):
        nome = "A" * 101

        with self.assertRaisesRegex(ValueError, "no máximo 100 caracteres"):
            self.service.criar_usuario(
                nome,
                "direto",
            )

    def test_aceita_nome_com_100_caracteres(self):
        nome = "A" * 100

        usuario = self.service.criar_usuario(
            nome,
            "direto",
        )

        self.assertEqual(usuario.nome, nome)

    def test_aceita_estilo_detalhado(self):
        usuario = self.service.criar_usuario(
            "Maria",
            "detalhado",
        )

        self.assertEqual(usuario.estilo_instrucao, "detalhado")

    # Testes de listagem

    def test_lista_usuarios(self):
        primeiro = self.service.criar_usuario(
            "Anada",
            "direto",
        )
        segundo = self.service.criar_usuario(
            "Bia",
            "detalhado",
        )

        resultado = self.service.listar_usuarios()

        self.assertEqual(len(resultado), 2)
        self.assertEqual(resultado[primeiro.id]["nome"], "Anada")
        self.assertEqual(resultado[segundo.id]["nome"], "Bia")
        self.assertEqual(resultado[primeiro.id]["estilo"], "direto")
        self.assertEqual(resultado[segundo.id]["estilo"], "detalhado")

    def test_lista_usuarios_sem_cadastro(self):
        resultado = self.service.listar_usuarios()

        self.assertEqual(resultado, {})

    def test_lancar_erro_quando_repositorio_nao_consegue_listar(self):
        self.repo.listar = lambda: None

        with self.assertRaisesRegex(ValueError, "Não foi possivel listar"):
            self.service.listar_usuarios()

    # Testes de busca por ID

    def test_busca_usuario_por_id(self):
        usuario = self.service.criar_usuario(
            "Anada",
            "direto",
        )

        resultado = self.service.buscar_por_id(usuario.id)

        self.assertEqual(resultado["id"], usuario.id)
        self.assertEqual(resultado["nome"], "Anada")
        self.assertEqual(resultado["estilo_instrucao"], "direto")
        self.assertEqual(resultado["criado_em"], usuario.criado_em)

    def test_busca_usuario_por_id_recebendo_string_numerica(self):
        usuario = self.service.criar_usuario(
            "Anada",
            "direto",
        )

        resultado = self.service.buscar_por_id(str(usuario.id))

        self.assertEqual(resultado["id"], usuario.id)

    def test_nao_aceita_id_vazio(self):
        with self.assertRaisesRegex(ValueError, "id não pode ser vazio"):
            self.service.buscar_por_id(None)

    def test_nao_aceita_id_com_letras(self):
        with self.assertRaisesRegex(ValueError, "id só pode conter números"):
            self.service.buscar_por_id("abc")

    def test_nao_aceita_id_zero(self):
        with self.assertRaisesRegex(ValueError, "id deve ser maior que zero"):
            self.service.buscar_por_id(0)

    def test_nao_aceita_id_negativo(self):
        with self.assertRaisesRegex(ValueError, "id só pode conter números"):
            self.service.buscar_por_id(-1)

    def test_erro_ao_buscar_usuario_inexistente(self):
        with self.assertRaisesRegex(ValueError, "Usuário não encontrado"):
            self.service.buscar_por_id(999)

    # Testes de exclusão

    def test_exclui_usuario_por_id(self):
        usuario = self.service.criar_usuario(
            "Anada",
            "direto",
        )

        resultado = self.service.excluir_por_id(usuario.id)

        self.assertTrue(resultado)
        self.assertIsNone(self.repo.buscar_por_id(usuario.id))

    def test_exclui_usuario_por_id_recebendo_string_numerica(self):
        usuario = self.service.criar_usuario(
            "Anada",
            "direto",
        )

        resultado = self.service.excluir_por_id(str(usuario.id))

        self.assertTrue(resultado)
        self.assertIsNone(self.repo.buscar_por_id(usuario.id))

    def test_nao_aceita_id_vazio_ao_excluir(self):
        with self.assertRaisesRegex(ValueError, "id não pode ser vazio"):
            self.service.excluir_por_id(None)

    def test_nao_aceita_id_com_letras_ao_excluir(self):
        with self.assertRaisesRegex(ValueError, "id só pode conter números"):
            self.service.excluir_por_id("abc")

    def test_nao_aceita_id_zero_ao_excluir(self):
        with self.assertRaisesRegex(ValueError, "id deve ser maior que zero"):
            self.service.excluir_por_id(0)

    def test_erro_ao_excluir_usuario_inexistente(self):
        with self.assertRaisesRegex(ValueError, "Usuario não encontrado"):
            self.service.excluir_por_id(999)


if __name__ == "__main__":
    unittest.main()