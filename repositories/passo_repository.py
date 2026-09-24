from sqlalchemy import select 
from config.database import SessionLocal 
from models.passo import Passo

class PassoRepository:

    def listar_por_tarefa(self, tarefa_id):
        with SessionLocal() as session:
            comando = select(Passo).where(Passo.tarefa_id == tarefa_id).order_by(Passo.ordem)
            return list(session.scalars(comando))

    def criar_passo(self, tarefa_id, texto, ordem):
        with SessionLocal() as session:
            passo = Passo(
                tarefa_id = tarefa_id,
                texto = texto,
                ordem = ordem
            )

            session.add(passo)
            session.commit()
            session.refresh(passo)

            return passo

    def alternar_concluido(self, passo_id, modo="None"):
        with SessionLocal() as session:
            passo = session.scalar(
                select(Passo).where(Passo.id == passo_id)
            )

            if passo is None:
                return None

            if modo.casefold() == "true":
                passo.concluido = True
                
                session.commit()
                session.refresh(passo)
                
                return passo.concluido

            elif modo.casefold() == "false":
                passo.concluido = False
                
                session.commit()
                session.refresh(passo)
                
                return passo.concluido

            else:
                passo.concluido = not passo.concluido

                session.commit()
                session.refresh(passo)

                return passo.concluido

    def excluir_por_id(self, id):
        with SessionLocal() as session: 
            passo = session.scalar( 
                select(Passo).where(Passo.id == id) 
            )
        
            if passo is None:
                return False
                
            session.delete(passo) 
            session.commit() 
        
            return True