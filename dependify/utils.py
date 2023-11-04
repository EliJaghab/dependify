import ast
import os
from logging import getLogger
from typing import List, Optional

logging = getLogger(__name__)


def find_python_files(root_dir: str) -> List[str]:
    """Recursively find Python files in subdirectories."""
    python_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        python_files.extend(
            os.path.join(dirpath, filename)
            for filename in filenames
            if filename.endswith(".py")
        )
    return python_files


def parse_python_file(file_path: str) -> Optional[ast.AST]:
    """Parse a Python file and return its AST, or None if it couldn't be parsed."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            source_code = f.read()
        return ast.parse(source_code)
    except SyntaxError as e:
        logging.info(f"SyntaxError in {file_path}: {e}")
    except Exception as e:
        logging.error(f"Failed to parse {file_path}: {e}")
    return None


def extract_imports(tree: ast.AST) -> List[str]:
    """
    Extract imports from the AST of a file.

    Args:
        tree (ast.AST): The AST of a Python file.
            Examples:
                ast.parse("import os")
                ast.parse("from ast import List, Optional")
                ast.parse("from logging import getLogger as get_logger")

    Returns:
        List[str]: A list of strings representing the imported modules.
            Examples:
                ['os']
                ['ast.List', 'ast.Optional']
                ['logging.getLogger']
    """
    logging.info("Extracting imports...")
    imports = [
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    ] + [
        (node.module + "." + alias.name if node.module else alias.name)
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom)
        for alias in node.names
    ]
    for import_name in imports:
        logging.info(f"Import found: {import_name}")
    return imports
