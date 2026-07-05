import os
import time
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from pcacompressor import compress_image

# mulai aplikasi Flask
app = Flask(__name__, template_folder='./')

# pengaturan folder penyimpanan
UPLOAD_FOLDER = 'test/input'
OUTPUT_FOLDER = 'test/output'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Membuat folder jika belum ada saat server berjalan
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
# membatasi jenis file yang boleh diupload (png, jpg, jpeg)
def file_diizinkan(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/') # menghubungkan dengan file html
def index():
    return render_template('index.html')

@app.route('/compress', methods=['POST'])
def compress_api():
    # memeriksa apakah ada gambar yang diunggah
    if 'image' not in request.files:
        return jsonify({'error': 'Tidak ada gambar yang diunggah'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'Nama file kosong'}), 400
    
    try:
        k_value = int(request.form.get('k_value'))
    except ValueError:
        return jsonify({'error': 'Nilai harus berupa angka!'}), 400
    
    if file and file_diizinkan(file.filename):
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_path)

        # nama file output
        output_filename = f"compressed_{k_value}_{filename}"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

        # jalankan kompresi dan catat waktu
        start_time = time.time()
        success = compress_image(input_path, output_path, k_value)
        end_time = time.time()

        if success:
            # hitung waktu
            runtime = round(end_time - start_time, 2)
            
            original_size = os.path.getsize(input_path)
            compressed_size = os.path.getsize(output_path)
            
            # menghitung perubahan ukuran file
            compress_ratio = ((original_size - compressed_size) / original_size) * 100

            return jsonify({
                'success': True,
                'original_url': f"/{input_path}",
                'compressed_url': f"/{output_path}",
                'filename': output_filename,
                'metrics': {
                    'runtime': runtime,
                    'original_size_kb': round(original_size / 1024, 2),
                    'compressed_size_kb': round(compressed_size / 1024, 2),
                    'compress_ratio': round(compress_ratio, 2)
                }
            })
        else:
            return jsonify({'error': 'Gagal melakukan kompresi gambar!'}), 500
    else:
        return jsonify({'error': 'Format file tidak didukung'}), 400
    
@app.route('/download/<filename>')
def download_file(filename):
    # untuk mengunduh hasil kompresi gambar
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename, as_attachment=True)

if __name__=='__main__':
    # menjalankan serverdalam mode debug
    app.run(debug=True, port=5000)



