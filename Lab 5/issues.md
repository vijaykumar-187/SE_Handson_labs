# Lab 5: Static Code Analysis — Issues and Fixes

The original `vehicle_service.py` was analyzed using Pylint, Bandit, and Flake8.

## Issues identified

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| Weak MD5 hash | Security — High | 39 | Bandit B324 identified the use of MD5, which is unsuitable for security-sensitive hashing. | Replaced MD5 with SHA-256 for job card ID generation. |
| Shell command execution | Security — High | 61 | Bandit B602 flagged `subprocess.call()` with `shell=True`, which can introduce command-injection risks. | Removed shell-based copying and used `shutil.copy2()` instead. |
| Hardcoded password | Security — Low | 8 | Bandit B105 flagged the hardcoded value `garage-demo`. | Removed the hardcoded administrator password from the source code. |
| Unnecessary subprocess import | Security — Low | 3 | Bandit B404 flagged the use of the subprocess module. | Removed the subprocess import after replacing the shell-based backup operation. |
| Mutable default argument | Code quality | 12 | Pylint W0102 identified a list used as a default function argument, which could be shared across calls. | Used a `None` default and initialized a new list when required. |
| Broad exception handling | Code quality | 23 | Pylint W0718 flagged catching the general `Exception` class. | Narrowed the exception handling to the expected `KeyError`. |
| Missing file encoding | Reliability | 50 | Pylint W1514 reported that `open()` did not specify an encoding. | Specified an explicit encoding when opening files. |
| Missing documentation | Maintainability | Multiple | Pylint reported missing module and function docstrings. | Added module and function docstrings. |
| Non-standard naming | Style | Multiple | Pylint flagged camelCase function names, arguments, and variables. | Renamed identifiers to use snake_case. |
| Formatting violations | Style | 7, 43, 49, 77 | Flake8 reported missing whitespace, incorrect blank lines, and a line exceeding 79 characters. | Corrected spacing, blank lines, and line length. |

## Results

- Initial Pylint score: 4.66/10.
- Final Pylint score: 10.00/10.
- Initial Bandit findings: 2 high-severity and 2 low-severity findings.
- Final Bandit result: No issues identified.
- Initial Flake8 findings: 4 style violations.
- Final Flake8 result: No violations reported.

The findings above are based on the saved initial analysis reports. Line numbers refer to the original source file and may differ in the cleaned version.
