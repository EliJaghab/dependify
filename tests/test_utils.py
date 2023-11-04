import ast
from unittest.mock import mock_open, patch

from dependify.utils import extract_imports, find_python_files, parse_python_file


class TestFindPythonFiles:
    @patch("os.walk")
    def test_find_python_files(self, mock_walk):
        mock_walk.return_value = [
            ("/some/dir", ("subdir1", "subdir2"), ("file1.py", "file2.txt")),
            ("/some/dir/subdir1", (), ("file3.py", "file4.py")),
        ]

        result = find_python_files("/some/dir")

        expected_result = [
            "/some/dir/file1.py",
            "/some/dir/subdir1/file3.py",
            "/some/dir/subdir1/file4.py",
        ]
        assert result == expected_result


class TestParsePythonFile:
    @patch(
        "builtins.open",
        new_callable=lambda: mock_open(read_data="invalid python code")(),
    )
    def test_parse_python_file_syntax_error(self, mock_file):
        result = parse_python_file("some_file_path.py")
        assert result is None

    @patch("builtins.open")
    def test_parse_python_file_exception(self, mock_file):
        def side_effect(*args, **kwargs):
            raise Exception("Some error")

        mock_file.side_effect = side_effect

        result = parse_python_file("some_file_path.py")
        assert result is None


def test_extract_imports():
    test_file_content = (
        "import os\n"
        "from typing import List, Optional\n"
        "from logging import getLogger\n"
    )
    tree = ast.parse(test_file_content)
    imports = extract_imports(tree)
    assert isinstance(imports, list), f"Expected list, got {type(imports)}"
    assert "os" in imports, "Expected 'os' in imports"
    assert "typing.List" in imports, "Expected 'typing.List' in imports"
    assert "typing.Optional" in imports, "Expected 'typing.Optional' in imports"
    assert "logging.getLogger" in imports, "Expected 'logging.getLogger' in imports"
