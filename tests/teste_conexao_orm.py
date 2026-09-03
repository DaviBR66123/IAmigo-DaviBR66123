from sqlalchemy import text 
from config.database import engine 
with engine.connect() as conexao: 
 resultado = conexao.execute(text("SELECT 1")).scalar() 
 print("CONEXAO ORM OK:", resultado)
