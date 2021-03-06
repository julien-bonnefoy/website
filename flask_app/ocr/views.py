# -*- coding: utf-8 -*-
""" OCR VIEWS

BLUEPRINT: ocr_bp
ROUTES FUNCTIONS: ocr, uploaded_file
OTHER FUNCTIONS: allowed_file, tesseract_get_text, get_img_from_url, azure_get_text
"""
from PIL import Image
import requests
from flask import request, Blueprint, render_template, redirect, flash, send_from_directory
from werkzeug.utils import secure_filename
import pytesseract
import shutil
import os
from config import basedir


# Blueprint Configuration
ocr_bp = Blueprint(
    'ocr_bp',
    __name__,
    template_folder='../templates/',
    static_folder='../static/'
)

ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif', 'svg'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@ocr_bp.route('/ocr', methods=['GET', 'POST'])
def ocr():
    import shutil
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(f'app/ocr/uploads/{filename}')
                source = os.path.join(basedir, f'app/ocr/uploads/{filename}')
                img = Image.open(source)
                ocr_text = tesseract_get_text(img)
                ocr_text = ocr_text.split('\n')
                return render_template("ocr/ocr.html", source=f"/ocr/uploads/{filename}", ocr_text=ocr_text)

        elif "img_url" in request.form:
            url = request.form['img_url']
            if url == "":
                flash('No selected file')
                return redirect(request.url)
            filename = get_img_from_url(url)
            if url and allowed_file(filename):
                filename = secure_filename(filename)
                source = os.path.join(basedir, f'app/ocr/uploads/{filename}')
                img = Image.open(source)
                ocr_text = tesseract_get_text(img)
                ocr_text = ocr_text.split('\n')
                return render_template("ocr/ocr.html", source=url, ocr_text=ocr_text)
        else:
            flash('No file part')
            return redirect(request.url)

    return render_template("ocr/ocr.html")


@ocr_bp.route('/ocr/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('ocr/uploads', filename)


def tesseract_get_text(img):
    # custom_config = r'--oem 2 --psm 12'
    # result = pytesseract.image_to_string(img, config=custom_config)
    result = pytesseract.image_to_string(img)
    #with open('text_result.txt', mode ='w') as file:
    #    file.write(result)
    return result


def get_img_from_url(img_url):
    # Set up the filename
    filename = img_url.split("/")[-1]
    r = requests.get(img_url, stream=True)

    if r.status_code == 200:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True

    with open(os.path.join(basedir, f'app/ocr/uploads/{filename}'), 'wb') as file:
        shutil.copyfileobj(r.raw, file)

    return filename


def azure_get_text(url_image):
    endpoint = "https://westeurope.api.cognitive.microsoft.com"
    subscription_key = "b7b423c4968348568076f549657d6199"
    text_recognition_url = endpoint + "/vision/v3.0/ocr"

    headers = {"Ocp-Apim-Subscription-Key": subscription_key,
               'Content-type': 'application/json'}
    # params = {"includeTextDetails": True}

    data = {'url': url_image}

    response = requests.post(
        text_recognition_url, headers=headers, json=data
    )
    doc = []
    for rdrx, region in enumerate(response.json()['regions']):
        para = []
        for index, line in enumerate(response.json()['regions'][rdrx]['lines']):
            text_line = []
            for jdex, word in enumerate(line['words']):
                text_line.append(line['words'][jdex]['text'])
            text_line = ' '.join(text_line)
            para.append(text_line)
        doc.append(para)

    return doc




