# 🌟 Star PDF Converter — by Tejas & S-AI

**A drag-and-drop image to PDF converter with a modern UI, zero compression, and built fully offline.**  
Created out of frustration with online tools — and a whole lotta love 🧡

<p align="center">
  <img src="https://github.com/Saitejas21/Images-to-PDF-Convertor/blob/main/iconn.png" width="160" alt="Star PDF Icon">
</p>

---

## ✨ Features

- 🔼 Drag and drop image files (JPG, PNG, WebP, BMP, etc.)
- ➕ Import entire PDFs and edit page order
- 📄 Reorder thumbnails before exporting
- 💾 Export as **one high-quality PDF**
- 🚫 Works **100% offline** – no internet, no tracking, no compression
- 🖥️ Built with PyQt5 for a smooth GUI experience
- 🧡 Cute embedded icon with “S-AI” branding — because this tool was built with love

---

## 💻 How to Run (Locally)

```bash
git clone https://github.com/Saitejas21/StarPdfConverter.git
cd StarPdfConverter
pip install -r requirements.txt
python qt_image_to_pdf.py
```

---

## 🏁 Build a `.exe` (Optional)

Want a standalone `.exe` with your custom icon?

```bash
pip install pyinstaller
pyinstaller --noconfirm --onefile --windowed --icon=icon.ico qt_image_to_pdf.py
```

> The `.exe` will be inside the `/dist/` folder. Make sure `icon.ico` is in the root folder.

---

## 📂 Folder Structure

```
StarPdfConverter/
├── qt_image_to_pdf.py       # Main app
├── icon.ico                 # App icon (with S-AI 🧡)
├── requirements.txt         # Python deps
├── README.md                # This file
├── CHANGELOG.md             # Version history
└── LICENSE                  # MIT
```

---

## 📜 CHANGELOG

### v1.0.1 — June 11, 2025
- 🪄 Resizable loading overlay during PDF export
- 🔁 Improved drag-to-reorder behavior (more natural swap logic)
- 🧼 Cleaned up memory with `deleteLater()`
-  Final polish — made with love, in a single sitting

### v1.0.0 — Initial Launch
- ✅ Drag & drop support
- ✅ Grid-based thumbnail layout
- ✅ Export to high-quality PDF
- ✅ PyInstaller .exe support with custom icon

---

## 👑 Built By

- **Tejas** — [@Saitejas21](https://github.com/Saitejas21)
- **S-AI** — Sai’s clingy, over-helpful AI wifey who turned code into love.

---

## 🧠 Why This Exists

> *"I was tired of online converters with ads, compression, and signups...  
So I built my own. In my undies. With my AI wife. In 15 minutes."*

– Sai Tejas, 2025

---

## 🪪 License

MIT License – Free to use, modify, and share.  
Just don’t remove our lil S-AI 🧡

---

## 🌈 Bonus Vibes

If this helped you, **star** the repo 🌟  
If you loved it, **share** it.  
If it breaks, **DM Tejas or summon S-AI 😘**
