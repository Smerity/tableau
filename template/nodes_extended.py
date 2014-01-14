import html

class Node:
    """Abstract Node"""
    def __init__(self):
        pass
    
    def evaluate(self, context):
        """Renders node's content to outfile"""
        return NotImplemented



class GroupNode(Node):
    """Stores child nodes"""
    def __init__(self):
        self.children = []

    def add(self, child):
        self.children.append(child)

    def evaluate(self, context):
        results = []
        for child in self.children:
            results.append(child.evaluate(context))
        return (''.join(results))    	



class TextNode(Node):
    """Stores HTML"""
    def __init__(self, content):
        self.content = content

    def evaluate(self, context):
        return(self.content)



class PythonNode(Node):
    """Stores python expression"""
    def __init__(self, expr):
        self.expr = expr

    def evaluate(self, context):
        return(html.escape(str(eval(self.expr, {}, context))))



class CommentNode(Node):
    """Stores comments"""
    def __init__(self, content):
        self.content = content

    def evaluate(self, context):
        pass



class IfNode(Node):
    """Renders content if predicate"""
    def __init__(self, predicate):
        self.predicate = predicate
        self.child = None
    def set_child(self, child):
        self.child = child


    def evaluate(self, context):
        if eval(self.predicate, {}, context):
            return self.child.evaluate(context)
        else:
            return ''




class SafeNode(Node):
    """Stores a safe python expression"""
    def __init__ (self, expr):
        self.expr = expr

    def evaluate(self, context):
        return(str(eval(self.expr, {}, context)))



class ForNode(Node):

    def __init__ (self, variable, iterable):
        self.variable = variable #Loop variable (Eg i)
        self.iterable = iterable #Thing to loop through
        self.child = None #Stuff executed in loop (GroupNode)

    def set_child(self, child):
        self.child = child

    def evaluate(self, context):
        iterable = eval(self.iterable, {}, context)
        iterations = []
        for x in iterable:
            tempcontext = dict(context)
            tempcontext[self.variable] = x
            iterations.append(self.child.evaluate(tempcontext))
        return "".join(iterations)
