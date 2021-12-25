from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite://///Users/fatih/Desktop/hemodiyaliz_randevu_sistemi/randevu.db'

db = SQLAlchemy(app)


class HemodiyalizVakti(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    complete = db.Column(db.Boolean)


@app.route('/')
def index():
    tamamlanmamis = HemodiyalizVakti.query.filter_by(complete=False).all()
    tamamlanmis = HemodiyalizVakti.query.filter_by(complete=True).all()

    return render_template('index1.html', tamamlanmamis=tamamlanmamis, tamamlanmis=tamamlanmis)


@app.route('/add', methods=['POST'])
def add():
    randevu = HemodiyalizVakti(text=request.form['randevuitem'], complete=False)
    db.session.add(randevu)
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/complete/<id>')
def complete(id):

    randevu = HemodiyalizVakti.query.filter_by(id=int(id)).first()
    randevu.complete = True
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/delete/<id>')
def delete(id):

    randevu = HemodiyalizVakti.query.filter_by(id=int(id)).first()
    db.session.delete(randevu)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/update/<id>',methods=['POST'])
def update(id):
    randevu = HemodiyalizVakti.query.filter_by(id=int(id)).first()
    randevu.text =request.form['randevuitem']
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
