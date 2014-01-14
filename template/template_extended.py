import re, sys, os
from .nodes import GroupNode, PythonNode, TextNode, IfNode, ForNode

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "..", "templates")
DEBUG_MODE = True

class TemplateException(Exception):
    pass

def debug(text):
    if DEBUG_MODE:
        print(text)
def parse_template(token_list, upto, parent, parent_type):
    pos = upto
    if parent is None:
        parent = GroupNode()
    while pos < len(token_list):
        t = token_list[pos]
        if t['label'] == "python":
            parent.add(PythonNode(t['expr']))
            pos += 1
        elif t['label'] == "include":
            file_path = os.path.join(TEMPLATE_DIR, t['expr'])
            with open(file_path) as f:
                parse_template(lexer(f.read()),0,parent,parent_type)[0]
            pos += 1
        elif t['label'] == 'if':
            new_node = IfNode(t['expr'])
            parent.add(new_node)
            pos += 1
            parse_result = parse_template(token_list, pos, GroupNode(), "if")
            if_group = parse_result[0]
            pos = parse_result[1]
            new_node.set_child(if_group)
        elif t['label'] == "end if":
            if parent_type == "if":
                pos += 1
                return (parent, pos)
            else:
                raise TemplateException("Unexpected end of 'if' tag. Parent is {!r}".format(parent_type))
        elif t['label'] == 'for':
            new_node = ForNode(t['expr']['variable'], t['expr']['iterable'])
            parent.add(new_node)
            pos += 1
            parse_result = parse_template(token_list, pos, GroupNode(), "for")
            for_group = parse_result[0]
            pos = parse_result[1]
            new_node.set_child(for_group)
        elif t['label'] == "end for":
            if parent_type == "for":
                pos += 1
                return (parent, pos)
            else:
                raise TemplateException("Unexpected end of 'for' tag. Parent is {!r}".format(parent_type))
        elif t['label'] == "html":
            parent.add(TextNode(t['expr']))
            pos += 1
    return (parent, pos)

def render(in_file, context):
    file_path = os.path.join(TEMPLATE_DIR, in_file)
    with open(file_path) as f:
        parse_result =  parse_template(lexer(f.read()),0,None,'group')[0]
        return parse_result.evaluate(context)
        

def lexer (file_contents):
    tags = re.compile(r"({[{%].*?[%}]})")
    tokens = re.split(tags, file_contents)
    labelled_tokens = [token_identifier(t) for t in tokens]
    return (labelled_tokens)

def token_creator(expr, label):
    return {'expr':expr, 'label':label}

def token_identifier(token):
    if token.startswith("{{") and token.endswith("}}"):
        return token_creator(token[2:-2].strip(), "python")
    elif token.startswith("{%") and token.endswith("%}"):
        token_list = token[2:-2].strip().split()
        if token_list[0] == "include":
            return token_creator(token_list[1], "include")
        elif token_list[0] == "if":
            return token_creator(" ".join(token_list[1:]), "if")
        elif ' '.join(token_list) == 'end if':
            return token_creator(None, 'end if')
        elif token_list [0] == "for":
            return token_creator({'variable': token_list[1], 'iterable': ' '.join(token_list[3:])}, "for")
        elif ' '.join(token_list) == 'end for':
            return token_creator(None, 'end for')
    else:
        return token_creator(token,'html')