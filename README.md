# 📝 Markdown-It  
### AI-Powered PDF & Image → Markdown Converter

Markdown-It is a Django web app that lets you upload a **PDF** or **image**, then automatically converts it into clean, well-formatted **Markdown text** using **ChatGPT**.

### How it looks
<img src="./Screenshot from 2025-11-01 17-18-52.png" width="60%">

---

## 🚀 Features
- 🧠 AI-based Markdown generation with OpenAI
- 📄 PDF text extraction (via `pdfplumber`)
- 🖼️ Image text extraction (via `pytesseract`)
- 💾 Local file upload handling (via `FileSystemStorage`)
- ⚙️ `.env` configuration for API keys and secrets
- 🌐 Django web interface for easy use

---

## 🧰 Tech Stack
- **Backend:** Django 5.x (Python 3.12+)
- **AI Integration:** OpenAI API
- **OCR:** Tesseract (via `pytesseract`)
- **PDF Parsing:** pdfplumber
- **Frontend:** HTML / Django templates

---

## 🧩 Project Structure
```
markdown_it/
├── converter/
│ ├── templates/converter/index.html
│ ├── utils.py
│ ├── views.py
│ ├── urls.py
│ └── ...
├── manage.py
├── .env
├── .gitignore
├── LICENSE
└── README.md
```
---

## Installation & Setup

### Clone the repository
```bash
git clone https://github.com/fekri8614/markdown-it.git
cd markdown-it
```
### Create & activate virtual environment
```bash
python3 -m venv my-venv
source my-venv/bin/activate
```
### Install dependencies
```bash
pip install -r requirements.txt
```
### Create a `.env` file in the root directory
```bash
OPENAI_API_KEY=sk-your-openai-key-here
DJANGO_SECRET_KEY=your-django-secret
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```
### Run migrations
```bash
python manage.py migrate
```
### Run the app
```bash
python manage.py runserver
```

## License
This project is licensed under the MIT LICENSE — [see LICENSE](https://github.com/fekri8614/markdown-it/blame/main/LICENSE)
