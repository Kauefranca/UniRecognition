import psycopg2
from PIL import Image
from io import BytesIO
from os import listdir

con = psycopg2.connect(
	host='localhost', 
	database='postgres', 
	port='5432',
	user='postgres', 
	password='unimar')

cur = con.cursor()

def selectNameWithRA(ra):
	sql = f'SELECT * FROM usuario WHERE ra={ra};'
	cur.execute(sql)

	recset = cur.fetchall()
	print(recset)
	# return recset[0][0]


def createUser(name, ra):
	sql = f"""INSERT INTO usuario(nome, ra) VALUES('{name}', {ra});"""
	cur.execute(sql)
	con.commit()


def insertImage(image_path, ra):
    # Read the image file as binary data
    with open(image_path, 'rb') as file:
        image_binary = file.read()

    # Insert the image binary data into the database
    sql = 'INSERT INTO imagem(imagem, id_usuario) VALUES (%s, (SELECT id_usuario FROM usuario WHERE ra = %s));'
    try:
        cur.execute(sql, (image_binary, ra))
        con.commit()
        print("Image inserted successfully.")
    except Exception as e:
        print(f"Error: {e}")
        
def selectImage(ra):
    # Execute a query to select the image data
    sql = 'SELECT imagem FROM imagem WHERE id_usuario = (SELECT id_usuario FROM usuario WHERE ra = %s);'
    try:
        cur.execute(sql, (ra,))
        result = cur.fetchone()

        if result:
            # Retrieve image data from the result
            image_data = result[0]

            # Create an image object from the binary data
            image = Image.open(BytesIO(image_data))

            # Display or process the image as needed
            image.show()

        else:
            print("Image not found for the given ra.")
    except Exception as e:
        print(f"Error: {e}")

selectImage(1959642)
     
# createUser("Eduardo Santos", 1959642)

# for path in listdir('./fotos/1959642/'):
# 	insertImage('./fotos/1959642/' + path, 1959642)
     
# selectNameWithRA('1959642')
con.close()

