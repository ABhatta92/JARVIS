# tool_registry.py

from tools.filesystem import (
    read_file,
    write_file,
    list_files,
    delete_file,
    file_exists,
    make_directory
)

# from tools.data import (
    # load_data,
    # save_data,
# )

from tools.python_runner import (
    run_python,
)

TOOLS = [
    read_file,
    write_file,
    list_files,
    delete_file,
    file_exists,
    make_directory,
    # load_data,
    # save_data,
    run_python,
]