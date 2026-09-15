from sqlalchemy import select 
from config.database import SessionLocal 
from models.tarefa import Tarefa

class TarefaRepository:
    
    def listar_por_usuario(self, usuario_id): 
        with SessionLocal() as session: 
            comando = select(Tarefa).where(Tarefa.usuario_id == usuario_id).order_by(Tarefa.criado_em)
            return list(session.scalars(comando))
    
    def buscar_por_id(self, id): 
        with SessionLocal() as session: 
            comando = select(Tarefa).where(Tarefa.id == id)
            return session.scalar(comando)
        
    def criar_tarefa(self, usuario_id, tipo, titulo, descricao, prioridade, prazo=None): 
        with SessionLocal() as session: 
            tarefa = Tarefa( 
                usuario_id=usuario_id,
                tipo=tipo,
                titulo=titulo,
                descricao=descricao,
                prioridade=prioridade,
                prazo=prazo
            )
    
            session.add(tarefa) 
            session.commit() 
            session.refresh(tarefa)

            return tarefa
        
    def excluir_por_id(self, id):
        with SessionLocal() as session: 
            tarefa = session.scalar( 
                select(Tarefa).where(Tarefa.id == id) 
            )
        
            if tarefa is None:
                return False
                
            session.delete(tarefa) 
            session.commit() 
        
            return True