from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/about')
def about():
    return "<h1>About Page</h1>"

@app.route('/contact')
def contact():
    return "<h1>Contact Page</h1>"

@app.route('/user/<name>')
def user(name):
    return f"<h1>Hello, {name}!</h1>"

@app.route('/students')
def students():
    student_list = ["Haziq", "Hussain", "Hamza"]
    return render_template("students.html", students=student_list)

if __name__ == "__main__":
    app.run(debug=True)