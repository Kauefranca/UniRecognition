import psycopg2

con = psycopg2.connect(
  host='localhost', 
  database='unirecog', 
  port='5432',
  user='postgres', 
  password='unimar')

cur = con.cursor()

def selectNameWithRA(ra):
    sql = f'SELECT nome FROM usuario WHERE ra={ra};'
    cur.execute(sql)

    recset = cur.fetchall()

    con.close()
    return recset[0][0]

nome = selectNameWithRA('1964011')
print(nome)