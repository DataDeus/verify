import os
from services import match, detect
from werkzeug.utils import secure_filename
from flask import Flask, flash, request, redirect, jsonify, url_for

response = {'verified': None, 'views': None}

#UPLOAD_FOLDER = '/Users/eliel/Postman/folder/'
UPLOAD_FOLDER = '/Users/eliel/Documents/Dev/Druve/verify/verify'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'super secret key'

def allowedFile(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/verify', methods=['POST'])
def verify():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowedFile(file.filename):
            # img = request.files['file']
            # image = img.read()
    
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image = UPLOAD_FOLDER+filename
            response['verified'] = match(image)
            if response['verified'] == True:
                response['views'] = detect(image)
            else:
                response['views'] = None
            # return redirect(url_for('download_file', name=filename))
    
    return jsonify(response)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 6001))
    app.run(debug=False, host='0.0.0.0', port=port)
    # app.debug = True
    # app.run()
# create tempn image folder 