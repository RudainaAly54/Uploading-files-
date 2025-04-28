from flask import Flask, request, render_template
import boto3
from werkzeug.utils import secure_filename

app = Flask(__name__)
s3 = boto3.client('s3')
BUCKET_NAME = 'file-sharing-2025'  # غيّري ده باسم الـ bucket بتاعك

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file uploaded', 400
    file = request.files['file']
    if file.filename == '':
        return 'No file selected', 400
    
    # تحققي من نوع الملف
    allowed_extensions = {'.pdf', '.jpg', '.jpeg', '.png', '.txt'}
    if not any(file.filename.lower().endswith(ext) for ext in allowed_extensions):
        return 'File type not allowed', 400
    
    filename = secure_filename(file.filename)
    s3.upload_fileobj(file, BUCKET_NAME, filename)
    download_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{filename}"
    return render_template('index.html', download_url=download_url)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # استخدمي port 5000 للاختبار محليًا