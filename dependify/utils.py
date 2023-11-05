from ast import AST
from ast import Import as ast_Import
from ast import ImportFrom as ast_ImportFrom
from ast import parse
from ast import walk as ast_walk
from logging import getLogger
from os import walk as os_walk
from os.path import join
from typing import List, Optional

logging = getLogger(__name__)


def find_python_files(root_dir: str) -> List[str]:
    """Recursively find Python files in subdirectories."""
    python_files = []
    logging.info(f"Finding Python files in {root_dir}...")
    for dirpath, _, filenames in os_walk(root_dir):
        python_files.extend(
            join(dirpath, filename)
            for filename in filenames
            if filename.endswith(".py")
        )
    return python_files


def parse_python_file(file_path: str) -> Optional[AST]:
    """Parse a Python file and return its AST, or None if it couldn't be parsed."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            source_code = f.read()
        return parse(source_code)
    except SyntaxError as e:
        logging.info(f"SyntaxError in {file_path}: {e}")
    except Exception as e:
        logging.info(f"Failed to parse {file_path}: {e}")
    return None


def extract_imports(tree: AST) -> List[str]:
    """
    Extract imports from the AST of a file.

    Args:
        tree (ast.AST): The AST of a Python file.
            Examples:
                parse("import os")
                parse("from ast import List, Optional")
                parse("from logging import getLogger as get_logger")

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
        for node in ast_walk(tree)
        if isinstance(node, ast_Import)
        for alias in node.names
    ] + [
        (node.module + "." + alias.name if node.module else alias.name)
        for node in ast_walk(tree)
        if isinstance(node, ast_ImportFrom)
        for alias in node.names
    ]
    for import_name in imports:
        logging.info(f"Import found: {import_name}")
    return imports
