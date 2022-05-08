from flask import Flask, redirect, url_for, render_template, request, send_file
from werkzeug.utils import secure_filename
import stegosaurus
app = Flask(__name__)

# Using templates and Static Files
@app.route('/')
def index():
    return render_template("index.html")

# Routing calls to functions
#@app.route('/hello')
#def hello_world():
#    return 'Hello World'

# Using Variables in Flask
#@app.route('/hello/<name>')
#def hello_name(name):
#    return 'Hello %s!' % name

#@app.route('/upload')
#def upload_file():
#    return render_template('upload.html')

#@app.route('/uploader', methods = ['GET', 'POST'])
#def uploader_file():
#    if request.method == 'POST':
#        f = request.files['file']
#        f.save(secure_filename(f.filename))
#        return 'File Uploaded Successfully'

@app.route('/encode')
def encode_file():
    return render_template('encode.html')

@app.route('/encoader', methods = ['GET', 'POST'])
def encoader_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        #return 'Message Hidden Successfully. File ready for download.'
        return redirect(url_for('upload_form', file_name=f.filename))

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
