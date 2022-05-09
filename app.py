from flask import Flask, redirect, url_for, render_template, request, send_file, send_from_directory
from werkzeug.utils import secure_filename
import os
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
        msg = request.form['message']
        f.save(os.path.join("./uploaded_files/",secure_filename(f.filename)))
        #f.save(secure_filename(f.filename))
        stegosaurus.encode("./uploaded_files/"+f.filename, msg)

        #stegosaurus.encode(f.filename, "test")
        #return 'Message Hidden Successfully. File ready for download.'
        #return redirect(url_for('upload_form', file_name="encoded_"+f.filename))
        return redirect(url_for('upload_form', file_name="encoded_out.png"))

@app.route('/downloader/<file_name>')
def upload_form(file_name):
    #file_name = request.args['filename']
    return render_template('download.html', file_name=file_name)

@app.route('/download/<file_name>')
def download_file(file_name):
    #path = "flower_lotus.2170.jpg"
    path=file_name

    #return send_file(path, as_attachment=True)
    return send_from_directory("./output_files/", path, as_attachment=True)

@app.route('/decode')
def decode_file():
    return render_template('decode.html')

@app.route('/decoder', methods = ['GET', 'POST'])
def decoder_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(os.path.join("./uploaded_files/",secure_filename(f.filename)))
        dec_msg = stegosaurus.decode("./uploaded_files/"+f.filename)
        print(dec_msg)

        #stegosaurus.encode(f.filename, "test")
        #return 'Message Hidden Successfully. File ready for download.'
        #return redirect(url_for('decoded', dec_msg=dec_msg))
        return render_template('decoded_message.html', dec_msg=dec_msg)

if __name__=='__main__':
    app.run()
