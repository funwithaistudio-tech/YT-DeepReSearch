# Contributing to YT-DeepReSearch

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/YT-DeepReSearch.git`
3. Create a branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Run tests: `pytest tests/`
6. Commit: `git commit -m "Add your feature"`
7. Push: `git push origin feature/your-feature-name`
8. Create a Pull Request

## Development Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Install development tools
pip install black flake8 mypy pytest-cov

# Run setup script
./setup.sh
```

## Code Style

### Python Style Guide

- Follow PEP 8 guidelines
- Use type hints for function signatures
- Maximum line length: 100 characters
- Use docstrings for all public functions and classes

### Formatting

```bash
# Format code with black
black src/ tests/

# Check with flake8
flake8 src/ tests/ --max-line-length=100

# Type checking with mypy
mypy src/ --ignore-missing-imports
```

## Testing

### Writing Tests

- Place tests in `tests/` directory
- Name test files `test_*.py`
- Use descriptive test names
- Mock external API calls
- Aim for 80%+ coverage

### Running Tests

```bash
# All tests
pytest

# Specific test file
pytest tests/test_phase1.py

# With coverage
pytest --cov=src --cov-report=html

# Verbose output
pytest -v
```

## Documentation

### Docstring Format

```python
def function_name(param1: str, param2: int) -> Dict:
    """
    Brief description of function.
    
    Args:
        param1: Description of param1
        param2: Description of param2
    
    Returns:
        Description of return value
    
    Raises:
        ExceptionType: When this exception is raised
    """
    pass
```

### Updating Documentation

- Update relevant `.md` files in `docs/`
- Update README.md for user-facing changes
- Update CHANGELOG.md for all changes
- Add code examples where appropriate

## Commit Messages

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples

```
feat(phase2): Add caching for research results

Implement Redis caching to avoid duplicate API calls
for the same queries within 24 hours.

Closes #123
```

```
fix(excel): Handle empty Excel file gracefully

Add validation to check if Excel file has data
before processing to prevent crashes.
```

## Pull Request Process

### Before Submitting

1. ✅ Run all tests and ensure they pass
2. ✅ Update documentation
3. ✅ Update CHANGELOG.md
4. ✅ Ensure code follows style guidelines
5. ✅ Add tests for new features
6. ✅ Rebase on latest main branch

### PR Description

Include:
- Summary of changes
- Motivation and context
- Testing performed
- Screenshots (if UI changes)
- Related issues

### Review Process

- At least one approval required
- All tests must pass
- Documentation must be updated
- Code coverage should not decrease

## Feature Requests

### Proposing New Features

1. Check existing issues first
2. Open a new issue with label `enhancement`
3. Describe the feature clearly
4. Explain use cases
5. Provide examples if possible

### Feature Checklist

- [ ] Feature description
- [ ] Use cases
- [ ] Implementation plan
- [ ] Testing strategy
- [ ] Documentation plan
- [ ] Breaking changes noted

## Bug Reports

### Reporting Bugs

Use the issue tracker with label `bug` and include:

1. **Description**: Clear description of the bug
2. **Steps to Reproduce**: Detailed steps
3. **Expected Behavior**: What should happen
4. **Actual Behavior**: What actually happens
5. **Environment**: Python version, OS, dependencies
6. **Logs**: Relevant log files
7. **Screenshots**: If applicable

### Bug Report Template

```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce:
1. Go to '...'
2. Click on '....'
3. See error

**Expected behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment:**
 - OS: [e.g. Ubuntu 22.04]
 - Python Version: [e.g. 3.12]
 - YT-DeepReSearch Version: [e.g. 0.1.0]

**Additional context**
Any other context about the problem.
```

## Code Review Guidelines

### As a Reviewer

- Be respectful and constructive
- Focus on code, not the person
- Ask questions, don't make demands
- Suggest alternatives
- Approve when ready

### As an Author

- Respond to all comments
- Don't take feedback personally
- Ask for clarification if needed
- Make requested changes
- Thank reviewers

## Project Structure

```
src/
├── config/          # Configuration management
├── orchestrator/    # Pipeline orchestration
├── phases/          # Phase implementations
├── research/        # Research components
├── content/         # Content generation
└── utils/           # Utility functions

tests/              # Test suite
docs/               # Documentation
```

## Areas for Contribution

### High Priority

- [ ] Integration tests for full pipeline
- [ ] Performance optimization
- [ ] Advanced caching
- [ ] Error recovery improvements
- [ ] Multi-language support

### Medium Priority

- [ ] Additional validation metrics
- [ ] Alternative API clients
- [ ] Monitoring dashboard
- [ ] CLI enhancements
- [ ] Example notebooks

### Good First Issues

- [ ] Documentation improvements
- [ ] Code comments
- [ ] Test coverage
- [ ] Minor bug fixes
- [ ] Configuration options

## Questions?

- Open an issue with label `question`
- Check existing documentation
- Review closed issues

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Code of Conduct

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone.

### Our Standards

- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what is best for the community

### Enforcement

Report unacceptable behavior to project maintainers.

---

Thank you for contributing to YT-DeepReSearch! 🎉
