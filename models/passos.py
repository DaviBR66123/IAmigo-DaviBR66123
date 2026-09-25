from sqlalchemy import Boolean, Column, Integer, Text, text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.database import Base

class Passo(Base):

    __tablename__ = "passos"
    
    id = Column(Integer, primary_key=True)
    tarefa_id = Column(Integer, ForeignKey("tarefas.id", ondelete="CASCADE"), nullable=False)
    texto = Column(Text, nullable=False)
    concluido = Column(Boolean, nullable=False, server_default=text("0"))
    ordem = Column(Integer, nullable=False, server_default=text("1"))

    tarefa = relationship(
        "Tarefa",
        back_populates="passos"
    )

    #python -m unicorvi.api_app:app --reload