import unittest
from services.usuario_service import UsuarioService


class UsuarioRepositoryFake:
    """Fake do UsuarioRepository para testes sem banco de dados"""
    
    def __init__(self):
        self.usuarios = {
            "1": {"id": "1", "nome": "João Silva", "estilo_instrucao": "direto"},
            "2": {"id": "2", "nome": "Maria Santos", "estilo_instrucao": "detalhado"},
        }
    
    def buscar_por_id(self, id):
        """Retorna o usuário se existir, None caso contrário"""
        return self.usuarios.get(id)


class TestUsuarioServiceBuscarPorId(unittest.TestCase):
    
    def setUp(self):
        """Configura o teste com um RepositoryFake"""
        self.repository_fake = UsuarioRepositoryFake()
        self.service = UsuarioService(repository=self.repository_fake)
    
    def test_buscar_por_id_com_id_valido(self):
        """Deve retornar o usuário quando o ID é válido e existe"""
        resultado = self.service.buscar_por_id("1")
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado["id"], "1")
        self.assertEqual(resultado["nome"], "João Silva")
    
    def test_buscar_por_id_com_id_nao_existente(self):
        """Deve lançar ValueError quando o usuário não existe"""
        with self.assertRaises(ValueError) as contexto:
            self.service.buscar_por_id("999")
        self.assertEqual(str(contexto.exception), "Usuário não encontrado")
    
    def test_buscar_por_id_com_id_vazio(self):
        """Deve lançar ValueError quando o ID é None"""
        with self.assertRaises(ValueError) as contexto:
            self.service.buscar_por_id(None)
        self.assertEqual(str(contexto.exception), "O id não pode ser vazio")
    
    def test_buscar_por_id_com_id_contendo_letras(self):
        """Deve lançar ValueError quando o ID contém caracteres não numéricos"""
        with self.assertRaises(ValueError) as contexto:
            self.service.buscar_por_id("1a")
        self.assertEqual(str(contexto.exception), "O id só pode conter números")
    
    def test_buscar_por_id_com_id_contendo_caracteres_especiais(self):
        """Deve lançar ValueError quando o ID contém caracteres especiais"""
        with self.assertRaises(ValueError) as contexto:
            self.service.buscar_por_id("1@2")
        self.assertEqual(str(contexto.exception), "O id só pode conter números")
    
    def test_buscar_por_id_com_id_contendo_espacos(self):
        """Deve lançar ValueError quando o ID contém espaços"""
        with self.assertRaises(ValueError) as contexto:
            self.service.buscar_por_id("1 2")
        self.assertEqual(str(contexto.exception), "O id só pode conter números")


if __name__ == "__main__":
    unittest.main()
