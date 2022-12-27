import re
import ast


class LineAnalyser:
    def __init__(self, line_num, line_content, path):
        self.line_num = line_num
        self.line_content = line_content
        self.path = path

    def analyse(self, content_list):
        errors = [
            self.line_length(),
            self.line_has_semicolon(),
            self.blank_lines(content_list),
            self.line_comment_spaces(),
            self.line_indentation_multiple_of_4(),
            self.line_def_class_spaces(),
            self.line_has_todo(),
        ]
        return list(filter(lambda x: x is not None, errors))

    def line_length(self):
        if len(self.line_content) > 79:
            return "{}: Line {}: S001 Too long".format(self.path, self.line_num)

    def line_has_semicolon(self):
        regexp = '(.*;).*'
        match = re.match(regexp, self.line_content)
        if match and not re.findall("(.*;).*'", match.string) and len(re.findall('#.*;', match.string)) == 0:
            return "{}: Line {}: S003 Unnecessary semicolon".format(self.path, self.line_num)

    def line_has_todo(self):
        match = re.findall(r"#.*(Todo)", self.line_content, flags=re.I)
        if match:
            return "{}: Line {}: S005 TODO found".format(self.path, self.line_num)

    def line_comment_spaces(self):
        regexp = '(.*#).*'
        match = re.match(regexp, self.line_content)
        if match:
            before = match.string.split("#").pop(0)
            if len(before) == 0:
                return
            count = 0
            for char in before[::-1]:
                if re.match('( )', char):
                    count += 1
                else:
                    break
            # print(line_num, count)
            if count < 2:
                return "{}: Line {}: S004 At least two spaces required before inline comments".format(self.path,
                                                                                                      self.line_num)

    def line_indentation_multiple_of_4(self):
        if self.line_content != '\n' and (len(self.line_content) - len(self.line_content.lstrip())) % 4:
            return "{}: Line {}: S002 Indentation is not a multiple of four".format(self.path, self.line_num)

    def blank_lines(self, content_list):
        limit = 2
        blanks = 0
        for curr_line in reversed(content_list[:self.line_num - 1]):
            if curr_line == '\n':
                blanks += 1
            else:
                break
        if blanks > limit:
            return "{}: Line {}: S006 More than two blank lines used before this line".format(self.path, self.line_num)

    def line_def_class_spaces(self):
        regexp = r'\s*(class|def) {2,}'
        match = re.match(regexp, self.line_content)
        if match:
            element = "class"
            if "def " in self.line_content:
                element = "def"

            return "{}: Line {}: S007 Too many spaces after '{}'".format(self.path, self.line_num, element)


class AstAnalyser:
    def __init__(self, content, path):
        self.content = content
        self.path = path

    def analyse(self):
        errors = list()
        try:
            tree = ast.parse(self.content)
            for n in ast.walk(tree):
                if isinstance(n, ast.ClassDef):
                    errors.append(self.line_class_camel_case(n.name, n.lineno))
                elif isinstance(n, ast.FunctionDef):
                    errors.append(self.line_function_snake_case(n.name, n.lineno))
                    args = [a.arg for a in n.args.args]
                    for arg in args:
                        errors.append(self.line_function_arg_snake_case(arg, n.lineno))
                    errors.extend(self.line_function_variable_snake_case(n))
                    for def_arg in n.args.defaults:
                        errors.append(self.line_function_default_arg_mutable(def_arg))
        except IndentationError:
            pass
        return list(filter(lambda x: x is not None, errors))

    def line_class_camel_case(self, name, lineno):
        regexp = r'([a-z]+|\w*_+.*)'
        match = re.match(regexp, name)
        # print('MATCH', match)
        if match:
            return "{}: Line {}: S008 Class name '{}' should use CamelCase". \
                format(self.path, lineno, name)

    def line_function_snake_case(self, name, lineno):
        regexp = r'[A-Z]+.*'
        match = re.match(regexp, name)
        if match:
            return "{}: Line {}: S009 Function name '{}' should use snake_case". \
                format(self.path, lineno, name)

    def line_function_arg_snake_case(self, name, lineno):
        regexp = r'[A-Z]+.*'
        match = re.match(regexp, name)
        if match:
            return "{}: Line {}: S010 Argument name '{}' should use snake_case". \
                format(self.path, lineno, name)

    def line_function_variable_snake_case(self, node):
        errors = []
        regexp = r'[A-Z]+.*'
        for b in node.body:
            if isinstance(b, ast.Assign):
                for target in b.targets:
                    if isinstance(target, ast.Name):
                        match = re.match(regexp, target.id)
                        if match:
                            errors.append("{}: Line {}: S011 Variable '{}' in function should use snake_case".
                                          format(self.path, target.lineno, target.id))

        return errors

    def line_function_default_arg_mutable(self, node):

        if not isinstance(node, ast.Constant):
            return "{}: Line {}: S012 Default argument value is mutable".\
                          format(self.path, node.lineno)


