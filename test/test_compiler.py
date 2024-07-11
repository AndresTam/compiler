import unittest
from logic.compiler import NumerinCompiler

class TestNumerinCompiler(unittest.TestCase):
    def setUp(self):
        self.compiler = NumerinCompiler()

    def test_variable_declaration(self):
        self.compiler.parse_line("*123=A;")
        self.assertEqual(self.compiler.variables["*123"], "0")

    def test_print(self):
        self.compiler.parse_line("*123=A;")
        output = self.compiler.handle_print("631(*123);")
        self.assertEqual(output, "Mensaje: 0")

    def test_print_direct(self):
        output = self.compiler.execute("*123=A;\n631(*123);")
        self.assertEqual(output, "Mensaje: 0")

    def test_if_true(self):
        output = self.compiler.execute("*123=A;\n625(*123=0){\n631(*123);\n}")
        self.assertEqual(output, "Mensaje: 0")

    def test_if_false(self):
        output = self.compiler.execute("*123=B;\n625(*123=0){\n631(*123);\n}")
        self.assertEqual(output, "")

    def test_syntax_error(self):
        output = self.compiler.execute("*123=A\n631(*123)")
        self.assertEqual(output, "Error: Sintaxis incorrecta, falta punto y coma ';' al final")

if __name__ == "__main__":
    unittest.main()