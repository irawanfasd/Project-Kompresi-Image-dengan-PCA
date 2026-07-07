import os
import cv2
import numpy as np
import sys

# Batas dimensi maksimum sebelum PCA dijalankan.
# Gambar yang lebih besar dari ini akan di-resize dulu supaya matriks
# kovarians tidak terlalu besar untuk RAM server (mencegah crash/502).
MAX_DIMENSION = 800

def pca_processing(img, num_PC):
    try:
        M = np.mean(img.T, axis=1)
        C = img - M
        V = np.cov(C.T)

        # eigh khusus untuk matriks simetris (seperti kovarians):
        # lebih cepat, lebih hemat memori, dan tidak menghasilkan
        # bilangan kompleks dibanding eig biasa.
        values, vectors = np.linalg.eigh(V)

        # eigh mengurutkan nilai secara menaik, jadi dibalik agar
        # komponen dengan varians terbesar berada di depan.
        idx = np.argsort(values)[::-1]
        vectors = vectors[:, idx]
        values = values[idx]

        vector = vectors[:, :num_PC]
        score = np.dot(C, vector)
        constructed_img = np.dot(score, vector.T) + M
        constructed_img = np.clip(constructed_img, 0, 255).astype(np.uint8)
        return constructed_img
    except Exception as e:
        print(f"Error di PCA processing: {e}", file=sys.stderr)
        return img

def compress_image(input_file, output_file, tingkat_kompresi):
    """
    Menjalankan kompresi PCA pada gambar.
    Mengembalikan path file output (string) jika berhasil, atau False jika gagal.
    Output selalu disimpan sebagai .jpg agar kompresi lossy JPEG ikut membantu
    ukuran file akhir (penting terutama untuk gambar dengan warna flat seperti
    screenshot, yang setelah PCA jadi bernoise dan membengkak jika disimpan PNG).
    """
    try:
        img_array = cv2.imread(input_file)
        if img_array is None:
            print(f"Error: Gagal membaca gambar {input_file}", file=sys.stderr)
            return False

        original_h, original_w = img_array.shape[:2]

        # Resize dulu jika gambar terlalu besar, supaya matriks kovarians
        # tidak membebani RAM server (penyebab utama crash/502 sebelumnya).
        scale = 1.0
        if max(original_h, original_w) > MAX_DIMENSION:
            scale = MAX_DIMENSION / max(original_h, original_w)
            new_w = int(original_w * scale)
            new_h = int(original_h * scale)
            img_array = cv2.resize(img_array, (new_w, new_h), interpolation=cv2.INTER_AREA)
            print(f"Gambar di-resize dari {original_w}x{original_h} ke {new_w}x{new_h} untuk efisiensi memori")

        h, w = img_array.shape[:2]
        max_k = min(h, w)
        if tingkat_kompresi > max_k:
            tingkat_kompresi = max_k
            print(f"K dibatasi ke {max_k} (maksimal dimensi gambar setelah resize)")

        b, g, r = cv2.split(img_array)
        b_compressed = pca_processing(b, tingkat_kompresi)
        g_compressed = pca_processing(g, tingkat_kompresi)
        r_compressed = pca_processing(r, tingkat_kompresi)

        reconstructed_img = cv2.merge((b_compressed, g_compressed, r_compressed))

        # Kembalikan ke ukuran asli supaya hasil tetap sebanding dengan gambar input.
        if scale != 1.0:
            reconstructed_img = cv2.resize(
                reconstructed_img, (original_w, original_h), interpolation=cv2.INTER_LINEAR
            )

        # Paksa extension output jadi .jpg, apapun input formatnya.
        base, _ = os.path.splitext(output_file)
        output_file_jpg = base + ".jpg"

        success = cv2.imwrite(output_file_jpg, reconstructed_img, [cv2.IMWRITE_JPEG_QUALITY, 85])
        if not success:
            print(f"Error: Gagal menulis file output {output_file_jpg}", file=sys.stderr)
            return False

        return output_file_jpg
    except Exception as e:
        print(f"Error di compress_image: {e}", file=sys.stderr)
        return False
