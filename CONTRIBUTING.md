# Contributing to ALMA - Advanced Learning & Metadata Assistant

Thank you for your interest in contributing to ALMA! This document explains how to contribute to this project.

## 🔒 Repository Access Policy

This repository is **public** and **read-only** for external contributors. The `main` branch is protected and cannot be modified directly, even by contributors with write access.

### How to Contribute

All contributions must be made through the **fork and pull request workflow**:

1. **Fork the repository** to your GitHub account
2. **Clone your fork** to your local machine
3. **Create a feature branch** for your changes
4. **Make your changes** and commit them
5. **Push to your fork** on GitHub
6. **Open a pull request** from your fork to this repository's `main` branch

### ✅ What You Can Do

- ✅ Fork the repository to your own GitHub account
- ✅ Clone your fork to work on it locally
- ✅ Create branches in your fork
- ✅ Submit pull requests for review
- ✅ Open issues for bugs or feature requests
- ✅ Participate in discussions

### ❌ What You Cannot Do

- ❌ Push directly to the `main` branch
- ❌ Force push to any branch
- ❌ Delete the `main` branch
- ❌ Merge pull requests without approval
- ❌ Bypass branch protection rules

## 🚀 Getting Started

### Prerequisites

- Python 3.11.x
- Git
- Azure CLI (for deployment)
- Azure account with required services (for full functionality)

### Fork and Clone

1. Click the "Fork" button at the top right of this repository
2. Clone your fork:

```bash
git clone https://github.com/YOUR-USERNAME/cpgai_chatbot.git
cd cpgai_chatbot
```

3. Add the upstream repository as a remote:

```bash
git remote add upstream https://github.com/natalinio/cpgai_chatbot.git
```

4. Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 🔄 Development Workflow

### 1. Keep Your Fork Updated

Before starting work, sync your fork with the upstream repository:

```bash
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

### 2. Create a Feature Branch

Always create a new branch for your changes:

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

Use descriptive branch names:
- `feature/` for new features
- `fix/` for bug fixes
- `docs/` for documentation changes
- `refactor/` for code refactoring

### 3. Make Your Changes

- Write clean, readable code
- Follow existing code style and conventions
- Add comments where necessary
- Update documentation if needed
- Write or update tests for your changes

### 4. Test Your Changes

Run the test suite to ensure your changes don't break existing functionality:

```bash
pytest tests/
```

### 5. Commit Your Changes

Write clear, descriptive commit messages:

```bash
git add .
git commit -m "feat: add new ETL configuration feature"
# or
git commit -m "fix: resolve Cosmos DB query issue"
```

Follow conventional commit format:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation
- `refactor:` for code refactoring
- `test:` for adding tests
- `chore:` for maintenance tasks

### 6. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

### 7. Create a Pull Request

1. Go to your fork on GitHub
2. Click "Pull Request" button
3. Select your feature branch as the source
4. Select `natalinio/cpgai_chatbot:main` as the destination
5. Fill in the pull request template:
   - Clear title summarizing the change
   - Description of what and why
   - Reference any related issues
   - Add screenshots for UI changes
6. Submit the pull request

## 📋 Pull Request Guidelines

### Before Submitting

- [ ] Code follows the project's style guidelines
- [ ] Tests pass locally
- [ ] Documentation is updated (if applicable)
- [ ] Commit messages are clear and descriptive
- [ ] Branch is up-to-date with `main`

### Pull Request Requirements

- **One feature per PR**: Keep pull requests focused on a single feature or fix
- **Description**: Provide a clear description of what changes and why
- **Testing**: Include information about how you tested your changes
- **Breaking changes**: Clearly mark any breaking changes
- **Review**: Be responsive to feedback and make requested changes

### Review Process

1. A maintainer will review your pull request
2. You may be asked to make changes or provide clarification
3. Once approved, a maintainer will merge your pull request
4. Your changes will be included in the next release

## 🐛 Reporting Bugs

Found a bug? Please open an issue with:

- Clear, descriptive title
- Steps to reproduce the bug
- Expected behavior
- Actual behavior
- Environment details (OS, Python version, etc.)
- Screenshots or logs (if applicable)

## 💡 Suggesting Features

Have an idea? Open an issue with:

- Clear description of the feature
- Use case and benefits
- Proposed implementation (optional)

## 📝 Code Style

This project follows:

- **PEP 8** for Python code style
- **Type hints** where appropriate
- **Docstrings** for functions and classes
- **Meaningful variable names**
- **Comments** for complex logic

## 🧪 Testing

- Write tests for new features
- Update tests when modifying existing code
- Ensure all tests pass before submitting PR
- Aim for good test coverage

## 📚 Documentation

- Update README.md if adding major features
- Add docstrings to new functions and classes
- Update relevant documentation files in `docs/`
- Add comments for complex code sections

## 🤝 Code of Conduct

- Be respectful and inclusive
- Accept constructive criticism
- Focus on what's best for the project
- Show empathy towards other contributors

## 📞 Getting Help

- Open an issue for questions
- Check existing documentation in `docs/`
- Review closed issues and pull requests

## 🙏 Thank You

Thank you for contributing to ALMA! Your efforts help make this project better for everyone.

---

**Note**: This repository's `main` branch is protected. All contributions must go through the fork and pull request workflow. Direct pushes to `main` are not allowed, ensuring code quality and proper review processes.
