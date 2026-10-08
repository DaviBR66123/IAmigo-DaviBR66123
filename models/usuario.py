from sqlalchemy import Boolean, Column, DateTime, Integer, String, Enum
from sqlalchemy.sql import func 
from config.database import Base

class Usuario(Base): 
   
   __tablename__ = "usuarios" 
   id = Column(Integer, primary_key=True) 
   nome = Column(String(100), nullable=False, unique=True) 
   estilo_instrucao = Column(String(20), nullable=False, default="direto")
   role = Column(String(5), nullable=False, default="user")
   gmail = Column(String(250), nullable=False)
   senha = Column(String(64), nullable=False)
   criado_em = Column(DateTime, server_default=func.now())

   def __repr__(self): 
         return ( 
      f"Usuario(id={self.id}, " 
      f"nome='{self.nome}', " 
      f"estilo='{self.estilo_instrucao}')" 
      )
