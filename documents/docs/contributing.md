---
title: Contribution Guide
description: How to contribute code to the py-xiaozhi project
sidebar: false
outline: deep
---

<div class="contributing-page">

# Contribution Guidelines

<div class="header-content">
<h2>How to contribute code to the py-xiaozhi project 🚀</h2>
</div>

## Preface

Thank you for your interest in the py-xiaozhi project! We welcome contributions from community members, whether fixing bugs, improving documentation, or adding new features. This guide will help you understand how to submit contributions to the project.

## Development environment preparation

### Basic requirements

- Python 3.9 or higher
- Git version control system
- Basic Python development tools (Visual Studio Code is recommended)

### Get source code

1. First, Fork this project to your own account on GitHub
- Visit [py-xiaozhi project page](https://github.com/huangjunsen0406/py-xiaozhi)
- Click the "Fork" button in the upper right corner
- Wait for the Fork to complete and you will be redirected to your copy of the repository

2. Clone your forked repository locally:

```bash
git clone https://github.com/YOUR_USERNAME/py-xiaozhi.git
cd py-xiaozhi
```

3. Add the upstream repository as a remote source:

```bash
git remote add upstream https://github.com/huangjunsen0406/py-xiaozhi.git
```

You can use the `git remote -v` command to confirm that the remote repository is configured correctly:

```bash
git remote -v
# should display:
# origin    https://github.com/YOUR_USERNAME/py-xiaozhi.git (fetch)
# origin    https://github.com/YOUR_USERNAME/py-xiaozhi.git (push)
# upstream  https://github.com/huangjunsen0406/py-xiaozhi.git (fetch)
# upstream  https://github.com/huangjunsen0406/py-xiaozhi.git (push)
```

### Install development dependencies
- For other dependencies, please check the relevant documents under the guide
```bash
# Create and activate virtual environment (recommended)
python -m venv venv
source venv/bin/activate # On Windows use: venv\Scripts\activate

# Install project dependencies
pip install -r requirements.txt
```

## Development process

### Keep in sync with the main repository

Before starting work, it is very important to ensure that your local repository is in sync with the main project. Here are the steps to synchronize your local repository:

1. Switch to your master branch (`main`):

```bash
git checkout main
```

2. Pull the latest changes from the upstream warehouse:

```bash
git fetch upstream
```

3. Merge the changes from the upstream master branch into your local master branch:

```bash
git merge upstream/main
```

4. Push the updated local master branch to your GitHub repository:

```bash
git push origin main
```

### Create a branch

Before starting any work, make sure to create a new branch from the latest upstream master branch:

```bash
# Get the latest upstream code (as described in the previous section)
git fetch upstream
git checkout -b feature/your-feature-name upstream/main
```

When naming your branches, you can follow the following conventions:
- `feature/xxx`: new feature development
- `fix/xxx`: fix bug
- `docs/xxx`: Documentation update
- `test/xxx`: Test related work
- `refactor/xxx`: code refactoring

### Coding specifications

We use [PEP 8](https://www.python.org/dev/peps/pep-0008/) as the style guide for Python coding. Before submitting your code, please make sure your code meets the following requirements:

- Use 4 spaces for indentation
- Line length must not exceed 120 characters
- Use meaningful variable and function names
- Add docstrings for public APIs
- Use Type Hints

We recommend using static code analysis tools to help you follow coding conventions:

```bash
# Use flake8 to check code style
flake8 .

# Use mypy for type checking
mypy .
```

### test

Before submitting, make sure all tests pass

## Submit changes

### Pre-submission checklist

Before submitting your code, make sure to complete the following checks:

1. Whether the code complies with PEP 8 specifications
2. Whether necessary test cases have been added
3. Whether all tests pass
4. Whether appropriate documentation has been added
5. Does it solve the problem you planned to solve?
6. Whether it is synchronized with the latest upstream code

### Submit changes

During the development process, develop the habit of submitting in small batches and frequently. This makes your changes easier to track and understand:

```bash
# View changed files
git status

#Stage changes
git add file1.py file2.py

# Submit changes
git commit -m "feat: add new feature X"
```

### Resolve conflicts

If you encounter conflicts while trying to merge upstream changes, follow these steps to resolve them:

1. First understand the location of the conflict:

```bash
git status
```

2. Open the conflict file and you will see a mark similar to the following:

```
<<<<<<< HEAD
your code
=======
upstream code
>>>>>>> upstream/main
```

3. Modify the file to resolve the conflict and remove the conflict mark
4. After resolving all conflicts, temporarily save and submit:

```bash
git add .
git commit -m "fix: resolve merge conflicts"
```

### Submission specifications

We use the [conventionalcommits](https://www.conventionalcommits.org/zh-hans/) specification to format Git commit messages. Commit messages should follow the following format:

```
<type>[optional scope]: <description>

[optional text]

[optional footnote]
```

Common submission types include:
- `feat`: new function
- `fix`: bug fix
- `docs`: Documentation changes
- `style`: changes that do not affect the meaning of the code (such as spaces, formatting, etc.)
- `refactor`: code refactoring that neither fixes bugs nor adds functionality
- `perf`: code changes to improve performance
- `test`: add or fix tests
- `chore`: changes to the build process or auxiliary tools and libraries

For example:

```
feat(tts): Add new speech synthesis engine support

Add support for Baidu speech synthesis API, including the following features:
-Supports multiple tone selections
-Supports speaking speed and volume adjustment
- Supports mixed synthesis of Chinese and English

Fix #123
```

### Push changes

Once you've completed your code changes, push your branch to your GitHub repository:

```bash
git push origin feature/your-feature-name
```

If you have already created a Pull Request and need to update it, just push to the same branch again:

```bash
# After making more changes
git add .
git commit -m "refactor: improve code based on feedback"
git push origin feature/your-feature-name
```

### Synchronize the latest code before creating a Pull Request

Before creating a Pull Request, it is recommended to synchronize with the upstream repository again to avoid potential conflicts:

```bash
# Get the latest upstream code
git fetch upstream

# Rebase the latest upstream code to your feature branch
git rebase upstream/main

# If conflicts arise, resolve them and continue rebasing
git add .
git rebase --continue

# Force push the updated branch to your repository
git push --force-with-lease origin feature/your-feature-name
```

Note: Using `--force-with-lease` is safer than using `--force` directly and prevents overwriting changes pushed by others.

### Create Pull Request

When you have completed feature development or bug fixing, follow these steps to create a Pull Request:

1. Push your changes to GitHub:

```bash
git push origin feature/your-feature-name
```

2. Visit the repository page of your fork on GitHub and click the "Compare & pull request" button

3. Fill out the Pull Request form:
- Use clear titles and follow commit message format
- Provide details in the description
- Quote related issues (using `#issue number` format)
- If this is a work in progress, please add the `[WIP]` prefix to the title

4. Submit a Pull Request and wait for review by the project maintainer

### Life cycle of Pull Request

1. **Create**: Submit your PR
2. **CI Check**: Automated testing and code style checking
3. **Code Review**: Maintainers will review your code and provide feedback
4. **Revision**: Modify your code based on feedback
5. **Approval**: Once your PR is approved
6. **Merge**: The maintainer will merge your PR into the master branch

## Documentation contribution

If you want to improve your project documentation, follow these steps:

1. Follow the above steps to Fork the project and clone it locally

2. The document is located in the `documents/docs` directory and uses Markdown format

3. Install document development dependencies:

```bash
cd documents
pnpm install
```

4. Start the local document server:

```bash
pnpm docs:dev
```

5. Visit `http://localhost:5173/py-xiaozhi/` in your browser to preview your changes

6. Once you have completed your changes, submit your contribution and create a Pull Request

### Document writing guidelines

- Use clear, concise language
- Provide practical examples
- Detailed explanation of complex concepts
- Include appropriate screenshots or diagrams (where required)
- Avoid too many technical terms and provide explanations when necessary
- Keep document structure consistent

## Problem feedback

If you find an issue but cannot fix it temporarily, please [create an Issue](https://github.com/huangjunsen0406/py-xiaozhi/issues/new) on GitHub. When creating an Issue, please include the following information:

- Detailed description of the problem
- Steps to reproduce the problem
- expected behavior and actual behavior
- Your operating system and Python version
- Relevant log output or error messages

## Code review

After submitting your Pull Request, your code will be reviewed by the project maintainers. During the code review process:

- Please be patient and wait for feedback
- Respond promptly to comments and suggestions
- Modify and update your Pull Request if necessary
- Keep discussions polite and constructive

### Handle code review feedback

1. Read all comments and suggestions carefully
2. Respond to or change each point
3. If you disagree with a suggestion, politely explain your reasons
4. After the modification is completed, leave a message in the PR to notify the reviewer.

## Become a project maintainer

If you continue to make valuable contributions to the project, you may be invited to become a maintainer of the project. As a maintainer, you will have permission to review and merge other people's Pull Requests.

### Responsibilities of Maintainers

- Review Pull Request
- Manage issues
- Participate in project planning
- Answer community questions
- Help onboard new contributors

## Code of Conduct

Please respect all project participants and follow the following code of conduct:

- Use inclusive language
- Respect different perspectives and experiences
- Accept constructive criticism gracefully
- Look out for the best interests of the community
- Show empathy towards other community members

## FAQ

### Where should I start contributing?

1. View issues marked "good first issue"
2. Fix errors or unclear parts of the document
3. Add more test cases
4. Solve the problems you find during use

### There has been no response to the PR I submitted for a long time, what should I do?

Leave a PR in the PR and politely ask if further improvements or clarifications are needed. Please understand that maintainers may be busy and need some time to review your contributions.

### What types of changes can I contribute?

- Bug fixes
- new features
- Performance improvements
- Documentation updates
- test cases
- Code refactoring

## Acknowledgments

Thanks again for contributing to the project! Your participation is very important to us, and we work together to make py-xiaozhi better!

</div>

<style>
.contributing-page {
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem 1.5rem;
}

.contributing-page h1 {
  text-align: center;
  margin-bottom: 1rem;
}

.header-content {
  text-align: center;
}

.header-content h2 {
  color: var(--vp-c-brand);
  margin-bottom: 1rem;
}

.contributing-page h2 {
  margin-top: 3rem;
  padding-top: 1rem;
  border-top: 1px solid var(--vp-c-divider);
}

.contributing-page h3 {
  margin-top: 2rem;
}

.contributing-page code {
  background-color: var(--vp-c-bg-soft);
  padding: 0.2em 0.4em;
  border-radius: 3px;
}

.contributing-page pre {
  margin: 1rem 0;
  border-radius: 8px;
  overflow: auto;
}
</style> 