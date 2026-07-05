import cv2
import numpy as np 

def pca_processing(img, num_PC):

    #ngetung rata2
    M = np.mean(img.T, axis=1)
    #ngurangi karo mean e
    C = img - M
    #ngitung covariance
    V = np.cov(C.T)
    #ngitung eigen value, ro eigen vectors
    values, vectors =np.linalg.eig(V)

    p = np.size(vectors, axis=1)
    #ngurutke eigen values escending
    idx = np.argsort(values)
    idx = idx [::-1]
    #sorting eigen vectors
    vectors = vectors [:,idx]
    values = values [idx]

    vector = vectors[:, range(num_PC)]
    #recontruksi gambar
    score = np.dot(C, vector)
    constructed_img = np.dot(score, vector.T) + M 
    constructed_img = np.clip(constructed_img.real, 0, 255).astype(np.uint8)
    return constructed_img

def compress_image(input_file, output_file, tingkat_kompresi):
    #lokasi nyang folder sik podo ro code py ne
    
    img_array = cv2.imread(input_file)

    #mbagi dadi 3 (biru, ijo, abang)
    b, g, r = cv2.split(img_array)

    #proses kompres 
    b_compressed = pca_processing(b, tingkat_kompresi)
    g_compressed = pca_processing(g, tingkat_kompresi)
    r_compressed = pca_processing(r, tingkat_kompresi)

    #biru, ijo, abang digabung
    reconstructed_img = cv2.merge((b_compressed, g_compressed, r_compressed))

    #output file
    cv2.imwrite(output_file, reconstructed_img)
