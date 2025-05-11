import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QPushButton, QVBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import time


class Interpreter:
    def __init__(self):
        self.env = {}
        self.output = ""

    def evaluate(self, code, env=None):
        if env is None:
            env = self.env
        try:
            lines = code.split('\n')
            i = 0
            while i < len(lines):
                line = lines[i].strip()
                if not line:
                    i += 1
                    continue

                if line.startswith("num"):
                    parts = line[4:].split("=")
                    var_name = parts[0].strip()
                    expr = parts[1].strip()
                    env[var_name] = eval(expr, {}, env)

                elif line.startswith("write"):
                    expr = line[6:].strip()
                    result = eval(expr, {}, env)
                    self.output += str(result) + "\n"

                elif line.startswith("if"):
                    condition = line[2:].strip().rstrip(":")
                    block = []
                    i += 1
                    while i < len(lines) and not lines[i].strip().startswith("else") and not lines[i].strip().startswith("end"):
                        block.append(lines[i])
                        i += 1
                    if eval(condition, {}, env):
                        self.evaluate("\n".join(block), env)

                    if i < len(lines) and lines[i].strip().startswith("else"):
                        else_block = []
                        i += 1
                        while i < len(lines) and not lines[i].strip().startswith("end"):
                            else_block.append(lines[i])
                            i += 1
                        if not eval(condition, {}, env):
                            self.evaluate("\n".join(else_block), env)

                elif line.startswith("while"):
                    condition = line[5:].strip().rstrip(":")
                    loop_block = []
                    i += 1
                    while i < len(lines) and not lines[i].strip().startswith("end"):
                        loop_block.append(lines[i])
                        i += 1
                    while eval(condition, {}, env):
                        self.evaluate("\n".join(loop_block), env)

                elif line.startswith("for"):
                    header = line[3:].strip().rstrip(":")
                    var_name, range_part = header.split("=")
                    var_name = var_name.strip()
                    start, end = map(int, range_part.strip().split("to"))
                    loop_block = []
                    i += 1
                    while i < len(lines) and not lines[i].strip().startswith("end"):
                        loop_block.append(lines[i])
                        i += 1
                    for x in range(start, end):
                        env[var_name] = x
                        self.evaluate("\n".join(loop_block), env)

                i += 1
            return self.output
        except Exception as e:
            return f"Error: {e}"


class CompilerUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bhuvan'S Own Compiler")
        self.setGeometry(100, 100, 900, 600)
        self.setStyleSheet("""
            background-color: #2e2e2e;
            color: #dcdcdc;
            border: none;
        """)

        self.layout = QVBoxLayout()

        # Code input without line numbers
        self.code_input = QTextEdit()
        self.code_input.setFont(QFont("Fira Code", 12))
        self.code_input.setPlaceholderText("Write your code here...")
        self.code_input.setStyleSheet("""
            background-color: #1e1e1e; 
            color: #dcdcdc; 
            border: 1px solid #444444; 
            padding: 10px;
            selection-background-color: #264f78;
            selection-color: #ffffff;
        """)

        # Compile button
        self.compile_button = QPushButton("Compile")
        self.compile_button.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            background-color: #007acc;
            color: white;
            padding: 10px;
            border-radius: 5px;
            border: none;
        """)
        self.compile_button.clicked.connect(self.compile_code)

        # Output display
        self.output_display = QTextEdit()
        self.output_display.setReadOnly(True)
        self.output_display.setPlaceholderText("Output...")
        self.output_display.setStyleSheet("""
            background-color: #1e1e1e;
            color: #dcdcdc;
            border: 1px solid #444444;
            padding: 10px;
            selection-background-color: #264f78;
            selection-color: #ffffff;
        """)

        # Add widgets to layout
        self.layout.addWidget(self.code_input)
        self.layout.addWidget(self.compile_button)
        self.layout.addWidget(self.output_display)
        self.setLayout(self.layout)

    def compile_code(self):
        self.compile_button.setEnabled(False)
        code = self.code_input.toPlainText()
        interpreter = Interpreter()
        self.output_display.setText("Compiling...\nPlease wait.")
        time.sleep(1)
        output = interpreter.evaluate(code)
        self.output_display.setText(output)
        self.compile_button.setEnabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CompilerUI()
    window.show()
    sys.exit(app.exec_())
