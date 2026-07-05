# 🖼️ Image Compression Using Principal Component Analysis (PCA)

A web-based application for image compression using the **Principal Component Analysis (PCA)** algorithm. This project is built with **Python**, **Flask**, **OpenCV**, and **NumPy**, providing an interactive interface to compress images while displaying compression statistics and allowing users to download the processed results.

---

## 📖 Overview

Principal Component Analysis (PCA) is a dimensionality reduction technique commonly used in image processing. By selecting only the most significant principal components, the application reconstructs the image with reduced data while maintaining acceptable visual quality.

This project demonstrates how PCA can be applied as an image compression technique through a simple and user-friendly web application.

---

## ✨ Features

* Upload image files (`.jpg`, `.jpeg`, `.png`)
* Compress images using the PCA algorithm
* Adjustable number of principal components (K)
* Preview original and compressed images
* Display compression statistics:

  * Runtime
  * Original file size
  * Compressed file size
  * Compression ratio
* Download compressed images
* Responsive web interface

---

## 🛠️ Technologies Used

### Backend

* Python 3
* Flask
* NumPy
* OpenCV

### Frontend

* HTML5
* CSS3
* JavaScript (Fetch API)

---

## 📂 Project Structure

```text
Project-Kompresi-Image-dengan-PCA/
│
├── backend.py                 # Flask application
├── pcacompressor.py           # PCA compression algorithm
├── index.html                 # Main interface
│
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── script.js
│   ├── uploads/
│   └── output/
│
├── test/
│   ├── input/
│   └── output/
│
├── venv/
└── README.md
```

---

# 🚀 Getting Started

## 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/Project-Kompresi-Image-dengan-PCA.git
cd Project-Kompresi-Image-dengan-PCA
```

---

## 2. Create a Virtual Environment

Linux/macOS

```bash
python3 -m venv venv
```

Windows

```powershell
python -m venv venv
```

---

## 3. Activate the Virtual Environment

Linux/macOS

```bash
source venv/bin/activate
```

Windows

```powershell
venv\Scripts\activate
```

---

## 4. Install Dependencies

```bash
pip install flask numpy opencv-python
```

---

## 5. Run the Application

```bash
python backend.py
```

Open your browser and visit:

```text
http://127.0.0.1:5000
```

---

# 📷 Supported Image Formats

* PNG
* JPG
* JPEG

---

# ⚙️ How It Works

1. Upload an image.
2. Enter the desired number of principal components (K).
3. Click **Compress Image**.
4. The PCA algorithm reconstructs the image using the selected principal components.
5. The application displays:

   * Original image
   * Compressed image
   * Runtime
   * Original size
   * Compressed size
   * Compression ratio
6. Download the compressed image if desired.

---

# 🧠 PCA Compression Workflow

```text
Input Image
      │
      ▼
Read Image
      │
      ▼
Split RGB Channels
      │
      ▼
Compute Mean
      │
      ▼
Calculate Covariance Matrix
      │
      ▼
Eigenvalue Decomposition
      │
      ▼
Select K Principal Components
      │
      ▼
Reconstruct RGB Channels
      │
      ▼
Merge Channels
      │
      ▼
Compressed Image
```

---

# 📊 Performance Metrics

The application provides the following information after each compression:

* Runtime (seconds)
* Original image size (KB)
* Compressed image size (KB)
* Compression ratio (%)

---

# 📸 Screenshots

You can place screenshots inside a `docs/` folder and display them here.

```text
docs/
├── homepage.png
├── upload.png
└── result.png
```

Example:

```markdown
## Home Page

![Home](docs/homepage.png)

## Compression Result

![Result](docs/result.png)
```

---

---

# 👨‍💻 Author
Kelompok Aljabar Linear 

Computer Science Student

---

# 📄 License

This project is licensed under the MIT License.

You are free to use, modify, and distribute this project for educational and research purposes.
