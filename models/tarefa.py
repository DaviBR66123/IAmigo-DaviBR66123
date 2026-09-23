from sqlalchemy import Boolean, Column, DateTime, Integer, String, Enum, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.database import Base

class Tarefa(Base):

    __tablename__ = "tarefas"
    
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, nullable=False)
    tipo = Column(Enum('tarefas_diarias', 'tarefas_educacionais'), nullable=False)
    titulo = Column(String(200), nullable=False)
    descricao = Column(String(500), nullable=True)
    prioridade = Column(Enum('baixa', 'media', 'alta'), nullable=False, default='media')
    prazo = Column(Date, nullable=True)
    concluida = Column(Boolean, nullable=False, default=False)
    criado_em = Column(DateTime, default=func.now())

    passos = relationship(
        "Passo",
        back_populates="tarefa",
        cascade="all, delete-orphan"
    )