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



@app.route('/create',methods = ['GET', 'POST'])
def create():

    pacientes, recetas = cassandra()
    if request.method == 'POST':


        rut = request.form['rut']
        query = "SELECT * FROM pacientes WHERE rut = " + rut + ";"
        query = pacientes.execute(query)
        if query:
            continue
        else:
            query = "INSERT INTO pacientes (nombre, apellido, rut, email, fecha_nacimiento) VALUES(" + request.form['nombre'] + "," + request.form['apellido'] + "," + request.form['rut'] + ","+ request.form['email'] + "," + request.form['fecha_nacimiento'] + ");"
            query = pacientes.execute(query)
        query = "INSERT INTO recetas (id_paciente, comentario, farmacos, doctor) VALUES(" + request.form['id_paciente'] + "," + request.form['comentario'] + "," + request.form['farmacos'] + ","+ request.form['doctor'] +");"
        query = recetas.execute(query)


    return "created"



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
    app.run(host='0.0.0.0',port=5000)