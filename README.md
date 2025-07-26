<div align="center">

# 🤖 Eliza AI - Email Automation Pipeline 🤖

*Automate your inbox. Extract the data. Reclaim your time.*

</div>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/status-in--development-orange.svg" alt="Project Status">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="PRs Welcome">
</p>

---

Eliza AI is a powerful, hands-off automation pipeline that transforms your email inbox into a structured data source. It diligently monitors for new emails, intelligently processes attachments like invoices or reports, extracts key information, and securely delivers the data to an SFTP server.

## ✨ Key Features

* **⏰ Scheduled Execution**: Runs automatically every hour using `apscheduler`. Never miss a beat.
* **📧 Smart Email Processing**: Connects to Gmail via IMAP to find and process only unread emails.
* **📄 Multi-Format Attachment Handling**: Effortlessly handles PDFs, DOCX, XLSX, CSV, and common image formats.
* **🧠 AI-Ready Data Extraction**: Uses a combination of libraries like PyMuPDF and Pytesseract. The core logic is a placeholder, ready for your custom AI model.
* **📊 Structured Output**: Normalizes extracted data and saves it into clean, timestamped `.csv` files.
* **🔒 Secure File Upload**: Uploads the results to your designated SFTP server using `paramiko`.
* **✍️ Comprehensive Logging**: Keeps a detailed, easy-to-read log of all operations and errors.

---

## 📂 Project Structure

```text
.
├── .venv/
├── app/
│   ├── ai/
│   │   └── extractor.py
│   ├── config/
│   │   └── settings.yaml
│   ├── core/
│   │   ├── email_handler.py
│   │   ├── ftp_uploader.py
│   │   ├── logger.py
│   │   └── normalizer.py
│   └── main.py
├── data/
│   └── logs/
│       └── eliza.log
├── model_training/
│   └── annotations/
└── requirements.txt
```

---

## 🚀 Getting Started: Setup and Installation

Follow these steps to get Eliza AI up and running.

### 1️⃣ Install System Dependencies (Tesseract)

Eliza uses Tesseract for OCR. This is a one-time setup.

* **On Linux (Ubuntu/Debian):**
    ```bash
    sudo apt update && sudo apt install tesseract-ocr
    ```
* **On macOS (using Homebrew):**
    ```bash
    brew install tesseract
    ```
* **On Windows:**
    Download and run the installer from the [Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki) page.

### 2️⃣ Set Up the Python Environment

Using a virtual environment is strongly recommended to avoid conflicts.

```bash
# Navigate to the project's root directory
cd /path/to/sem-5-project/

# Create a virtual environment
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate
```

### 3️⃣ Install Python Packages

Install all the required libraries with a single command.

```bash
pip install -r requirements.txt
```
> **Note**: The `requirements.txt` file should be in your project's root directory.

---

## ⚙️ Configuration

All configuration lives in `app/config/settings.yaml`. **This step is mandatory!**

1.  **📧 Email Settings**:
    * `username`: Your Gmail address.
    * `password`: Your **16-digit Google App Password**.
    > **⚠️ Important!** You cannot use your regular Google password. You must generate an App Password.

2.  ** SFTP Settings**:
    * Update the placeholder values with your **real SFTP server details**.
    * For local testing, you can run an OpenSSH server and use `host: "127.0.0.1"`, your Linux username, and your Linux password. Make sure the `target_dir` exists!

---

## ▶️ How to Run

1.  **Activate Environment**: Make sure your virtual environment is active (`source .venv/bin/activate`).
2.  **Send an Email**: Send a new, **unread** email with an attachment to the configured address.
3.  **Launch the App**: Run the main script from the project's root directory.

    ```bash
    python app/main.py
    ```

The script will start, process the email, and then wait for the next hourly interval. Check `data/logs/eliza.log` to see the magic happen!

---

## 🧠 A Note on the AI Model

> The current data extraction logic in `app/ai/extractor.py` is a **placeholder**. It's designed to show the pipeline works. The `model_training` directory is where you can build a real AI model to unlock the full power of Eliza.
