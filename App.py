from flask import Flask,render_template,request

app = Flask(__name__)

@app.route('/filter')
def form():
    return render_template('form.html', template_folder='../templates')

@app.route('/add-filter', methods = ['POST', 'GET'])
def data():
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/filter' to submit form"
    if request.method == 'POST':
        form = request.form
        
        return render_template('form.html', template_folder='../templates')

