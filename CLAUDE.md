# CLAUDE.md - AI Assistant Guide for Conjugation Repository

> **Last Updated:** 2025-12-08
> **Repository:** sophiness/conjugation
> **Status:** Early Development / Initial Setup

## Table of Contents
- [Repository Overview](#repository-overview)
- [Current Repository Structure](#current-repository-structure)
- [Development Workflow](#development-workflow)
- [Git Branch Conventions](#git-branch-conventions)
- [Code Style and Conventions](#code-style-and-conventions)
- [Testing Guidelines](#testing-guidelines)
- [AI Assistant Best Practices](#ai-assistant-best-practices)
- [Common Tasks](#common-tasks)

---

## Repository Overview

### Purpose
The `conjugation` repository is a project focused on [to be determined based on future development].

### Current State
- **Status:** Early development phase
- **Initial Commit:** ee4bed7 - Initial commit
- **Files:** README.md only (minimal setup)
- **No dependencies or build configuration yet**

### Technology Stack
*To be determined as the project evolves*

---

## Current Repository Structure

```
conjugation/
├── .git/                 # Git version control
├── README.md            # Project readme
└── CLAUDE.md            # This file - AI assistant guide
```

### Expected Future Structure
As the project develops, anticipate the following structure:

```
conjugation/
├── src/                 # Source code
├── tests/               # Test files
├── docs/                # Documentation
├── config/              # Configuration files
├── scripts/             # Build/utility scripts
├── package.json         # (if Node.js project)
├── requirements.txt     # (if Python project)
├── README.md
└── CLAUDE.md
```

---

## Development Workflow

### 1. Branch Management

**Feature Branch Pattern:**
- All development work should be done on feature branches
- Current development branch: `claude/claude-md-mixndcxf6u3wq8ob-01Kbe2g5jnH3xh9aVZyFxvvP`
- Branch naming for Claude sessions: `claude/claude-<description>-<session-id>`

**Before Starting Work:**
```bash
# Check current branch
git status

# Ensure you're on the correct feature branch
git branch --show-current

# If branch doesn't exist, create it
git checkout -b <branch-name>
```

### 2. Making Changes

1. **Read First**: Always read existing files before modifying them
2. **Plan**: Use TodoWrite tool for multi-step tasks
3. **Implement**: Make focused, incremental changes
4. **Test**: Verify changes work as expected
5. **Commit**: Use clear, descriptive commit messages

### 3. Commit Guidelines

**Commit Message Format:**
```
<type>: <brief description>

<optional detailed explanation>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks
- `style`: Code style changes (formatting, etc.)

**Examples:**
```bash
git commit -m "feat: add verb conjugation engine"
git commit -m "docs: update README with usage examples"
git commit -m "fix: handle irregular verb edge cases"
```

### 4. Pushing Changes

**Always use:**
```bash
git push -u origin <branch-name>
```

**Important:** Branch must start with `claude/` and end with matching session ID for Claude-initiated work.

**Network Retry Policy:**
- If push fails due to network errors, retry up to 4 times
- Use exponential backoff: 2s, 4s, 8s, 16s between attempts

---

## Git Branch Conventions

### Branch Types

1. **Main Branch** (production-ready code)
2. **Feature Branches** (`feature/<feature-name>`)
3. **Claude Branches** (`claude/claude-<description>-<session-id>`)
4. **Bugfix Branches** (`fix/<bug-description>`)

### Protection Rules

- **NEVER** push directly to main without explicit permission
- **NEVER** force push to main/master
- **NEVER** use `--force` unless explicitly requested
- **NEVER** use `--no-verify` to skip hooks

### Pull Request Process

When creating PRs:
1. Ensure all tests pass
2. Write clear PR description with:
   - Summary of changes
   - Testing performed
   - Any breaking changes
3. Reference related issues if applicable

---

## Code Style and Conventions

### General Principles

1. **Simplicity Over Complexity**
   - Don't over-engineer solutions
   - Avoid premature abstractions
   - Keep code readable and maintainable

2. **Security First**
   - No command injection vulnerabilities
   - No XSS vulnerabilities
   - No SQL injection vulnerabilities
   - Follow OWASP Top 10 guidelines

3. **Minimal Changes**
   - Only change what's necessary
   - Don't refactor unrelated code
   - Don't add features that weren't requested

### Code Organization

*To be defined as codebase develops*

### Naming Conventions

*To be defined based on chosen programming language(s)*

---

## Testing Guidelines

### Test Philosophy

- Write tests for new features
- Maintain existing tests
- Ensure tests pass before committing

### Running Tests

*To be defined when test framework is established*

### Test Coverage

*To be defined based on project requirements*

---

## AI Assistant Best Practices

### Before Starting Any Task

1. **Understand Context**: Read existing code before modifying
2. **Plan Complex Tasks**: Use TodoWrite for multi-step operations
3. **Check Branch**: Verify you're on the correct development branch
4. **Review Status**: Run `git status` to understand current state

### During Development

1. **Read Files First**: Never propose changes to unread code
2. **Use Specialized Tools**: Prefer Read/Edit/Write over bash commands
3. **Parallel Operations**: Run independent tasks in parallel when possible
4. **Track Progress**: Update todos as you complete steps

### Code Modifications

1. **Preserve Formatting**: Match existing indentation and style
2. **Avoid Over-Engineering**:
   - Don't add unnecessary error handling
   - Don't create abstractions for one-time use
   - Don't add comments to unchanged code
3. **Security Checks**: Review for common vulnerabilities
4. **Test Changes**: Verify modifications work correctly

### Git Operations

1. **Safe Commits**:
   - Never skip hooks unless requested
   - Never amend other developers' commits
   - Check authorship before amending
2. **Clear Messages**: Follow commit message conventions
3. **Status Checks**: Run `git status` after commits to verify
4. **No Secrets**: Don't commit .env, credentials, or sensitive files

### Communication Style

- Be concise and direct
- No unnecessary emojis (unless user requests)
- Output text directly, not via bash echo
- Focus on technical accuracy

---

## Common Tasks

### Creating a New Feature

```bash
# 1. Create feature branch
git checkout -b feature/feature-name

# 2. Implement changes (using appropriate tools)
# 3. Test changes
# 4. Commit with clear message
git add .
git commit -m "feat: add feature description"

# 5. Push to remote
git push -u origin feature/feature-name
```

### Fixing a Bug

```bash
# 1. Create fix branch
git checkout -b fix/bug-description

# 2. Identify and fix bug
# 3. Test fix
# 4. Commit
git commit -m "fix: resolve bug description"

# 5. Push
git push -u origin fix/bug-description
```

### Updating Documentation

```bash
# 1. Make documentation changes
# 2. Commit
git commit -m "docs: update documentation description"

# 3. Push
git push -u origin <current-branch>
```

### Exploring the Codebase

When asked to understand code structure:
1. Use Task tool with `subagent_type=Explore` for broad exploration
2. Use Glob for finding files by pattern
3. Use Grep for searching specific content
4. Use Read for examining specific files

---

## Project-Specific Guidelines

### Domain: Conjugation

*This section will be updated as project requirements become clear*

Potential areas of focus:
- Verb conjugation rules
- Language support
- Grammar patterns
- User interface
- API design
- Data structures

### Dependencies

*To be documented when dependencies are added*

### Configuration

*To be documented when configuration is established*

### Deployment

*To be documented when deployment strategy is defined*

---

## Notes for Future Updates

This CLAUDE.md file should be updated when:
- New dependencies are added
- Code structure changes significantly
- New conventions are established
- Testing framework is implemented
- Deployment process is defined
- New developers join the project

### Update Checklist

When updating this file:
- [ ] Update "Last Updated" date at the top
- [ ] Reflect current repository structure
- [ ] Update technology stack section
- [ ] Add new conventions or guidelines
- [ ] Update common tasks as needed
- [ ] Ensure all examples are current

---

## Questions or Clarifications

If you encounter situations not covered in this guide:
1. Check existing code for patterns
2. Ask the user for clarification
3. Document the decision in this file
4. Proceed with the most reasonable approach

---

**Remember:** The goal is to maintain a clean, secure, and maintainable codebase. When in doubt, choose simplicity and ask for clarification.
