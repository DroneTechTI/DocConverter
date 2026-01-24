# 📄 DocConverter

**Professional Document Conversion Software**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)](https://github.com/DevilStyle/DocConverter)

A powerful, cross-platform desktop application for converting documents between multiple formats with a modern graphical interface. Pure Python implementation - no external dependencies required for most conversions!

---

## 🎯 Overview

DocConverter is a professional-grade document conversion tool designed for efficiency and ease of use. Built with Python and PyQt6, it provides a modern graphical interface for batch document conversion with real-time progress tracking and comprehensive logging.

**Key Features:**
- 🚀 **Pure Python** - No Office/LibreOffice required for most conversions
- 🔄 **Multiple Formats** - Word, PDF, Excel, PowerPoint, Images, HTML
- ⚡ **Batch Processing** - Convert multiple files simultaneously with optimized performance
- 📊 **Real-time Progress** - Live progress bars and status updates
- 🎨 **Modern UI** - Clean, intuitive interface with drag-and-drop support
- 🌍 **Cross-platform** - Works on Windows, Linux, and macOS
- 📝 **Comprehensive Logging** - Detailed logs for troubleshooting
- 🔧 **Extensible Architecture** - Easy to add new converters

---

## ✨ Supported Conversions

### Currently Available

| From | To | Library | External Dependencies |
|------|----|---------|-----------------------|
| 📝 Word (.docx, .doc) | 📄 PDF | python-docx + reportlab | ❌ None |
| 📄 PDF | 📝 Word (.docx) | pdf2docx | ❌ None |
| 🖼️ Images (PNG, JPG, BMP, GIF, TIFF) | 📄 PDF | Pillow | ❌ None |
| 📄 PDF | 🖼️ Images | pdf2image | ❌ None |
| 📊 Excel (.xlsx, .xls) | 📄 PDF | openpyxl + reportlab | ❌ None |
| 🎨 PowerPoint (.pptx) | 📄 PDF | python-pptx + reportlab | ❌ None |
| 🌐 HTML | 📄 PDF | weasyprint | ❌ None |
| 📑 PDF Merge | 📄 PDF | pypdf | ❌ None |
| 🗜️ PDF Compress | 📄 PDF | pypdf | ❌ None |

### Plugin Architecture Ready

The modular architecture allows easy addition of new converters. Simply extend `ConverterBase` and register your converter!

---

## 💻 System Requirements

### Windows
- **OS**: Windows 10 or later (64-bit recommended)
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Disk Space**: 200MB for application + dependencies

### Linux
- **OS**: Any modern distribution (Ubuntu 20.04+, Fedora 35+, etc.)
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Disk Space**: 200MB for application + dependencies

### macOS
- **OS**: macOS 10.14 (Mojave) or later
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum, 8GB recommended

---

## 📦 Installation

### Quick Start (All Platforms)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/DevilStyle/DocConverter.git
   cd DocConverter
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python main.py
   ```

### Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/macOS)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run
python main.py
```

---

## 🚀 Usage

### Graphical Interface

1. Launch the application: `python main.py`
2. Drag and drop files or click "📁 Add Files"
3. Select conversion type from dropdown
4. (Optional) Choose output folder
5. Click "🚀 Convert All"
6. Monitor progress in real-time

### Batch Conversion

Convert multiple files at once:
- Add all files to the queue
- The batch optimizer automatically parallelizes conversions
- Memory optimizer ensures efficient resource usage
- Progress is tracked per file with overall completion percentage

### Command Line (Future)

```bash
# Single file conversion
python main.py convert input.docx output.pdf

# Batch conversion
python main.py convert-batch input_folder/ output_folder/ --format pdf
```

---

## 📁 Project Structure

```
DocConverter/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── LICENSE                # MIT License
├── CHANGELOG.md           # Version history
│
├── assets/                # Application resources
│   ├── icon.ico          # Windows icon
│   └── icon.png          # Cross-platform icon
│
├── config/                # Configuration modules
│   ├── settings.py       # Application settings
│   ├── i18n.py          # Internationalization
│   └── user_settings.py  # User preferences
│
├── core/                  # Core architecture
│   ├── converter_base.py      # Abstract base class
│   ├── converter_registry.py  # Converter management
│   └── dependency_checker.py  # Dependency validation
│
├── converters/            # Converter implementations
│   ├── word_to_pdf.py
│   ├── pdf_to_word.py
│   ├── images_to_pdf.py
│   ├── pdf_to_images.py
│   ├── excel_to_pdf.py
│   ├── powerpoint_to_pdf.py
│   ├── html_to_pdf.py
│   ├── pdf_merge.py
│   └── pdf_compress.py
│
├── gui/                   # Graphical interface
│   ├── main_window.py    # Main application window
│   ├── styles/           # UI themes
│   └── widgets/          # Custom widgets
│
├── utils/                 # Utility modules
│   ├── logger.py         # Logging system
│   ├── error_handler.py  # Error management
│   ├── file_handler.py   # File operations
│   ├── batch_optimizer.py    # Batch processing
│   └── memory_optimizer.py   # Memory management
│
└── tests/                 # Unit tests
    ├── test_converters.py
    └── test_new_features.py
```

---

## 🛠️ Development

### Adding a New Converter

1. Create a new file in `converters/`:

```python
from core.converter_base import ConverterBase
from utils.error_handler import ConversionError

class MyConverter(ConverterBase):
    def get_info(self):
        return {
            'name': 'My Converter',
            'input_formats': ['.ext1', '.ext2'],
            'output_format': '.pdf',
            'description': 'Converts my format to PDF',
            'requires_dependency': None
        }
    
    def convert(self, input_path, output_path, progress_callback=None, **kwargs):
        # Implement conversion logic
        return True
```

2. Register in `converters/__init__.py`:

```python
from .my_converter import MyConverter
registry.register(MyConverter)
```

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_converters.py

# Run with coverage
python -m pytest --cov=. tests/
```

---

## 🐛 Troubleshooting

### Common Issues

**Import Errors**
```bash
pip install -r requirements.txt --upgrade
```

**Permission Errors**
- Ensure files are not open in other applications
- Check file/folder permissions
- Run as administrator (if necessary)

**Missing Libraries**
The application auto-installs missing Python packages on first run. If auto-install fails:
```bash
pip install python-docx pypdf Pillow reportlab openpyxl python-pptx weasyprint pdf2docx pdf2image colorlog psutil
```

**GUI Not Starting**
- Verify PyQt6 installation: `pip install PyQt6 --upgrade`
- Check Python version: `python --version` (must be 3.8+)

### Logs

Application logs are stored in `logs/docconverter.log` with automatic rotation (max 10MB, 5 backups).

---

## 📝 Version History

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

**Current Version: 2.5.0**
- Complete English translation
- Professional code refactoring
- Enhanced type hints and documentation
- Improved architecture and modularity

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2026 DocConverter Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

## 👤 Author

**DocConverter Team**
- GitHub: [@DevilStyle](https://github.com/DevilStyle)

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add type hints to all functions
- Write comprehensive docstrings (Google style)
- Include unit tests for new features
- Update documentation as needed

---

## ⭐ Show Your Support

If you find this project useful, please consider giving it a star on GitHub!

---

## 📧 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing documentation
- Review closed issues for solutions

---

**Made with ❤️ by DocConverter Team**
