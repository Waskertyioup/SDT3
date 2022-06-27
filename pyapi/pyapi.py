from flask import Flask, request
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider



app = Flask(__name__)


def cassandra():
    cluster = Cluster(contact_points=['127.0.0.1'], port=9042, auth_provider=PlainTextAuthProvider(username='cassandra', password='cassandra'))

    pacientes = cluster.connect('pacientes')
    recetas = cluster.connect('recetas')

    pacientes.execute('USE pacientes')
    recetas.execute('USE recetas')

    return pacientes, recetas


@app.route('/',methods = ['GET', 'POST'])
def index():

    return "hola mundo"

@app.route('/pas',methods = ['GET', 'POST'])
def pasientes():

    if request.method == 'GET':
        pacientes, recetas = cassandra()
        query = "SELECT * FROM pacientes;"
        query = pacientes.execute(query)
        
        return query

@app.route('/res',methods = ['GET', 'POST'])
def recetas():

    if request.method == 'GET':
        pacientes, recetas = cassandra()
        query = "SELECT * FROM recetas;"
        query = pacientes.execute(query)
    
        return query


@app.route('/create',methods = ['GET', 'POST'])
def create():
    pacientes, recetas = cassandra()
    if request.method == 'POST':

        nombre = request.form['nombre']
        apellido = request.form['apellido']
        rut = request.form['rut']
        email = request.form['email']
        fecha_nacimiento = request.form['fecha_nacimiento']
        comentario = request.form['comentario']
        farmacos = request.form['farmacos']
        doctor = request.form['doctor']




    return "created"


@app.route('/update',methods = ['GET', 'POST'])
def edit():

    pacientes, recetas = cassandra()
    if request.method == 'POST':
        id = request.form['id']
        for key in request.form.items():
            if key != 'id':
                value = request.form[key]
                query = "UPDATE recetas SET " + key + " = '" + value + "' WHERE id = " + id + ";"
                recetas.execute(query)

    return "edited"

@app.route('/delete', methods = ['GET', 'POST'])
def delete():

    pacientes, recetas = cassandra()
    if request.method == 'POST':
        id = request.form['id']
        query = "DELETE FROM recetas WHERE id = " + id + ";"
        recetas.execute(query)

    return "deleted"

if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)