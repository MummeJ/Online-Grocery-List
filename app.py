from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from forms import SignUpForm, LoginForm
from flask_login import UserMixin, LoginManager, login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
login_manager = LoginManager()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'you-will-never-guess'
db = SQLAlchemy(app)
login_manager.init_app(app)


class Grocery_List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False )
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Item {}>'.format(self.id)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, index=True, unique=True )
    email = db.Column(db.String(100), nullable=False, index=True, unique=True)
    password_hash = db.Column(db.String(100), nullable=False, index=False, unique=False)
    joined_at_date = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    grocery_items = db.relationship('Grocery_List', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))

@app.route('/', methods=['POST', 'GET'])
@login_required
def index():
    if request.method == 'POST':
        item_content = request.form['content']
        new_item = Grocery_List(content=item_content, user_id=current_user.id)
        try:
            db.session.add(new_item)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your item'
    else:
        user = current_user
        items = User.query.get(current_user.id).grocery_items.all()
        users = User.query.all()
        return render_template('index.html', items=items, user=user, users=users)

@app.route('/delete/<int:id>')
@login_required
def delete(id):
    item_to_delete = Grocery_List.query.get_or_404(id)
    try:
        db.session.delete(item_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that item.'

@app.route('/update/<int:id>', methods=["POST", "GET"])
@login_required
def update(id):
    item = Grocery_List.query.get_or_404(id)
    if request.method == 'POST':
        try:
            item.content = request.form['content']
            db.session.commit()
            return redirect('/')
        except:
            return 'There was a problem updating this item'
    return render_template('update.html', item=item)
    item_to_update = Grocery_List.query.get_or_404(id)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
  form = SignUpForm(csrf_enabled=False)
  if request.method == 'POST':
      if form.validate_on_submit():
          user = User(username=form.username.data, email=form.email.data)
          user.set_password(form.password.data)
          db.session.add(user)
          db.session.commit()
          return redirect('/')
  return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm(csrf_enabled=False)
  users = User.query.all()
  if form.validate_on_submit():
      user = User.query.filter_by(username=form.username.data).first()
      if user and user.check_password(form.password.data):
          login_user(user)
          next_page = request.args.get('next')
          if next_page:
              return redirect(next_page)
          else:
              return redirect(url_for('index'))
      else:
          flash("Invalid Username or Password")
  return render_template('login.html', form=form)

@app.route('/remove_user/<int:id>')
@login_required
def remove_user(id):
     user_to_delete = User.query.get_or_404(id)
     try:
         db.session.delete(user_to_delete)
         db.session.commit()
         return redirect('/')
     except:
         return 'There was a problem deleting that user.'

@app.route('/view_list/<int:id>', methods=["POST", "GET"])
@login_required
def view_list(id):
    user = User.query.get_or_404(id)
    items = User.query.get(user.id).grocery_items.all()
    return render_template('user-items.html', items=items, user=user)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
