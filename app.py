from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/practice_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Table mapping
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(100))

# READ - show all users
@app.route('/')
def show_users():
    users = User.query.all()
    return render_template('show2.html', users=users)

# CREATE - add new user
@app.route('/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        new_user = User(name=name, email=email)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('show_users'))
    return render_template('add2.html')

# UPDATE - edit existing user
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_user(id):
    user = User.query.get_or_404(id)
    if request.method == 'POST':
        user.name = request.form['name']
        user.email = request.form['email']
        db.session.commit()
        return redirect(url_for('show_users'))
    return render_template('update2.html', user=user)

# DELETE - remove user
@app.route('/delete/<int:id>')
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('show_users'))

if __name__ == '__main__':
    app.run(debug=True)
