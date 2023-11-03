# Dependify

Dependify is a Python library designed to analyze and identify the libraries used in your test files. It leverages the power of Python's Abstract Syntax Tree (AST) to parse source files, extract import statements, and build a comprehensive map of dependencies. This enables a clear understanding of which libraries are crucial for your tests, and can be particularly useful in larger projects or in dynamic teams where dependencies may change over time.

## Features

- **Dependency Analysis:** Identify and list all the libraries that your test files depend on.
- **Import Extraction:** Extract all import statements from your Python files.
- **Recursive Tracing:** Recursively trace internal dependencies to ensure a thorough analysis.
- **Dependency Mapping:** Build a map of dependencies to visualize the dependency landscape of your project.

## Installation

```bash
pip install dependify
