import unittest
from unittest.mock import Mock, patch

from dependify import dependencies
from dependify.dependencies import Dependencies

ROOT_DIR = "/home/user/projects/my_project"
PROJECT_NAME = "my_project"


class TestDependenciesInit(unittest.TestCase):
    def test_dependencies_init(self):
        dependencies = Dependencies(ROOT_DIR, PROJECT_NAME)

        assert dependencies.root_dir == ROOT_DIR
        assert dependencies.project_name == PROJECT_NAME


class TestGetDependencies(unittest.TestCase):
    def setup(self):
        self.dependencies = Dependencies(ROOT_DIR, PROJECT_NAME)

    @patch.object(dependencies, "find_python_files", autospec=True)
    @patch.object(dependencies.Dependencies, "_analyze_test_file")
    def test_get_test_dependencies(
        self, mock_analyze_test_file, mock_find_python_files
    ):
        dependencies = Dependencies(ROOT_DIR, PROJECT_NAME)

        mock_find_python_files.return_value = [
            "tests/test_utils.py",
            "tests/test_helpers.py",
        ]

        def side_effect(test_file, dependency_map):
            if test_file == "tests/test_utils.py":
                dependency_map[test_file] = ["src/utils.py"]
            elif test_file == "tests/test_helpers.py":
                dependency_map[test_file] = ["src/helpers.py"]

        mock_analyze_test_file.side_effect = side_effect

        result = dependencies.get_test_dependencies()

        assert result == {
            "tests/test_utils.py": ["src/utils.py"],
            "tests/test_helpers.py": ["src/helpers.py"],
        }


class TestGetInternalDependencies(unittest.TestCase):
    def setUp(self):
        self.dependencies = Dependencies(ROOT_DIR, PROJECT_NAME)

    @patch.object(dependencies, "parse_python_file", autospec=True)
    @patch.object(dependencies, "extract_imports", autospec=True)
    @patch.object(Dependencies, "_find_module_path")
    def test_get_internal_dependencies_with_dependencies(
        self, mock_find_module_path, mock_extract_imports, mock_parse_python_file
    ):
        mock_parse_python_file.return_value = Mock()
        mock_extract_imports.return_value = [
            "my_project.helpers",
            "my_project.constants",
        ]
        mock_find_module_path.side_effect = (
            lambda module: f"{ROOT_DIR}/src/{module.split('.')[-1]}.py"
        )

        result = self.dependencies._get_internal_dependencies("src/utils.py")

        assert result == {"src/helpers.py", "src/constants.py"}

    @patch.object(dependencies, "parse_python_file", autospec=True)
    @patch.object(dependencies, "extract_imports", autospec=True)
    def test_get_internal_dependencies_no_dependencies(
        self, mock_extract_imports, mock_parse_python_file
    ):
        mock_parse_python_file.return_value = Mock()  # Assume the file is parseable
        mock_extract_imports.return_value = []  # No imports

        result = self.dependencies._get_internal_dependencies("src/utils.py")

        assert result == set()

    @patch.object(dependencies, "parse_python_file", autospec=True)
    def test_get_internal_dependencies_unparseable_file(self, mock_parse_python_file):
        mock_parse_python_file.return_value = None  # File is not parseable

        result = self.dependencies._get_internal_dependencies("src/utils.py")

        assert result == set()
