import tkinter as tk
from logic.compiler import NumerinCompiler

class NumerinGUI:
    def __init__(self):
        self.compiler = NumerinCompiler()
        self.root = tk.Tk()
        self.root.title("Numerin Compiler")

        self.code_input = tk.Text(self.root, height=20, width=60, undo=True, wrap='none')
        self.code_input.pack()

        self.code_input.bind("<Return>", self.auto_indent)
        self.code_input.bind("<Tab>", self.insert_tab)

        self.run_button = tk.Button(self.root, text="Ejecutar", command=self.run_code)
        self.run_button.pack()

        self.output_label = tk.Label(self.root, text="Salida:")
        self.output_label.pack()

        self.output_text = tk.Text(self.root, height=10, width=60)
        self.output_text.pack()

    def insert_tab(self, event):
        self.code_input.insert(tk.INSERT, " " * 4)
        return 'break'

    def auto_indent(self, event):
        current_line = self.code_input.get("insert linestart", "insert")
        indent = 0
        for char in current_line:
            if char == ' ':
                indent += 1
            else:
                break
        self.code_input.insert("insert", "\n" + " " * indent)
        return "break"

    def run_code(self):
        # Limpiar la pantalla de salida
        self.output_text.delete("1.0", tk.END)
        
        # Obtener el código del input
        code = self.code_input.get("1.0", tk.END)
        
        # Ejecutar el código
        output = self.compiler.execute(code)
        
        # Mostrar el resultado en la pantalla de salida
        self.output_text.insert(tk.END, output)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    gui = NumerinGUI()
    gui.run()