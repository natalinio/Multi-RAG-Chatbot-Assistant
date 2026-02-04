# Branch Protection Setup Guide

This guide explains how to configure branch protection rules for the repository to make it public while preventing direct modifications to the `main` branch.

## 🎯 Goal

Make the repository **public** while ensuring that:
- The `main` branch is **protected from direct pushes**
- Contributors must use the **fork and pull request workflow**
- All changes require **review before merging**
- Code quality is maintained through proper review processes

## 📋 Step-by-Step Setup

### Step 1: Make Repository Public

1. Go to your repository on GitHub
2. Click on **Settings** (gear icon)
3. Scroll down to the **Danger Zone** section
4. Click **Change visibility**
5. Select **Make public**
6. Confirm the change

### Step 2: Enable Branch Protection for Main

1. In repository **Settings**, click on **Branches** in the left sidebar
2. Under **Branch protection rules**, click **Add rule** (or **Add branch protection rule**)
3. In **Branch name pattern**, enter: `main`

### Step 3: Configure Protection Rules

Enable the following settings for maximum protection:

#### Protect Matching Branches

✅ **Require a pull request before merging**
  - ✅ Require approvals: Set to **1** (or more for stricter review)
  - ✅ Dismiss stale pull request approvals when new commits are pushed
  - ✅ Require review from Code Owners (optional, requires CODEOWNERS file)

✅ **Require status checks to pass before merging**
  - ✅ Require branches to be up to date before merging
  - Select specific status checks if you have CI/CD configured

✅ **Require conversation resolution before merging**
  - Ensures all review comments are addressed

✅ **Require signed commits** (optional, for extra security)

✅ **Require linear history** (optional, prevents merge commits)

✅ **Do not allow bypassing the above settings**
  - Ensures even administrators must follow the rules

❌ **Allow force pushes** - Keep this DISABLED
  - Prevents force pushing to main

❌ **Allow deletions** - Keep this DISABLED
  - Prevents deletion of the main branch

#### Rules Applied to Everyone

✅ **Include administrators**
  - Applies these rules even to repository administrators
  - Ensures consistent workflow for everyone

### Step 4: Additional Repository Settings

1. In **Settings** → **General**:
   - ✅ Enable **Issues**
   - ✅ Enable **Allow forking**
   - ✅ Enable **Sponsorships** (optional)
   - Choose merge options:
     - ✅ Allow merge commits
     - ✅ Allow squash merging
     - ✅ Allow rebase merging
   - ✅ Enable **Automatically delete head branches** (cleans up after merge)

### Step 5: Create CODEOWNERS File (Optional)

Create `.github/CODEOWNERS` to automatically request reviews from specific people:

```
# Default owner for everything in the repo
*       @natalinio

# Python application files
*.py    @natalinio
/app/   @natalinio

# Configuration files
*.yml   @natalinio
*.yaml  @natalinio
*.json  @natalinio

# Documentation
*.md    @natalinio
/docs/  @natalinio
```

## 🔒 What This Achieves

### For Repository Owner

- ✅ Control over all changes through PR review
- ✅ Maintain code quality standards
- ✅ Track all changes through pull requests
- ✅ Ability to discuss changes before merging
- ✅ Can still merge PRs from contributors

### For Contributors

- ✅ Can fork the repository freely
- ✅ Work on their own branches
- ✅ Submit pull requests for review
- ✅ Participate in discussions
- ❌ Cannot push directly to main
- ❌ Cannot force push or delete branches
- ❌ Cannot bypass review requirements

## 📝 Automation with Probot Settings App

Instead of manual configuration, you can use the Probot Settings GitHub App:

1. Install [Probot Settings](https://github.com/apps/settings) app on your repository
2. The `.github/settings.yml` file in this repository will automatically configure:
   - Repository settings
   - Branch protection rules
   - Other repository configurations

## ✅ Verification

After setup, verify the protection is working:

1. Try to push directly to main (should be blocked):
   ```bash
   git checkout main
   git commit --allow-empty -m "test"
   git push origin main
   # Should fail with: "refusing to allow a Personal Access Token to create or update workflow"
   ```

2. Verify the fork workflow works:
   ```bash
   # Create a new branch
   git checkout -b test-branch
   git commit --allow-empty -m "test"
   git push origin test-branch
   # Should succeed, then create a PR on GitHub
   ```

## 🚀 Using the Protected Repository

### For the Repository Owner

When you want to make changes:

1. Create a feature branch
2. Make your changes
3. Push the branch
4. Create a pull request
5. Review and merge (you can approve your own PR or wait for CI checks)

### For Contributors

Follow the workflow in [CONTRIBUTING.md](../CONTRIBUTING.md):

1. Fork the repository
2. Clone your fork
3. Create a feature branch
4. Make changes and commit
5. Push to your fork
6. Create a pull request

## 📚 Additional Resources

- [GitHub Branch Protection Documentation](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [Probot Settings App](https://probot.github.io/apps/settings/)
- [CODEOWNERS Documentation](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)

## 🤔 Troubleshooting

### "I can't push to main even though I'm the owner"

This is expected! The branch protection applies to everyone, including administrators. Use pull requests instead.

### "How do I make urgent fixes?"

Even urgent fixes should go through a PR, but you can:
1. Create a branch
2. Make the fix
3. Create a PR
4. Approve and merge it immediately
5. This maintains the audit trail

### "Can I temporarily disable protection?"

You can, but it's not recommended. If you must:
1. Go to Settings → Branches
2. Edit the protection rule
3. Disable specific rules
4. Remember to re-enable them after

---

**Note**: These settings ensure your repository remains public and forkable while maintaining control over the main branch and code quality.
