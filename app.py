from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/tpfinal.db'
db = SQLAlchemy(app)

class Contactos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(50))
    email = db.Column(db.String(100), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        first_name = request.form['nombre']
        last_name = request.form['apellido']
        phone = request.form['telefono']
        e_mail = request.form['email']
        if first_name!='' and last_name!='' and e_mail!='':
            dbdata = Contactos(nombre=first_name, apellido=last_name, telefono=phone, email=e_mail)
            db.session.add(dbdata)
            db.session.commit()
            return render_template('index.html') + '<h4><font style="color: green;">Se ingresaron los datos en la base...<font/><h4/>' 
        return render_template('index.html') + '<h4><font style="color: red;">Verifique si ha completado todos los campos!!!. No se ingresaron datos en la base...<font/><h4/>'       
        
@app.route('/listado', methods=['GET'])
def listado():
    contactos=Contactos.query.all()
    return render_template('listado.html', listado=contactos)

@app.route('/borrar/<id>')
def borrar(id):
    Contactos.query.filter_by(id=int(id)).delete()
    db.session.commit()
    return listado() + '<h4><font style="color: green;">Se borró el registro de la base...<font/><h4/>'
    

if __name__ == '__main__':
    db.create_all()
    app.run(port=3000, debug=True)
