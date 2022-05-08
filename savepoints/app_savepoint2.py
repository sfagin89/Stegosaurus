from flask import Flask, redirect, url_for, render_template, request, send_file
from werkzeug.utils import secure_filename
import stegosaurus
app = Flask(__name__)

# Using templates and Static Files
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/encode')
def encode_file():
    return render_template('encode.html')

@app.route('/encoder', methods = ['GET', 'POST'])
def encoder_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        stegosaurus.encode(f.filename, "test")
        #return 'Message Hidden Successfully. File ready for download.'
        return redirect(url_for('upload_form', file_name="encoded_"+f.filename))

@app.route('/downloader/<file_name>')
def upload_form(file_name):
    #file_name = request.args['filename']
    return render_template('download.html', file_name=file_name)

@app.route('/download/<file_name>')
def download_file(file_name):
    #path = "flower_lotus.2170.jpg"
    path=file_name
    return send_file(path, as_attachment=True)

if __name__=='__main__':
    app.run()
