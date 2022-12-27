# Static-Code-Analyser
Practicing ASTs and regex in python


# Usage

```shell
python code_analyzer.py project_folder

```

## Sample output
```shell
> python code_analyzer.py test_project
test_project\test_1.py: Line 1: S004 At least two spaces required before inline comments
test_project\test_1.py: Line 2: S003 Unnecessary semicolon
test_project\test_1.py: Line 3: S001 Too long
test_project\test_1.py: Line 3: S003 Unnecessary semicolon
test_project\test_1.py: Line 6: S001 Too long
test_project\test_1.py: Line 11: S006 More than two blank lines used before this line
test_project\test_1.py: Line 13: S003 Unnecessary semicolon
test_project\test_1.py: Line 13: S004 At least two spaces required before inline comments
test_project\test_1.py: Line 13: S005 TODO found
test_project\test_2.py: Line 1: S007 Too many spaces after 'class'
test_project\test_2.py: Line 4: S008 Class name 'user' should use CamelCase
test_project\test_2.py: Line 14: S009 Function name 'Print2' should use snake_case
test_project\test_3.py: Line 9: S012 Default argument value is mutable
test_project\test_4.py: Line 2: S010 Argument name 'Beta' should use snake_case
test_project\test_5.py: Line 3: S011 Variable 'Beta' in function should use snake_case
test_project\test_5.py: Line 9: S011 Variable 'Variable' in function should use snake_case
```