import numpy as np
import ast
from graphviz import *

def visit(node, nodes, pindex, g):
    name = str(type(node).__name__)
    index = len(nodes)
    nodes.append(index)
    g.node(str(index), name)
    if index != pindex:
        g.edge(str(index), str(pindex))
    for n in ast.iter_child_nodes(node):
        visit(n, nodes, index, g)
    

if __name__ == "__main__":
    with open("demo.py") as f:
        data = f.read()
    f_ast = ast.parse(data)
    graph = Digraph(format="png")
    print(ast.dump(f_ast))
    visit(f_ast, [], 0, graph)
    graph.render("test")
