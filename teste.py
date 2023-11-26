import psycopg2
from PIL import Image
from io import BytesIO

con = psycopg2.connect(
	host='localhost', 
	database='postgres', 
	port='5432',
	user='postgres', 
	password='unimar'
)

cur = con.cursor()
sql = """SELECT imagem FROM imagem WHERE id_aluno = (SELECT id_aluno FROM aluno WHERE ra = '1964011');"""
cur.execute(sql)
result = cur.fetchall()

print(result)