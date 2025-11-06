# py-xiaozhi documentation

This is the documentation website for the py-xiaozhi project, built on VitePress.

## Function

- Project Guide: Provide detailed usage instructions and development documents for the project
- Sponsor page: showcase and thank all sponsors of the project
- Contribution Guide: explains how to contribute code to the project
- Contributors list: Shows all developers who have contributed to the project
- Responsive design: adapts to desktop and mobile devices

## Local development

```bash
# Install dependencies
pnpm install

# Start development server
pnpm docs:dev

# Build static files
pnpm docs:build

# Preview build results
pnpm docs:preview
```

## Directory structure

```
documents/
├── docs/ # Document source file
│ ├── .vitepress/ # VitePress configuration
│ ├── guide/ # guide document
│ ├── sponsors/ # Sponsor page
│ ├── contributing.md # Contribution Guide
│ ├── contributors.md # Contributors list
│ └── index.md # Home page
├── package.json #Project configuration
└── README.md # Project description
```

## Sponsor Page

Sponsor pages are implemented in the following ways:

1. `/sponsors/` 目录包含了赞助商相关的内容
2. `data.json` file stores sponsor data
3. Use Vue components to dynamically render the sponsor list on the client side
4. Provide detailed instructions and payment methods for becoming a sponsor

## Contribution Guidelines

The Contribution Guidelines page provides the following:

1. Development environment preparation guide
2. Code contribution process description
3. Coding specifications and submission specifications
4. Pull Request creation and review process
5. Document Contribution Guidelines

## List of contributors

The contributor list page displays all developers who have contributed to the project, including:

1. Core development team members
2. Code contributors
3. Documentation contributors
4. Testing and feedback providers

## Deployment

Documentation sites are automatically deployed to GitHub Pages via GitHub Actions.