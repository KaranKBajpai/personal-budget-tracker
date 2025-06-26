from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///budget.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# # In-memory data storage (Will upgrade to a real database later)
# entries = []

# Define the database model
class Entry(db.Model):
    id = db.Column (db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(10), nullable=False)
    category = db.Column(db.String(50), nullable=True)

# Create the database file (only runs once)
if not os.path.exists('budget.db'):
    with app.app_context():
        db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        description = request.form["description"]
        category = request.form["category"]
        amount = float(request.form["amount"])
        type = request.form["type"]

        new_entry = Entry(description=description, amount=amount, type=type, category=category)
        db.session.add(new_entry)
        db.session.commit()

        return redirect('/')

    
    entries = Entry.query.all()

    # Calculate current balance 
    income = sum(entry.amount for entry in entries if entry.type == 'income')
    expense = sum(entry.amount for entry in entries if entry.type == 'expense')
    balance = income - expense

    return render_template('index.html', entries=entries, balance=balance)

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    entry = Entry.query.get_or_404(id)
    db.session.delete(entry)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)