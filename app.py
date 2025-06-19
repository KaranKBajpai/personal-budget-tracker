from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# In-memory data storage (Will upgrade to a real database later)
entries = []

@app.route('/', methods=['GET', 'POST'])
def index():
    global entries
    if request.method == 'POST':
        description = request.form["description"]
        amount = float(request.form["amount"])
        type = request.form["type"]
        entries.append({
            'description': description,
            'amount': amount,
            'type': type
        })
        return redirect('/')
    return render_template('index.html', entries=entries)

if __name__ == '__main__':
    app.run(debug=True)