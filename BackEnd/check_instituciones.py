from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()
DB_URL = os.getenv('DATABASE_URL') or 'postgresql://postgres:Segundo_Francia_2025@localhost:5432/sgmi'
engine = create_engine(DB_URL)
conn = engine.connect()

result = conn.execute(text('SELECT id, descripcion FROM institucion'))
print('Instituciones en DB:')
for row in result:
    print(f'  ID={row[0]}: {row[1]}')

conn.close()
