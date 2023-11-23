import psycopg2

con = psycopg2.connect(
  host='localhost', 
  database='unirecog', 
  port='5432',
  user='postgres', 
  password='unimar')

cur = con.cursor()

ra = '1964011'

sql = f'SELECT * FROM usuario WHERE ra ={ra};'
cur.execute(sql)

recset = cur.fetchall()
for rec in recset:
    print(rec)