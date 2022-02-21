import graphviz as gv
import re
import numbers
import sys
import math
import ast
from uuid import uuid4 as uuid

def get_demo_tree():
    y_i_dsub1_t = {
        "node_type": "tensor",
        "value": {
           "node_type": "tensor",
           "value": {
               "node_type": "tensor",
               "value": "y",
               "slice": {
                    "node_type": "index",
                    "value" : "i"
                },
           },
           "slice": {
               "node_type": "index",
               "value": {
                   "node_type": "bin_op",
                   "op": "sub",
                   "left": "d",
                   "right": {
                       "node_type": "number",
                       "n": 1
                   }
               }
           } 
        },
        "slice": {
            "node_type": "index",
            "value" : "t"
        },
    }
    xss_i_t = {
        "node_type": "tensor",
        "value": {
            "node_type": "tensor",
            "value": "xss",
            "slice": {
                "node_type": "index",
                "value": "i",
            }
        },
        "slice": {
            "node_type": "index",
            "value": "t",
        }
    }
    if_block = {
        "node_type": "if",
        "cond": "TBD",
        "body": [{
                "node_type": "assign",
                "target": "x_t",
                "value": xss_i_t,
        }],
        "else": [{
                "node_type": "assign",
                "target": "x_t",
                "value": y_i_dsub1_t,
        }]
    }

    y_i_d_t = {
        "node_type": "tensor",
        "value": {
           "node_type": "tensor",
           "value": {
               "node_type": "tensor",
               "value": "y",
               "slice": {
                    "node_type": "index",
                    "value" : "i"
                },
           },
           "slice": {
               "node_type": "index",
               "value": "d"
           } 
        },
        "slice": {
            "node_type": "index",
            "value" : "t"
        },
    }
    compute = {
        "node_type": "bin_op",
        "op": "add",
        "left": {
            "node_type": "bin_op",
            "op": "matmul",
            "left": "w",
            "right": "x_t",
        },
        "left": {
            "node_type": "bin_op",
            "op": "matmul",
            "left": "u",
            "right": {
                "node_type": "tensor",
                "value": "h0",
                "slice": {
                    "node_type": "index",
                    "value" : "i"
                },
            }
        },
    }

    body_node = [
        if_block,
        {
            "node_type": " assign",
            "target": y_i_d_t,
            "value": compute
        },
    ]

    for_whole = {
        "node_type": "for",
        "iter": {"node_type": "call"},
        "body": [{
            "node_type": "for",
            "iter": {"node_type": "call"},
            "body": [{
                "node_type": "for",
                "iter": {"node_type": "call"},
                "body": body_node,
            }],
        }]
    }

    func = {
        "node_type": "function",
        "name": "lstm",
        "args": "[args]",
        "body": [for_whole, {
                "node_type": "return",
                "value": "y",
        }]
    }

    return func

