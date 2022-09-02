# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


from interpreter import *


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    code = open('G-code/code2', 'r+', encoding='utf-8').read()
    lexer = Lexer(code)
    parser = Parser(lexer)
    tree = parser.parse()
    interpreter = Interpreter(tree)
    # semantic_analyzer = SemanticAnalyzer()
    # semantic_analyzer.visit(tree)
    interpreter.interpret()
    print(interpreter.MEMORY)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
