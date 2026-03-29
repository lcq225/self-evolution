# Contributing to Self-Evolution

Thank you for your interest in contributing to Self-Evolution! This guide will help you get started.

## 🎯 How to Contribute

### Report Bugs

1. **Check existing issues** - Search before creating new issue
2. **Create issue** - Use bug report template
3. **Include**:
   - Python version
   - OS version
   - Self-evolution version
   - Steps to reproduce
   - Expected vs actual behavior
   - Error messages and tracebacks

### Suggest Features

1. **Check existing issues** - Avoid duplicates
2. **Create issue** - Use feature request template
3. **Describe**:
   - Use case
   - Proposed solution
   - Alternatives considered
   - Impact on existing features

### Submit Code

#### 1. Fork and Clone

```bash
git clone https://github.com/your-username/self-evolution.git
cd self-evolution
git remote add upstream https://github.com/original-username/self-evolution.git
```

#### 2. Create Branch

```bash
git checkout -b feature/your-feature-name
```

#### 3. Make Changes

- Follow existing code style
- Add tests for new features
- Update documentation
- Keep commits focused and atomic

#### 4. Test

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Check code style
black src/self_evolution tests
flake8 src/self_evolution tests

# Type checking
mypy src/self_evolution
```

#### 5. Commit

```bash
git add .
git commit -m "feat: add new feature

- Description of change
- Related issues: #123"
```

**Commit message format:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `style:` Code style
- `refactor:` Code refactoring
- `test:` Tests
- `chore:` Maintenance

#### 6. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create Pull Request on GitHub.

### Code Review Process

1. **Automated checks** - CI/CD must pass
2. **Maintainer review** - At least one approval required
3. **Address feedback** - Respond to comments
4. **Merge** - Squash and merge by maintainer

## 📋 Code Style

### Python Style

- Follow PEP 8
- Use type hints
- Maximum line length: 88 characters
- Use docstrings for public APIs

### Example

```python
"""
Module docstring describing purpose.
"""

from typing import Optional, Dict


def example_function(
    param1: str,
    param2: Optional[int] = None
) -> Dict[str, int]:
    """
    Function docstring.
    
    Args:
        param1: Description
        param2: Description (optional)
    
    Returns:
        Description of return value
    
    Raises:
        ValueError: When parameter is invalid
    """
    if param2 is None:
        param2 = 0
    
    return {"result": len(param1) + param2}
```

## 🧪 Testing

### Writing Tests

```python
import pytest
from self_evolution import AutoErrorCatcher


def test_error_catcher():
    """Test error capture functionality"""
    with AutoErrorCatcher("test_func") as catcher:
        raise ValueError("Test error")
    
    assert catcher.has_error
    assert catcher.error.error_type == "ValueError"
```

### Running Tests

```bash
# All tests
pytest

# Specific test file
pytest tests/test_module.py

# With coverage
pytest --cov=self_evolution --cov-report=html
```

## 📝 Documentation

### Documentation Standards

- Use reStructuredText or Markdown
- Include examples
- Explain parameters and return values
- Document exceptions

### Building Docs

```bash
# Install documentation dependencies
pip install sphinx sphinx-rtd-theme

# Build HTML docs
cd docs
make html
```

## 🔐 Security

### Reporting Security Issues

**Do not create public issues for security vulnerabilities!**

Email: security@example.com

Include:
- Description of vulnerability
- Steps to reproduce
- Impact assessment
- Suggested fix (if any)

## 💬 Community

### Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Welcome newcomers
- No harassment or discrimination

### Communication Channels

- GitHub Issues - Bug reports and feature requests
- GitHub Discussions - Questions and discussions
- Email - Private matters

## 🎓 Learning Resources

- [Python Packaging Guide](https://packaging.python.org/)
- [PEP 8 Style Guide](https://pep8.org/)
- [pytest Documentation](https://docs.pytest.org/)
- [GitHub Flow](https://guides.github.com/introduction/flow/)

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Self-Evolution! 🚀
