from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
import cv2
import numpy as np
from model_training import load_model, predict_sign_language

app = Flask(__name__)

# 업로드된 파일을 저장할 폴더 경로 설정
UPLOAD_FOLDER = 'static/upload/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 허용할 파일 확장자
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov'}


# 허용된 파일 확장자 여부 확인 함수
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# 수어 인식 모델 로드
model = load_model()


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # 파일이 요청에 포함되어 있는지 확인
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        # 파일이 선택되지 않은 경우
        if file.filename == '':
            return redirect(request.url)

        # 파일이 허용된 확장자인지 확인
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # 수어 인식 함수 호출
            translation = predict_sign_language(model, filepath)

            return render_template('upload.html', filename=filename, translation=translation)

    return render_template('upload.html')


# 업로드된 파일을 보여주기 위한 URL 라우팅
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return redirect(url_for('static', filename='uploads/' + filename))


if __name__ == "__main__":
    app.run(debug=True)