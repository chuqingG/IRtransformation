#!/usr/bin/python3
import ast
import graphviz as gv
import subprocess
import numbers
import re
from uuid import uuid4 as uuid
import optparse
import sys
from manmade import get_demo_tree

def main(args):
    parser = optparse.OptionParser(usage="astvisualizer.py [options] [string]")
    parser.add_option("-f", "--file", action="store",
                      help="Read a code snippet from the specified file")
    parser.add_option("-l", "--label", action="store",
                      help="The label for the visualization")

    options, args = parser.parse_args(args)
    if options.file:
        with open(options.file) as instream:
            code = instream.read()
        label = options.file
        code_ast = ast.parse(code)
        transformed_ast = transform_ast(code_ast)
    else:
        transformed_ast = get_demo_tree()
        label = "mydemo"
    if options.label:
        label = options.label

    renderer = GraphRenderer()
    renderer.render(transformed_ast, label=label)


def transform_ast(code_ast):
    if isinstance(code_ast, ast.AST):
        node = {to_camelcase(k): transform_ast(getattr(code_ast, k)) for k in code_ast._fields}
        node['node_type'] = to_camelcase(code_ast.__class__.__name__)
        return node
    elif isinstance(code_ast, list):
        return [transform_ast(el) for el in code_ast]
    else:
        return code_ast


def to_camelcase(string):
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', string).lower()


class GraphRenderer:
    """
    this class is capable of rendering data structures consisting of
    dicts and lists as a graph using graphviz
    """

    graphattrs = {
        'labelloc': 't',
        'fontcolor': 'white',
        'bgcolor': '#333333',
        'margin': '0',
    }

    nodeattrs = {
        'color': 'white',
        'fontcolor': 'white',
        'style': 'filled',
        'fillcolor': '#006699',
    }

    edgeattrs = {
        'color': 'white',
        'fontcolor': 'white',
    }

    _graph = None
    _rendered_nodes = None


    @staticmethod
    def _escape_dot_label(str):
        return str.replace("\\", "\\\\").replace("|", "\\|").replace("<", "\\<").replace(">", "\\>")


    def _render_node(self, node, father=None):
        if isinstance(node, (str, numbers.Number)) or node is None:
            node_id = uuid()
        else:
            node_id = id(node)
        node_id = str(node_id)

        if node_id not in self._rendered_nodes:
            self._rendered_nodes.add(node_id)
            if isinstance(node, dict):
                self._render_dict(node, node_id, father)
            elif isinstance(node, list):
                self._render_list(node, node_id, father)
            else:
                name = self._escape_dot_label(str(node))
                # print("node:" + name)
                self._graph.node(node_id, label=name)

        return node_id

    
    def _skip_node(self, node):
        return
    
    def _skip_bridge_node(self, node):
        for key, value in node.items():
            if key == "id":
                return value
        # return node[0]

    def _skip_thischild(self, node, father):
        return 


    def _render_dict(self, node, node_id, father):
        name = node.get("node_type", "[dict]")
        if name == "name":
            var = node.get("id", "variable")
            self._graph.node(node_id, label=var)
        elif name == 'import':
            return
        elif name != "load" and name != "store":
            # print(node)
            
            # print("dict:" + name)
            # if name == 'for':
            #     print(node)
            self._graph.node(node_id, label=name)
            for key, value in node.items():
                if key == "node_type":
                    continue
                child_node_id = self._render_node(value)
                e_name = self._escape_dot_label(key)
                child_name = self._escape_dot_label(str(value))
                # print(name + "->" + e_name + "->" )
                # print("%ld:%ld", node_id, child_node_id)
                if e_name != "ctx":
                    self._graph.edge(node_id, child_node_id, label=e_name)
    

    def _render_list(self, node, node_id, father):
        self._graph.node(node_id, label="[list]")
        # print(node)
        for idx, value in enumerate(node):
            name = value.get("node_type", "default")
            if name == "import":
                continue
            child_node_id = self._render_node(value, node)
            self._graph.edge(node_id, child_node_id, label=self._escape_dot_label(str(idx)))


    def render(self, data, *, label=None):
        # create the graph
        graphattrs = self.graphattrs.copy()
        if label is not None:
            graphattrs['label'] = self._escape_dot_label(label)
        graph = gv.Digraph(graph_attr = graphattrs, node_attr = self.nodeattrs, edge_attr = self.edgeattrs)

        # recursively draw all the nodes and edges
        self._graph = graph
        self._rendered_nodes = set()
        self._render_node(data)
        self._graph = None
        self._rendered_nodes = None

        # display the graph
        graph.format = "png"
        graph.render(label)
        # subprocess.Popen(['xdg-open', "test.pdf"])


if __name__ == '__main__':
    parser = optparse.OptionParser(usage="astvisualizer.py [options] [string]")
    parser.add_option("-f", "--file", action="store",
                      help="Read a code snippet from the specified file")
    parser.add_option("-l", "--label", action="store",
                      help="The label for the visualization")

    options, args = parser.parse_args(sys.argv)
    if options.file:
        with open(options.file) as instream:
            code = instream.read()
        label = options.file
        code_ast = ast.parse(code)
        transformed_ast = transform_ast(code_ast)
    else:
        transformed_ast = get_demo_tree()
        label = "demoast"
    if options.label:
        label = options.label

    renderer = GraphRenderer()
    renderer.render(transformed_ast, label=label)
