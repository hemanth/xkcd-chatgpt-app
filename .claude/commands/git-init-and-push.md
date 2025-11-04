# Git Init and Push Workflow

Initialize a git repository, create an initial commit with conventional commit format, and push to a remote GitHub repository.

## Prerequisites
- Project files are ready to be committed
- GitHub repository URL is available
- Author name and email are known

## Workflow Steps

### 1. Initialize Git Repository
```bash
git init
```

### 2. Configure Git Author
```bash
git config user.name "Author Name"
git config user.email "author.email@example.com"
```

### 3. Stage All Changes
```bash
git add -A
```

### 4. Check Staged Files
```bash
git status
```

### 5. Create Initial Commit
Use conventional commit format (feat, fix, docs, style, refactor, test, chore):

```bash
git commit -m "$(cat <<'EOF'
feat: initial release of project-name v1.0.0

- Feature description 1
- Feature description 2
- Feature description 3
EOF
)"
```

### 6. Add Remote Repository
```bash
git remote add origin https://github.com/username/repo-name.git
```

### 7. Push to Main Branch
```bash
git push -u origin main
```

### 8. Verify Push
```bash
git remote -v
git log --format="%an <%ae>%n%s%n%b" -1
```

## Conventional Commit Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, semicolons, etc.)
- **refactor**: Code refactoring without changing functionality
- **test**: Adding or updating tests
- **chore**: Maintenance tasks, dependencies, configuration

## Example Commit Messages

### Feature Release
```
feat: initial release of xkcd-chatgpt-app v1.0.0

- Implemented MCP server for XKCD comic viewer widget
- Added modular architecture with src/xkcd_app package structure
- Created widget-backed tools following OpenAI Apps SDK patterns
```

### Bug Fix
```
fix: resolve image loading issue in comic viewer

- Added base64 encoding to bypass CSP restrictions
- Implemented error handling for failed image loads
```

### Documentation
```
docs: update README with project structure

- Added directory tree showing src/ layout
- Updated installation instructions
- Included API documentation links
```

## Best Practices

1. **Never mention AI assistants** in commit messages or author fields
2. **Use meaningful commit messages** that describe what and why
3. **Follow conventional commit format** for consistency
4. **Stage files intentionally** - review what's being committed
5. **Verify author information** before committing
6. **Check remote URL** before pushing
7. **Use descriptive bullet points** in commit body

## Common Issues and Solutions

### Issue: Wrong Author Information
```bash
# Fix last commit author
git commit --amend --author="Correct Name <correct@email.com>"
```

### Issue: Forgot to Add Files
```bash
# Add missed files
git add file1.py file2.py
git commit --amend --no-edit
```

### Issue: Wrong Remote URL
```bash
# Remove and re-add remote
git remote remove origin
git remote add origin https://github.com/username/correct-repo.git
```

### Issue: Need to Change Branch Name
```bash
# Rename current branch
git branch -m old-name new-name
```

## Template for New Projects

```bash
#!/bin/bash

# Configuration
AUTHOR_NAME="Your Name"
AUTHOR_EMAIL="your.email@example.com"
REPO_URL="https://github.com/username/repo-name.git"
PROJECT_VERSION="1.0.0"
PROJECT_NAME="project-name"

# Initialize and configure
git init
git config user.name "$AUTHOR_NAME"
git config user.email "$AUTHOR_EMAIL"

# Stage and commit
git add -A
git commit -m "feat: initial release of $PROJECT_NAME v$PROJECT_VERSION

- Feature description here
- Additional features
- Configuration details"

# Push to remote
git remote add origin "$REPO_URL"
git push -u origin main

# Verify
echo "✅ Pushed to: $REPO_URL"
git log --oneline -1
```

## Quick Reference

| Command | Purpose |
|---------|---------|
| `git init` | Initialize repository |
| `git add -A` | Stage all changes |
| `git status` | Check staged files |
| `git commit -m "msg"` | Commit with message |
| `git remote add origin URL` | Add remote |
| `git push -u origin main` | Push and set upstream |
| `git log -1` | Show last commit |

## Notes

- This workflow creates a new repository from scratch
- For existing repositories, skip the `git init` step
- Always review staged changes before committing
- Verify push succeeded by checking GitHub repository
