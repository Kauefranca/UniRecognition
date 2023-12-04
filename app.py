import shutil
import psycopg2
import json

from tempfile import mkdtemp
from os import mkdir, listdir, path
from datetime import datetime
from flask import Flask, Response
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from flask_socketio import SocketIO
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash

from utils.Uteis import erro, login_required
from utils.Reconhecimento import ReconhecimentoFacial
from utils.Treinamento import TreinadorReconhecimentoFacial
from utils.CameraFeed import CameraFeed
from utils.Captura import CapturaFaces
from utils.Conexão import DatabaseConnection

# Remover arquivos temporários antigos.
shutil.rmtree(path.join('Fotos'), ignore_errors=True)
mkdir(path.join('Fotos'))

ID_AULA = 1

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
socketio = SocketIO(app)

classifier_file = 'src\\frontalFaceHaarcascade.xml'
recognizer_file = 'src\\classificadores\\BCCA.yml'
cascade_file = "src\\frontalFaceHaarcascade.xml"  # Arquivo do classificador Haar

camera = CameraFeed()
treinador = TreinadorReconhecimentoFacial()
captura = CapturaFaces(cascade_file)
reconhecimento = ReconhecimentoFacial(classifier_file, recognizer_file)

reconhecimento.setStatus(None)

# Garantir que as respostas não entrem em cache
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

db = DatabaseConnection(host='localhost', database='postgres', user='postgres', password='unimar')
db.connect()

rows = db.execute_query("""SELECT * FROM aluno WHERE id_aula = (SELECT id_aula FROM aula WHERE id_aula = %s);""", ID_AULA)

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
@login_required
def reconhecer():
    data = db.execute_query("""SELECT * FROM aluno WHERE id_aula = (SELECT id_aula FROM aula WHERE id_aula = %s) ORDER BY nome;""", ID_AULA)

    return render_template('reconhecer.html', data=data)

@app.route("/registrar", methods=["GET", "POST"])
@login_required
def registrar():
    if request.method == "POST":
        if not request.form.get("nome"):
            return erro("Campo 'Nome' obrigatório!", 400)

        elif not request.form.get("ra"):
            return erro("Campo 'RA' obrigatório!", 400)
    
        elif not request.form.get("id_aula"):
            return erro("Campo 'id_aula' obrigatório!", 400)
        
        rows = db.execute_query("""SELECT * FROM aluno WHERE ra = %s""", (request.form.get("ra"),))

        if rows:
            return erro("Já existe alguém com esse RA cadastrado!", 400)
        
        db.execute_update("""INSERT INTO aluno(nome, ra, id_aula) VALUES (%s, %s, %s)""", (request.form.get("nome"), request.form.get("ra"), request.form.get("id_aula")))

        captura.iniciarCaptura(request.form.get("ra"))

        return redirect("/registrar")
    else:
        data = db.execute_query("""SELECT nome, id_aula FROM aula ORDER BY nome;""", ID_AULA)
        return render_template('registrar.html', data=data)

@app.route("/treinar", methods=["GET", "POST"])
@login_required
def treinar():
    if request.method == 'POST':
        treinador.treinar('src\\classificadores\\BCCA.yml', ID_AULA)
        return redirect('/treinar')
    else:
        data = db.execute_query("""SELECT nome, id_aula FROM aula WHERE id_aula = %s ORDER BY nome;""", ID_AULA)

        return render_template('treinar.html', data=data)

@app.route("/relatorio", methods=["GET", "POST"])
@login_required
def relatorio():
    if request.method == 'POST':
        if not request.form.get("tipo_relatorio"):
            return erro("Campo 'tipo_relatorio' obrigatório!", 400)
        
        if request.form.get("tipo_relatorio") == "listagem":
            rows = db.execute_query("""SELECT nome, ra, id_aula FROM aluno ORDER BY nome""")
            ids = dict(db.execute_query("""SELECT id_aula, nome FROM aula"""))

            return render_template("visualize.html", rows=rows, ids=ids, type="listagem")
        
        elif request.form.get("tipo_relatorio") == "presenca":
            rows = db.execute_query("""SELECT a.nome, a.ra, r.entrada, r.saida FROM aluno a LEFT JOIN registro r ON r.id_aluno = a.id_aluno;""")

            return render_template("visualize.html", rows=rows, type="presenca")
    else:
        return render_template('relatorio.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            return erro("must provide username", 400)
        
        elif not request.form.get("password"):
            return erro("must provide password", 400)

        rows = db.execute_query("""SELECT * FROM usuario WHERE login = %s;""", (request.form.get("username"),))

        if len(rows) != 1 or not check_password_hash(rows[0][2], request.form.get("password")):
            return erro("invalid username and/or password", 400)

        session["user_id"] = rows[0][0]
        session['alert'] = 'Login sucessful!'
        return redirect("/")

    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/incluir_fotos", methods=["POST"])
def incluir():
    if request.method == "POST":
        ra = request.form.get("ra")
        if not ra:
            return erro("Campo 'ra' obrigatório!", 400)
            
        for item in listdir(path.join('fotos', ra)):
            with open(path.join('fotos', ra, item), 'rb') as file:
                image_binary = file.read()

            db.execute_update("""INSERT INTO imagem(imagem, id_aluno) VALUES (%s, (SELECT id_aluno FROM aluno WHERE ra = %s));""", (image_binary, ra))

        shutil.rmtree(path.join('fotos', ra), ignore_errors=True)
        return redirect("/cadastrar")
    else:
        return erro('Method not allowed', 400)
    
@app.route("/start_aula", methods=["POST"])
def start_aula():
    if request.method == "POST":
        reconhecimento.setStatus('entrada')
        rows = db.execute_query("""SELECT * FROM aluno WHERE id_aula = %s ORDER BY nome;""", (ID_AULA,))

        for row in rows:
            db.execute_update("""INSERT INTO registro(id_aluno, id_aula, start_date) VALUES (%s, %s, %s);""", (row[0], ID_AULA, datetime.now()))

        return Response('Ok', status=200)
    else:
        return erro('Method not allowed', 400)

@app.route("/end_aula", methods=["POST"])
def end_aula():
    if request.method == "POST":
        reconhecimento.setStatus('saida')
        rows = db.execute_query("""SELECT * FROM aluno WHERE id_aula = %s ORDER BY nome;""", (ID_AULA,))

        for row in rows:
            db.execute_update("""UPDATE registro SET end_date=current_timestamp WHERE id_aluno=(SELECT id_aluno FROM aluno WHERE ra = %s) AND saida IS NULL;""", (row[2],))

        return Response('Ok', status=200)
    else:
        return erro('Method not allowed', 400)

@socketio.on('connect')
def handle_connect():
    socketio.emit('connection', 'Ok')

@socketio.on('req_update')
def update_table():
    result = obter_resultados_do_backend()
    socketio.emit('update', result)

def obter_resultados_do_backend():
    rows = db.execute_query("""SELECT a.nome, a.ra, r.entrada, r.saida, r.start_date, r.end_date FROM aluno a LEFT JOIN registro r ON r.id_aluno = a.id_aluno WHERE r.end_date IS NULL""")

    if (len(rows) <= 0): 
        return {}
    
    resultado = []
    for row in rows:
        result_dict = {
            'nome': row[0],
            'ra': row[1],
            'entrada': row[2].strftime("%d/%m/%Y %H:%M:%S") if row[2] is not None else None,
            'saida': row[3].strftime("%d/%m/%Y %H:%M:%S") if row[3] is not None else None,
        }
        resultado.append(result_dict)

    json_output = json.dumps(resultado)
    return json_output

def errorhandler(e):
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return erro(e.name, e.code)

# Método para capturar erros
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

if __name__ == '__main__':
    socketio.run(app, debug=True)

def gen():
    while True:
        frame = reconhecimento.run()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def gen_cap():
    while True:
        frame = captura.capturar()
        
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')