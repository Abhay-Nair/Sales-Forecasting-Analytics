# Contributing to Sales Forecasting Project

Thank you for your interest in contributing! 🎉

## How to Contribute

### Reporting Issues

If you find a bug or have a suggestion:

1. Check if the issue already exists in [Issues](https://github.com/Abhay-Nair/Sales-Forecasting-Analytics/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - Your environment (OS, Python version)

### Submitting Changes

1. **Fork the repository**
   ```bash
   git clone https://github.com/abhay/sales-forecasting-project.git
   cd sales-forecasting-project
   ```

2. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the existing code style
   - Add docstrings to new functions
   - Update documentation if needed
   - Test your changes

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add: brief description of changes"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Describe your changes
   - Link any related issues

## Code Style

- Use **snake_case** for variables and functions
- Use **PascalCase** for classes
- Add **docstrings** to all functions
- Follow **PEP 8** guidelines
- Keep functions **small and focused**

## Testing

- Test your changes by running the pipeline:
  ```bash
  python src/data_cleaning.py
  python src/train_sarima.py
  python src/forecast.py
  ```

- Ensure no errors occur
- Check that outputs are generated correctly

## Documentation

- Update README.md if you add new features
- Add docstrings to new functions
- Update IMPROVEMENTS.md if relevant

## Questions?

Feel free to open an issue for any questions or clarifications!

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person
- Help others learn and grow

Thank you for contributing! 🙏
