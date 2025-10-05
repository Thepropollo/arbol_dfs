import tkinter as tk
from tkinter import messagebox
from time import sleep

# --------------------
# Clase del nodo del árbol
# --------------------
class Nodo:
    def __init__(self, valor, izq=None, der=None):
        self.valor = valor
        self.izq = izq
        self.der = der

# --------------------
# Función para convertir expresión en árbol
# --------------------
def construir_arbol(expresion):
    import ast

    def build(node):
        if isinstance(node, ast.BinOp):
            op = type(node.op)
            if op == ast.Add:
                valor = "+"
            elif op == ast.Sub:
                valor = "-"
            elif op == ast.Mult:
                valor = "*"
            elif op == ast.Div:
                valor = "/"
            return Nodo(valor, build(node.left), build(node.right))
        elif isinstance(node, ast.Num):  # Python < 3.8
            return Nodo(str(node.n))
        elif isinstance(node, ast.Constant):  # Python 3.8+
            return Nodo(str(node.value))
        else:
            raise ValueError("Expresión no soportada")

    nodo_ast = ast.parse(expresion, mode="eval").body
    return build(nodo_ast)

# --------------------
# DFS con GUI
# --------------------
def dfs_evaluar_gui(nodo, canvas, posiciones, resultados):
    if nodo is None:
        return 0
    x, y = posiciones[nodo]

    # resaltar nodo actual
    ovalo = canvas.create_oval(x-25, y-25, x+25, y+25, fill="orange", outline="black")
    texto = canvas.create_text(x, y, text=nodo.valor, font=("Arial", 14, "bold"))
    canvas.update()
    sleep(1)

    if nodo.izq is None and nodo.der is None:  # hoja
        canvas.delete(ovalo, texto)
        canvas.create_oval(x-25, y-25, x+25, y+25, fill="lightgreen", outline="black")
        canvas.create_text(x, y, text=nodo.valor, font=("Arial", 14, "bold"))
        resultados[nodo] = int(nodo.valor)
        return int(nodo.valor)

    izq = dfs_evaluar_gui(nodo.izq, canvas, posiciones, resultados)
    der = dfs_evaluar_gui(nodo.der, canvas, posiciones, resultados)

    if nodo.valor == "+":
        val = izq + der
    elif nodo.valor == "-":
        val = izq - der
    elif nodo.valor == "*":
        val = izq * der
    elif nodo.valor == "/":
        val = izq / der

    canvas.delete(ovalo, texto)
    canvas.create_oval(x-25, y-25, x+25, y+25, fill="lightblue", outline="black")
    canvas.create_text(x, y, text=f"{val}", font=("Arial", 12, "bold"))
    resultados[nodo] = val
    canvas.update()
    sleep(1)
    return val

# --------------------
# Clase GUI
# --------------------
class ArbolGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Evaluación de Árbol de Expresión con DFS")
        self.canvas = tk.Canvas(root, width=700, height=500, bg="white")
        self.canvas.pack()

        self.arbol = None
        self.posiciones = {}
        self.resultados = {}

        # entrada de expresión
        frame = tk.Frame(root)
        frame.pack(pady=10)
        tk.Label(frame, text="Expresión: ").pack(side=tk.LEFT)
        self.entrada = tk.Entry(frame, width=30)
        self.entrada.pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Construir Árbol", command=self.construir).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Evaluar con DFS", command=self.evaluar).pack(side=tk.LEFT, padx=5)

    def calcular_posiciones(self, nodo, x, y, dx):
        if nodo is None:
            return
        self.posiciones[nodo] = (x, y)
        if nodo.izq:
            self.calcular_posiciones(nodo.izq, x - dx, y + 100, dx // 2)
        if nodo.der:
            self.calcular_posiciones(nodo.der, x + dx, y + 100, dx // 2)

    def dibujar_aristas(self, nodo):
        if nodo is None:
            return
        x, y = self.posiciones[nodo]
        if nodo.izq:
            x2, y2 = self.posiciones[nodo.izq]
            self.canvas.create_line(x, y, x2, y2)
            self.dibujar_aristas(nodo.izq)
        if nodo.der:
            x2, y2 = self.posiciones[nodo.der]
            self.canvas.create_line(x, y, x2, y2)
            self.dibujar_aristas(nodo.der)

    def dibujar_nodos(self, nodo):
        if nodo is None:
            return
        x, y = self.posiciones[nodo]
        self.canvas.create_oval(x-25, y-25, x+25, y+25, fill="lightgray", outline="black")
        self.canvas.create_text(x, y, text=nodo.valor, font=("Arial", 14, "bold"))
        self.dibujar_nodos(nodo.izq)
        self.dibujar_nodos(nodo.der)

    def construir(self):
        expresion = self.entrada.get()
        if not expresion:
            messagebox.showwarning("Error", "Ingrese una expresión matemática")
            return
        try:
            self.arbol = construir_arbol(expresion)
            self.posiciones.clear()
            self.canvas.delete("all")
            self.calcular_posiciones(self.arbol, 350, 50, 150)
            self.dibujar_aristas(self.arbol)
            self.dibujar_nodos(self.arbol)
        except Exception as e:
            messagebox.showerror("Error", f"Expresión inválida:\n{e}")

    def evaluar(self):
        if not self.arbol:
            messagebox.showwarning("Atención", "Primero construya el árbol")
            return
        self.resultados.clear()
        resultado = dfs_evaluar_gui(self.arbol, self.canvas, self.posiciones, self.resultados)
        messagebox.showinfo("Resultado", f"Resultado final: {resultado}")

# --------------------
# Programa principal
# --------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = ArbolGUI(root)
    root.mainloop()
