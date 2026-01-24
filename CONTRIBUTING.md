# Contributing to DocConverter

Thank you for considering contributing to DocConverter! 🎉

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- System information (OS, Python version, DocConverter version)
- Log file if available

### Suggesting Features

Feature requests are welcome! Please:
- Check if the feature has already been requested
- Provide a clear use case
- Explain how it would benefit users

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Make your changes**
   - Follow PEP 8 style guidelines
   - Add type hints to all functions
   - Write Google-style docstrings
   - Include tests if applicable

4. **Commit your changes**
   ```bash
   git commit -m "Add amazing feature"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/amazing-feature
   ```

6. **Open a Pull Request**

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/DocConverter.git
cd DocConverter

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov black flake8
```

## Code Style

- Follow PEP 8
- Use type hints
- Write docstrings (Google style)
- Keep functions focused and small
- Use meaningful variable names

### Example:

```python
def convert_document(
    input_path: str,
    output_path: str,
    progress_callback: Optional[Callable[[int, str], None]] = None
) -> bool:
    """
    Convert a document from one format to another.
    
    Args:
        input_path: Path to input file
        output_path: Path to output file
        progress_callback: Optional callback for progress updates
        
    Returns:
        True if conversion succeeded
        
    Raises:
        ConversionError: If conversion fails
    """
    # Implementation here
    pass
```

## Testing

Run tests before submitting:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. tests/

# Run specific test
pytest tests/test_converters.py
```

## Adding a New Converter

1. Create new file in `converters/`
2. Extend `ConverterBase`
3. Implement `get_info()` and `convert()`
4. Register in `converters/__init__.py`
5. Add tests
6. Update documentation

## Questions?

Feel free to open an issue for any questions about contributing!

---

**Thank you for making DocConverter better!** ❤️
