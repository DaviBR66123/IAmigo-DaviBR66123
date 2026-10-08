from sqlalchemy import select 
from config.database import SessionLocal 
from models.usuario import Usuario

class UsuarioRepository:
    
    def listar(self): 
        with SessionLocal() as session: 
            comando = select(Usuario).order_by(Usuario.nome)
            return list(session.scalars(comando)) 

    def buscar_por_nome(self, nome): 
        with SessionLocal() as session: 
            comando = select(Usuario).where(Usuario.nome == nome) 
            return session.scalar(comando)

    def buscar_por_id(self, id): 
        with SessionLocal() as session: 
            comando = select(Usuario).where(Usuario.id == id)
            return session.scalar(comando)
    
    def criar(self, nome, estilo_instrucao, gmail, senha): 
        with SessionLocal() as session: 
            usuario = Usuario( 
            nome=nome,  
            estilo_instrucao=estilo_instrucao,
            gmail=gmail,
            senha=senha
            )

        session.add(usuario) 
        session.commit() 
        session.refresh(usuario)

        return usuario

    def atualizar(self, id, nome, estilo_instrucao, gmail, senha):
        with SessionLocal() as session:
            usuario = session.scalar(
                select(Usuario).where(Usuario.id == id)
            )

            if usuario is None:
                return None

            usuario.nome = nome
            usuario.estilo_instrucao = estilo_instrucao
            usuario.gmail = gmail
            usuario.senha = senha

            session.commit()
            session.refresh(usuario)

            return usuario
    
    def excluir_por_nome(self, nome):
        with SessionLocal() as session: 
            usuario = session.scalar( 
            select(Usuario).where(Usuario.nome == nome) 
            )

        if usuario is None:

            return False
        
        session.delete(usuario) 
        session.commit() 

        return True

    def excluir_por_id(self, id):
        with SessionLocal() as session: 
            usuario = session.scalar( 
            select(Usuario).where(Usuario.id == id) 
            )
    
        if usuario is None:
    
            return False
            
        session.delete(usuario) 
        session.commit() 
    
        return True

    def buscar_por_gmail(self, gmail):
        with SessionLocal() as session:
            comando = select(Usuario).where(Usuario.gmail == gmail)
            return session.scalar(comando)

    def permissoes(self, id, role):
        with SessionLocal() as session:
            usuario = session.scalar(
                select(Usuario).where(Usuario.id == id)
            )

            usuario.role = role

            session.commit()
            session.refresh(usuario)

            return usuario