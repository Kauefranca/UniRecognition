import psycopg2
from PIL import Image
from io import BytesIO
from os import listdir

con = psycopg2.connect(
	host='localhost', 
	database='postgres', 
	port='5432',
	user='postgres', 
	password='unimar'
)

cur = con.cursor()

def selectNameWithRA(ra):
    sql = """SELECT * FROM aluno WHERE ra=%s;"""
    try:
        cur.execute(sql, (ra,))
        return cur.fetchall()
    except Exception as e:
        print(f"Error: {e}")

def createUserAdmin():
    sql = """INSERT INTO usuario(login, hash) VALUES ('admin','pbkdf2:sha256:600000$JSADrlTwzvIXNZCu$93d4d3a797024b4bb22ec7169d1ffbed93674e42b9a2f58b6e06c16b27da425a');"""
    cur.execute(sql)
    con.commit()
     
def createProfessor(nome):
    sql = """INSERT INTO professor(nome) VALUES(%s);"""
    try:
        cur.execute(sql, (nome,))
        con.commit()
    except Exception as e:
        print(f"Error: {e}")
     
def createAula(nome, id_professor):
    sql = """INSERT INTO aula(nome, id_professor) VALUES(%s, %s);"""
    try:
        cur.execute(sql, (nome, id_professor))
        con.commit()
    except Exception as e:
        print(f"Error: {e}")

def insertImage(image_path, ra):
    # Abrir imagem como binário
    with open(image_path, 'rb') as file:
        image_binary = file.read()

    sql = """INSERT INTO imagem(imagem, id_aluno) VALUES (%s, (SELECT id_aluno FROM aluno WHERE ra = %s));"""
    try:
        cur.execute(sql, (image_binary, ra))
        con.commit()
        print("Image inserted successfully.")
    except Exception as e:
        print(f"Error: {e}")
        
def selectImage(ra):
    sql = """SELECT imagem FROM imagem WHERE id_aluno = (SELECT id_aluno FROM aluno WHERE ra = %s);"""
    try:
        cur.execute(sql, (ra,))
        result = cur.fetchone()

        if result:
            image_data = result[0]

            image = Image.open(BytesIO(image_data))

            image.show()

        else:
            print("Image not found for the given ra.")
    except Exception as e:
        print(f"Error: {e}")

def selectAllImages():
    sql = """SELECT * FROM imagem;"""
    try:
        cur.execute(sql)
        result = cur.fetchall()

        if result:
            return result

        else:
            print("Image not found for the given ra.")
    except Exception as e:
        print(f"Error: {e}")

def selectAllUsers(id_aula):
    sql = """SELECT * FROM aluno WHERE id_aula = (SELECT id_aula FROM aula WHERE id_aula = %s);"""
    try:
        cur.execute(sql, (id_aula, ))
        result = cur.fetchall()

        if result:
            return result

        else:
            print("Nothing to see here")
    except Exception as e:
        print(f"Error: {e}")


createUserAdmin()

createProfessor("Rafael Gutierres")

createAula('Fábrica de projeto ágeis', 1)
con.close()