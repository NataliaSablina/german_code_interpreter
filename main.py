# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


from interpreter import *


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    code = open('G-code/code1', 'r+').read()
    lexer = Lexer(code)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    interpreter.interpret()
    print(interpreter.MEMORY)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
