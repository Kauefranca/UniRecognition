import psycopg2

con = psycopg2.connect(
  host='localhost', 
  database='postgres', 
  port='5432',
  user='postgres', 
  password='unimar')

cur = con.cursor()

sql = 'CREATE TABLE IF NOT EXISTS professor(id_professor SERIAL NOT NULL PRIMARY KEY, nome VARCHAR(60) NOT NULL);'
cur.execute(sql)
con.commit()

sql = "CREATE TABLE IF NOT EXISTS aula(id_aula SERIAL NOT NULL PRIMARY KEY, nome VARCHAR(60) NOT NULL, id_professor INT NOT NULL REFERENCES professor(id_professor));"
cur.execute(sql)
con.commit()

sql = "CREATE TABLE IF NOT EXISTS usuario(id_usuario SERIAL NOT NULL UNIQUE PRIMARY KEY, nome VARCHAR(60) NOT NULL,ra INT NOT NULL UNIQUE, id_aula INT NULL REFERENCES aula(id_aula));"
cur.execute(sql)
con.commit()

# sql = "CREATE TABLE IF NOT EXISTS imagem(id_imagem SERIAL NOT NULL PRIMARY KEY,nome VARCHAR(60) NOT NULL,imagem BYTEA NOT NULL,id_usuario INT REFERENCES usuario(id_usuario));"
sql = "CREATE TABLE IF NOT EXISTS imagem(imagem BYTEA NOT NULL, id_usuario INT REFERENCES usuario(id_usuario));"
cur.execute(sql)
con.commit()

sql = "CREATE TABLE IF NOT EXISTS registro(id_registro INT NOT NULL UNIQUE PRIMARY KEY, id_usuario INT NOT NULL REFERENCES usuario(id_usuario),id_aula INT NOT NULL REFERENCES aula(id_aula),	dthr TIMESTAMP NOT NULL);"
cur.execute(sql)
con.commit()

#recset = cur.fetchall()
#for rec in recset:
#  print (rec)

con.close()