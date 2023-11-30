import shutil
import psycopg2
import json
from flask import Flask, Response
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from flask_socketio import SocketIO
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from os import mkdir, listdir, path
from utils.Helpers import apology, login_required
from datetime import datetime as dt

from utils.Reconhecimento import ReconhecimentoFacial
from utils.Treinamento import TreinadorReconhecimentoFacial
from utils.CameraFeed import CameraFeed
from utils.Captura import CapturaFaces

ID_AULA = 1

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
socketio = SocketIO(app)

classifier_file = 'src\\frontalFaceHaarcascade.xml'
recognizer_file = 'src\\classificadores\\BCCA.yml'
cascade_file = "src\\frontalFaceHaarcascade.xml"  # Arquivo do classificador Haar

shutil.rmtree(path.join('Fotos'), ignore_errors=True)
mkdir(path.join('Fotos'))

camera = CameraFeed()
treinador = TreinadorReconhecimentoFacial()
captura = CapturaFaces(cascade_file)

reconhecimento = ReconhecimentoFacial(classifier_file, recognizer_file)
reconhecimento.setStatus(None)

  # Instância da classe CapturaFaces

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

con = psycopg2.connect(
	host='localhost', 
	database='postgres', 
	port='5432',
	user='postgres', 
	password='unimar'
)

cursor = con.cursor()
sql = """SELECT * FROM aluno WHERE id_aula = (SELECT id_aula FROM aula WHERE id_aula = %s);"""
cursor.execute(sql, (ID_AULA,))
rows = cursor.fetchall()

alunos = {}

for row in rows:
    alunos[row[2]] = row[1]

reconhecimento.setAlunos(alunos)

@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route('/rec')
def rec():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame ')

@app.route('/cap')
def cap():
    return Response(gen_cap(), mimetype='multipart/x-mixed-replace; boundary=frame ')

@app.route("/reconhecer", methods=["GET"])
# @login_required
def reconhecer():
    cursor = con.cursor()
    sql = """SELECT * FROM aluno WHERE id_aula = (SELECT id_aula FROM aula WHERE id_aula = %s) ORDER BY nome;"""
    cursor.execute(sql, (ID_AULA,))
    data = cursor.fetchall()

    return render_template('reconhecer.html', data=data)

@app.route("/registrar", methods=["GET", "POST"])
@login_required
def registrar():
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("nome"):
            return apology("Campo 'Nome' obrigatório!", 400)

        # Ensure password was submitted
        elif not request.form.get("ra"):
            return apology("Campo 'RA' obrigatório!", 400)
    
        elif not request.form.get("id_aula"):
            return apology("Campo 'id_aula' obrigatório!", 400)
        
        cursor = con.cursor()
        sql = """SELECT * FROM aluno WHERE ra = %s"""
        cursor.execute(sql, (request.form.get("ra"),))
        rows = cursor.fetchone()

        if rows:
            return apology("Já existe alguém com esse RA cadastrado!", 400)
        
        cursor = con.cursor()
        sql = """INSERT INTO aluno(nome, ra, id_aula) VALUES (%s, %s, %s)"""
        cursor.execute(sql, (request.form.get("nome"), request.form.get("ra"), request.form.get("id_aula")))
        con.commit()

        captura.iniciarCaptura(request.form.get("ra"))

        # Redirect user to home page
        return redirect("/registrar")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        cursor = con.cursor()
        sql = """SELECT nome, id_aula FROM aula ORDER BY nome;"""
        cursor.execute(sql, (ID_AULA,))
        data = cursor.fetchall()

        return render_template('registrar.html', data=data)

@app.route("/treinar", methods=["GET", "POST"])
@login_required
def treinar():
    if request.method == 'POST':
        treinador.treinar('src\\classificadores\\BCCA.yml', ID_AULA)
        return redirect('/treinar')
    else:
        cursor = con.cursor()
        sql = """SELECT nome, id_aula FROM aula ORDER BY nome;"""
        cursor.execute(sql)
        data = cursor.fetchall()

        return render_template('treinar.html', data=data)

@app.route("/relatorio", methods=["GET", "POST"])
# @login_required
def relatorio():
    if request.method == 'POST':
        if not request.form.get("tipo_relatorio"):
            return apology("Campo 'tipo_relatorio' obrigatório!", 400)
        
        if request.form.get("tipo_relatorio") == "listagem":
            cursor = con.cursor()
            sql = """SELECT nome, ra, id_aula FROM aluno ORDER BY nome"""
            cursor.execute(sql)
            rows = cursor.fetchall()
            sql = """SELECT id_aula, nome FROM aula"""
            cursor.execute(sql)
            ids = dict(cursor.fetchall())

            return render_template("visualize.html", rows=rows, ids=ids, type="listagem")
        
        elif request.form.get("tipo_relatorio") == "presenca":
            cursor = con.cursor()
            sql = """SELECT id_aluno, entrada, saida FROM registro;"""
            cursor.execute(sql)
            rows = cursor.fetchall()

            return render_template("visualize.html", rows=rows, type="presenca")
    else:
        return render_template('relatorio.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        cursor = con.cursor()
        sql = """SELECT * FROM usuario WHERE login = %s;"""
        cursor.execute(sql, (request.form.get("username"),))
        rows = cursor.fetchall()

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0][2], request.form.get("password")):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0][0]
        session['alert'] = 'Login sucessful!'
        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/incluir_fotos", methods=["POST"])
def incluir():
    if request.method == "POST":
        ra = request.form.get("ra")
        if not ra:
            return apology("Campo 'ra' obrigatório!", 400)
            
        for item in listdir(path.join('fotos', ra)):
            with open(path.join('fotos', ra, item), 'rb') as file:
                image_binary = file.read()

            sql = """INSERT INTO imagem(imagem, id_aluno) VALUES (%s, (SELECT id_aluno FROM aluno WHERE ra = %s));"""
            cursor.execute(sql, (image_binary, ra))
            con.commit()

        shutil.rmtree(path.join('fotos', ra), ignore_errors=True)
        return redirect("/cadastrar")
    else:
        return apology('Method not allowed', 400)
    
@app.route("/start_aula", methods=["POST"])
def start_aula():
    if request.method == "POST":
        reconhecimento.setStatus('entrada')
        cursor = con.cursor()
        sql = """SELECT * FROM aluno WHERE id_aula = %s ORDER BY nome;"""
        cursor.execute(sql, (ID_AULA,))
        rows = cursor.fetchall()
        for row in rows:
            cursor = con.cursor()
            sql = """INSERT INTO registro(id_aluno, id_aula, start_date) VALUES (%s, %s, %s);"""
            cursor.execute(sql, (row[0], ID_AULA, dt.now()))
            con.commit()
        return Response('Ok', status=200)
    else:
        return apology('Method not allowed', 400)

@app.route("/end_aula", methods=["POST"])
def end_aula():
    if request.method == "POST":
        reconhecimento.setStatus('saida')
        cursor = con.cursor()
        sql = """SELECT * FROM aluno WHERE id_aula = %s ORDER BY nome;"""
        cursor.execute(sql, (ID_AULA,))
        rows = cursor.fetchall()
        for row in rows:
            cursor = con.cursor()
            sql = """UPDATE registro SET end_date=current_timestamp WHERE id_aluno=(SELECT id_aluno FROM aluno WHERE ra = %s) AND saida IS NULL;"""
            cursor.execute(sql, (row[2],))
            con.commit()
        return Response('Ok', status=200)
    else:
        return apology('Method not allowed', 400)

@socketio.on('connect')
def handle_connect():
    socketio.emit('connection', 'Ok')

@socketio.on('req_update')
def update_table():
    socketio.emit('update', obter_resultados_do_backend())

def obter_resultados_do_backend():
    cursor = con.cursor()
    sql = """SELECT * FROM aluno;"""
    cursor.execute(sql)
    rows = cursor.fetchall()

    resultado = []
    # Transformar a lista de tuplas em uma lista de dicionários
    for row in rows:
        result_dict = {
            'id': row[0],
            'nome': row[1],
            'ra': row[2],
            'id_aula': row[3]
        }
        resultado.append(result_dict)

    # Serializar a lista de dicionários em formato JSON
    json_output = json.dumps(resultado)
    return resultado

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)

# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

if __name__ == '__main__':
    # app.run(host='127.0.0.1', debug=True)
    socketio.run(app, debug=True)

def gen():
    while True:
        frame = reconhecimento.run()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def gen_cap():
    while True:
        frame = captura.capturar()
        
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')