document.getElementById('compressionForm').addEventListener('submit', function(e) {
    e.preventDefault(); // Mencegah browser me-reload halaman

    // Mengambil elemen-elemen UI
    const form = e.target;
    const formData = new FormData(form);
    const loading = document.getElementById('loadingIndicator');
    const resultSection = document.getElementById('resultSection');
    const submitBtn = form.querySelector('button[type="submit"]');

    // Menampilkan loading dan mematikan tombol
    loading.classList.remove('d-none');
    resultSection.classList.add('d-none');
    submitBtn.disabled = true;

    // Mengirim data ke backend Flask menggunakan Fetch API
fetch('/pca/compress', {
    method: 'POST',
    body: formData
})
    .then(response => response.json())
    .then(data => {
        // Sembunyikan loading dan aktifkan tombol kembali
        loading.classList.add('d-none');
        submitBtn.disabled = false;

        if (data.success) {
            // Memasukkan URL gambar ke dalam tag <img>
            // Tambahkan timestamp untuk mencegah browser menyimpan cache gambar lama
            const timeStamp = new Date().getTime();
document.getElementById('originalImage').src = "/pca" + data.original_url + "?t=" + timeStamp;
document.getElementById('compressedImage').src = "/pca" + data.compressed_url + "?t=" + timeStamp;
            // Memperbarui teks metrik
            document.getElementById('metricRuntime').textContent = data.metrics.runtime + " dtk";
            document.getElementById('metricOriginal').textContent = data.metrics.original_size_kb + " KB";
            document.getElementById('metricCompressed').textContent = data.metrics.compressed_size_kb + " KB";
document.getElementById('metricRatio').textContent = data.metrics.compress_ratio + "%";
            // Mengatur tautan tombol unduh
document.getElementById('downloadBtn').href = "/pca/download/" + data.filename;            // Tampilkan bagian hasil
            resultSection.classList.remove('d-none');
        } else {
            alert("Error: " + data.error);
        }
    })
    .catch(error => {
        loading.classList.add('d-none');
        submitBtn.disabled = false;
        alert("Terjadi kesalahan pada jaringan atau server.");
        console.error('Error:', error);
    });
});
