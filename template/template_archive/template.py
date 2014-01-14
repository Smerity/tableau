import re, sys, os
from .nodes import GroupNode, PythonNode, TextNode

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "..", "templates")

def _parse_template(file_contents):

    root = GroupNode()        
    for i in re.split("({[{%].*?[%}]})", file_contents):

        #   Checks for python expressions
        if i.startswith("{{") and i.endswith("}}"):
            i = i[2:-2].strip()
            root.add(PythonNode(i))
        #   Checks for the squiggily percent nodes
        #   and renders if the keyword is include
        elif i.startswith("{%") and i.endswith("%}"):
            
            i = i[2:-2].strip().split()
            if i[0] == "include":
                #Need to use helper to open include file
                root.add(parse_template(i[1]))
            #For other tags, use _parse_template() 
                
        #   Otherwise it is just html
        else:
            root.add(TextNode(i))
    return root

def parse_template(file_path):
    file_path = os.path.join(TEMPLATE_DIR, file_path)
    with open(file_path) as f:
        return _parse_template(f.read())
        
def render(in_file, context):
    return parse_template(in_file).evaluate(context)
