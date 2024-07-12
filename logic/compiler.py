class NumerinCompiler:
    def __init__(self):
        self.variables = {}
        self.last_if_condition = False  # Almacena el resultado del último if

    def parse_line(self, line, indent_level=0):
        # Verificar si la línea termina con un punto y coma, excepto para líneas de apertura de bloque
        if not (line.endswith(';') or line.endswith('{') or line.endswith('}')):
            return "Error: Sintaxis incorrecta, falta punto y coma ';' al final"

        # Remover el punto y coma para el procesamiento, si existe
        if line.endswith(';'):
            line = line[:-1]

        # Extraer lexemas
        lexemes = self.extract_lexemes(line)
        print(f"Lexemas: {lexemes}")

        if line.startswith('*'):
            # Declaración de variable
            var_name, value = line.split('=')
            var_name = var_name.strip()
            value = value.strip()
            if any(op in value for op in ['+', '-', '*', '/']):
                self.handle_operation(var_name, value)
            else:
                if value.isalpha():
                    value = self.letter_to_number(value)
                self.variables[var_name] = int(value)
        elif line.startswith('631'):
            # Comando PRINT
            return self.handle_print(line)
        elif line.startswith('625'):
            # Comando IF
            return self.handle_if(line, indent_level)
        elif line.startswith('626'):
            # Comando ELSE
            return self.handle_else(line, indent_level)
        elif line.startswith('623'):
            # Comando FOR
            return self.handle_for(line, indent_level)
        return None

    def extract_lexemes(self, line):
        lexemes = []
        tokens = line.replace('(', ' ').replace(')', ' ').replace('=', ' ').replace('{', ' ').replace('}', ' ').split()
        for token in tokens:
            lexeme_type = self.identify_lexeme(token)
            lexemes.append((token.strip(), lexeme_type))
        return lexemes

    def identify_lexeme(self, token):
        if token.startswith('*'):
            return "Identificador"
        elif token.isdigit():
            return "Palabra Clave" if token in ['631', '625', '626', '623'] else "Número"
        elif token.isalpha():
            return "Token" if token in ["FOR", "WHILE", "IF", "ELSE", "SWITCH", "CASE", "BREAK", "EXIT", "PRINT", "DEF"] else "Identificador"
        elif token in ["(", ")", "=", "{", "}", ";", ",", "<", ">", "==", "<=", ">=", "+", "-", "*", "/"]:
            return "Simbología"
        else:
            return "Carácter no reconocido"

    def letter_to_number(self, letter):
        return ord(letter.upper()) - 65

    def handle_print(self, line):
        _, var_name = line.split('(')
        var_name = var_name.strip(');')
        if var_name in self.variables:
            return f"Mensaje: {self.variables[var_name]}"
        else:
            return "Error: Variable no definida"

    def handle_if(self, line, indent_level):
        try:
            condition_block = line[4:].split(')', 1)
            condition = condition_block[0].strip()  # Remove "625(" and strip spaces
            block = condition_block[1].split('{', 1)[1].rstrip('}')  # Extract block and remove closing brace

            variable, value = condition.split('=')
            variable = variable.strip()
            value = value.strip()

            # Evaluar la condición
            if variable in self.variables and str(self.variables[variable]) == value:
                self.last_if_condition = True
                indented_block = self.indent_code(block.strip(), indent_level + 1)
                return self.execute(indented_block, indent_level + 1)
            else:
                self.last_if_condition = False
                return None  # No output if the condition is false
        except Exception as e:
            return f"Error: Sintaxis incorrecta en la estructura IF ({str(e)})"

    def handle_else(self, line, indent_level):
        if not self.last_if_condition:
            try:
                block = line.split('{', 1)[1]
                block = block.rstrip('}')  # Remove closing brace
                indented_block = self.indent_code(block.strip(), indent_level + 1)
                return self.execute(indented_block, indent_level + 1)
            except Exception as e:
                return f"Error: Sintaxis incorrecta en la estructura ELSE ({str(e)})"
        return None  # No output if the last if condition was true

    def handle_for(self, line, indent_level):
        try:
            condition_block = line[4:].split(')', 1)
            condition_parts = condition_block[0].split(',')
            variable = condition_parts[0].strip()
            comparison = condition_parts[1].strip()
            increment = condition_parts[2].strip()
            block = condition_block[1].split('{', 1)[1].rstrip('}')

            var, operator, value = self.parse_comparison(comparison)

            # Evaluar la condición inicial del ciclo FOR
            if var in self.variables:
                initial_value = int(self.variables[var])
            else:
                initial_value = int(var)

            end_value = int(value)
            increment_value = int(self.letter_to_number(increment))

            output = []
            while (initial_value <= end_value and increment_value > 0) or (initial_value >= end_value and increment_value < 0):
                self.variables[variable] = initial_value
                indented_block = self.indent_code(block.strip(), indent_level + 1)
                result = self.execute(indented_block, indent_level + 1)
                if result:
                    output.append(result)
                initial_value += increment_value

            return "\n".join(output)
        except Exception as e:
            return f"Error: Sintaxis incorrecta en la estructura FOR ({str(e)})"

    def parse_comparison(self, comparison):
        operators = ['==', '<=', '>=', '<', '>']
        for op in operators:
            if op in comparison:
                var, value = comparison.split(op)
                # Convertir value a entero si es un número, de lo contrario, convertir a su valor numérico
                try:
                    value = int(value)
                except ValueError:
                    value = self.letter_to_number(value)
                return var.strip(), op.strip(), value.strip()
        raise ValueError("Operador de comparación no reconocido")

    def handle_operation(self, var_name, operation):
        try:
            if '+' in operation:
                operand1, operand2 = operation.split('+')
                result = self.evaluate_operand(operand1) + self.evaluate_operand(operand2)
            elif '-' in operation:
                operand1, operand2 = operation.split('-')
                result = self.evaluate_operand(operand1) - self.evaluate_operand(operand2)
            elif '*' in operation:
                operand1, operand2 = operation.split('*')
                result = self.evaluate_operand(operand1) * self.evaluate_operand(operand2)
            elif '/' in operation:
                operand1, operand2 = operation.split('/')
                result = self.evaluate_operand(operand1) // self.evaluate_operand(operand2)  # Usar división entera
            self.variables[var_name] = result
        except Exception as e:
            return f"Error: Sintaxis incorrecta en la operación ({str(e)})"

    def evaluate_operand(self, operand):
        operand = operand.strip()
        if operand in self.variables:
            return self.variables[operand]
        elif operand.isalpha():
            return self.letter_to_number(operand)
        else:
            return int(operand)

    def indent_code(self, block, indent_level):
        indented_lines = []
        for line in block.split('\n'):
            indented_lines.append('    ' * indent_level + line)
        return '\n'.join(indented_lines)

    def execute(self, code, indent_level=0):
        output = []
        lines = code.split('\n')
        for line in lines:
            if line.strip():
                result = self.parse_line(line.strip(), indent_level)
                if result:
                    output.append(result)
        return "\n".join(output)