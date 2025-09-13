<!-- contribution.md -->

# Contributing Guidelines

## How to Contribute

1. Fork and clone the repo from <https://github.com/Miras3210/codejam-laudatory-larkspurs>.
2. Make some changes to the source code.
3. Run code checks to make sure nothing breaks.
4. Push your changes and open a pull request.

## Code Checks

Use `ruff check` to check your code style and fix it.

```shell
ruff check .
ruff check . --fix
```

Use `pre-commit` to run linting before committing.

> [!NOTE]
> `pre-commit install` to install.

### Examples

```shell
pre-commit run --show-diff-on-failure --all-files
pre-commit run ruff-check --all-files
pre-commit run check-toml --all-files
```

**Pre-commit hooks:**

- `check-toml`: Lints and corrects your TOML files.
- `check-yaml`: Lints and corrects your YAML files.
- `end-of-file-fixer`: Makes sure you always have an empty line at the end of your file.
- `trailing-whitespace`: Removes whitespaces at the end of each line.
- `ruff-check`: Runs the Ruff linter.
- `ruff-format`: Runs the Ruff formatter.

## Rules

1. Comment your classes, functions, and non-obvious logic.
2. Use docstrings with author tags and short descriptions.

```py
class ClassName:
    '''Handle user input and validation.

    @author Mira
    '''
    ...

# Short function description
def do_something():
    '''Perform a single-step operation.

    :param paramname: does something
    :return: None

    @author Mira
    '''
    ...
```

## Naming Conventions

### Variables and Functions

All variables and functions use lowercase naming with underscores.

```py
def my_function():
    my_variable = "value"
```

### Classes and Type Aliases

Classes use the PascalCase naming convention.

```py
from typing import List

class MyClass:
    pass

ListOfMyClass = List[MyClass]
```

### Constants

Constants use the SCREAMING_SNAKE_CASE naming convention.

```py
MY_CONSTANT = 1
```

### Operators

Place operators at the start of a newline.

```py
# No
result = (
    1 +
    2 *
    3
)
# Yes
result = (
    1
    + 2
    * 3
)
```

### Equivalent to `None`

Use `is` or `is not` instead of `==`.

```py
if variable == None: # No
    print("Variable is None")
if variable is None: # Yes
    print("Variable is None")¨
```

### `not` positioning

```py
if not variable is None: # No
    print("Variable is not None")

if variable is not None: # Yes, easier to read
    print("Variable is not None")
```

### **Imports**

Do not import multiple modules on one line or everything from a module (`*`)

```py
# No
import pathlib, os
from pathlib import *

# Yes
import os
import pathlib
from pathlib import Path
```

## Contributors

<a href="https://github.com/Miras3210/codejam-laudatory-larkspurs/graphs/contributors"><img src="https://camo.githubusercontent.com/14f13a19c08fa212bdd5e2bc5cae2c35df4450011e2996efc0a2377f8cecf030/68747470733a2f2f636f6e747269622e726f636b732f696d6167653f7265706f3d4d69726173333231302f636f64656a616d2d6c61756461746f72792d6c61726b7370757273" alt="Contributors" data-canonical-src="https://contrib.rocks/image?repo=Miras3210/codejam-laudatory-larkspurs" style="max-width: 100%;"></a>

### Mira

**Team Leader**

<https://github.com/Miras3210>

- Python image editing and handling
- Some of commands listed in [/commands](commands.md)
- bugfixing pyodide's filesystem
  - handling image files

### Philip

<https://github.com/Osiris32-and-a-half>

- Command parser/environment and command framework
- Written/maintained a Majority of the commands listed in [/commands](commands.md) as the system evolved
  - notable ones being help and bg/fg
- Came up with the initial idea. (which then got misinterpreted twice)

### Ricky

<https://github.com/silladgey>

- Implemented functionality for image file upload through a drag and drop interface
- Created components for image display manager and GUI preview
- Simple RGB color information extraction and display feature
- Integrated Docker for containerized development
- Set up continuous deployment using GitHub Actions workflows

### Jont

<https://github.com/jon-edward>

- Developed core GUI microframework
- Created build script and initial HTML structure with Pyodide integration
- Implemented the terminal UI

### Julien

<https://github.com/Jujulien45>

- app layout design
- help with gui
- new feature ideas
- testing
