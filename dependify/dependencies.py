import os
from logging import getLogger
from typing import Dict, List, Set

from dependify.utils import extract_imports, find_python_files, parse_python_file

logging = getLogger(__name__)


class Dependencies:
    def __init__(self, root_dir: str, project_name: str):
        """
        Initialize a Dependencies instance.

        Args:
            root_dir (str): Root directory of the project.
                Example: "/home/user/projects/my_project"
            project_name (str): Name of the project or
                folder to consider for internal modules.
                Example: "my_project"
        """
        self.root_dir = root_dir
        self.project_name = project_name

    def get_test_dependencies(self) -> Dict[str, List[str]]:
        """
        Get the dependency graph of the test files in the specified project.

        Returns:
            Dict[str, List[str]]: Map of test files to lists of dependencies.
                Example: {"tests/test_utils.py": ["src/utils.py", "src/helpers.py"]}
        """
        logging.info("Getting dependencies...")
        test_files = find_python_files(os.path.join(self.root_dir, "tests"))
        dependency_map = {}
        logging.info(f"Found {len(test_files)} test files.")
        for test_file in test_files:
            logging.info("Analyzing test file: {test_file}")
            self._analyze_test_file(test_file, dependency_map)
        logging.info("Done.")
        return {k: list(v) for k, v in dependency_map.items()}

    def _get_internal_dependencies(self, module_file: str) -> Set[str]:
        """
        Get the internal dependencies of a specified module file.

        Args:
            module_file (str): Path to the module file.
                Example: "src/utils.py"

        Returns:
            Set[str]: Set of relative paths to internal dependencies.
                Example: {"src/helpers.py", "src/constants.py"}
                (The utils module imports helpers and constants.)
        """
        logging.info(f"Processing module file: {module_file}")
        tree = parse_python_file(module_file)
        if tree is None:
            logging.info(f"Could not parse file: {module_file}")
            return set()

        imports = extract_imports(tree)
        internal_dependencies = set()
        for module in imports:
            module_path = self._find_module_path(module)
            if module_path:
                relative_path = os.path.relpath(module_path, start=self.root_dir)
                internal_dependencies.add(relative_path)
                logging.info(f"Internal dependency found: {relative_path}")
            else:
                logging.info(f"No internal dependency resolved for: {module}")

        return internal_dependencies

    def _analyze_test_file(
        self, test_file: str, dependency_map: Dict[str, Set[str]]
    ) -> None:
        """
        Analyze a test file to find dependencies and update the dependency map.

        Args:
            test_file (str): Path to the test file.
                Example: "tests/test_utils.py"
            dependency_map (Dict[str, Set[str]]): Map to store dependencies.
        """
        seen_files = set()
        self._find_dependencies(test_file, seen_files, dependency_map)

    def _find_dependencies(
        self,
        module_file: str,
        seen_files: Set[str],
        dependency_map: Dict[str, Set[str]],
    ) -> None:
        """
        Recursively find dependencies for a given module file.

        Args:
            module_file (str): Path to the module file.
            seen_files (Set[str]): Set to keep track of already processed files
                and detect circular dependencies.
            dependency_map (Dict[str, Set[str]]): Map to store dependencies.
        """
        if module_file in seen_files:  # Handle circular dependencies
            logging.warning(f"Circular dependency detected: {module_file}")
            return
        seen_files.add(module_file)

        internal_dependencies = self._get_internal_dependencies(module_file)
        for internal_module in internal_dependencies:
            self._find_dependencies(internal_module, seen_files, dependency_map)

        if module_file in dependency_map:
            dependency_map[module_file].update(internal_dependencies)
        else:
            dependency_map[module_file] = internal_dependencies

    def _find_module_path(self, module_name: str) -> str:
        """
        Resolve the file path for a given module name within the root directory.

        Args:
            module_name (str): Name of the module to resolve.
                Example: "utils"

        Returns:
            str: Path to the module, or None if not found.
                Example: "/home/user/projects/my_project/src/utils.py"
        """
        if not module_name.startswith(f"{self.project_name}."):
            logging.info(f"Skipping external module: {module_name}")
            return None

        module_parts = module_name.split(".")
        for i in range(len(module_parts), 0, -1):
            current_module_parts = module_parts[:i]
            potential_paths = [
                os.path.join(self.root_dir, *current_module_parts) + ".py",
                os.path.join(self.root_dir, *current_module_parts, "__init__.py"),
            ]

            for path in potential_paths:
                if os.path.exists(path):
                    logging.info(
                        f"Module '{'.'.join(current_module_parts)}' "
                        f"resolved to path: {path}"
                    )
                    return path

        logging.info(
            f"Failed to resolve module path for '{module_name}'."
            f"Potential paths checked: {potential_paths}"
        )
        return None
