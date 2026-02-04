# Repository Configuration

This directory contains configuration files for repository settings and branch protection.

## 📁 Files

### `settings.yml`

Repository and branch protection configuration file. This file can be used with:

1. **Probot Settings App**: Install the [Probot Settings](https://github.com/apps/settings) GitHub App to automatically apply these settings
2. **Manual Configuration**: Use as a reference guide for manually configuring repository settings in GitHub UI

**Key configurations:**
- Repository visibility: Public
- Branch protection for `main` branch
- Pull request requirements
- Review requirements
- Restrictions on force pushes and deletions

### `BRANCH_PROTECTION_SETUP.md`

Comprehensive step-by-step guide for manually configuring branch protection rules in GitHub's web interface.

**Covers:**
- Making the repository public
- Setting up branch protection rules
- Configuring pull request requirements
- Creating CODEOWNERS file
- Verification steps
- Troubleshooting

## 🎯 Purpose

These configurations ensure that:

1. **Repository is Public**: Anyone can view and fork the repository
2. **Main Branch is Protected**: Direct pushes to `main` are not allowed
3. **Fork & PR Workflow**: All contributions must go through pull requests
4. **Code Review Required**: Changes must be reviewed before merging
5. **Quality Maintained**: Proper review and discussion for all changes

## 🚀 Quick Setup

### Option 1: Automated (Recommended)

1. Install [Probot Settings App](https://github.com/apps/settings) on your repository
2. The `settings.yml` file will automatically configure everything
3. Commit and push the settings.yml file

### Option 2: Manual Setup

Follow the detailed guide in [BRANCH_PROTECTION_SETUP.md](BRANCH_PROTECTION_SETUP.md)

## 📖 Related Documentation

- [CONTRIBUTING.md](../CONTRIBUTING.md) - Contribution guidelines for developers
- [README.md](../README.md) - Main project documentation
- [LICENSE](../LICENSE) - Project license (MIT)

## 🔒 Security

These settings protect the repository by:

- Preventing accidental or malicious direct pushes
- Requiring code review for all changes
- Maintaining an audit trail through pull requests
- Preventing force pushes that could rewrite history
- Blocking branch deletion

## ✅ What's Protected

- ✅ Main branch cannot be pushed to directly
- ✅ Main branch cannot be force-pushed to
- ✅ Main branch cannot be deleted
- ✅ All changes require pull request
- ✅ Pull requests require approval (configurable)
- ✅ Conversations must be resolved before merge

## 🤝 For Contributors

If you're a contributor, please read:
- [CONTRIBUTING.md](../CONTRIBUTING.md) for the complete workflow
- [BRANCH_PROTECTION_SETUP.md](BRANCH_PROTECTION_SETUP.md#-using-the-protected-repository) for how to work with protected branches

---

**Last Updated**: February 2025
