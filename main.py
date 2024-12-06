import math


class Node:
    def __init__(self, value, gradient=0):
        self.value = value
        self.parents = []
        self.operation = None
        self.gradient = gradient
        self.reverseGrad = 0

    def exp(self):
        output = Node(math.exp(self.value))
        output.parents.append(self)
        output.operation = "EXP"
        output.gradient = output.value * self.gradient
        return output

    def ln(self):
        output = Node(math.log(self.value))
        output.parents.append(self)
        output.operation = "NLOG"
        output.gradient = 1 / self.value * self.gradient
        return output

    def sin(self):
        output = Node(math.sin(self.value))
        output.parents.append(self)
        output.operation = "SIN"
        output.gradient = math.cos(self.value) * self.gradient
        return output

    def cos(self):
        output = Node(math.cos(self.value))
        output.parents.append(self)
        output.operation = "COS"
        output.gradient = -math.sin(self.value) * self.gradient
        return output

    def tan(self):
        output = Node(math.tan(self.value))
        output.parents.append(self)
        output.operation = "TAN"
        output.gradient = ((1 / math.cos(self.value)) ** 2) * self.gradient
        return output

    # Forward Mode
    def forward(self):
        return self.gradient

    # Reverse Mode
    def reverse(self):
        self.reverseGrad = 1

        stack = [self]
        visited_nodes = set()

        while stack:
            node = stack.pop()
            if node not in visited_nodes:
                visited_nodes.add(node)
                for parent in node.parents:
                    if node.operation == "ADD":
                        parent.reverseGrad += node.reverseGrad
                    elif node.operation == "SUB":
                        parent.reverseGrad += (
                            1 if parent == node.parents[0] else -1
                        ) * node.reverseGrad
                    elif node.operation == "MUL":
                        other = (
                            node.parents[0]
                            if parent == node.parents[1]
                            else node.parents[1]
                        )
                        parent.reverseGrad += node.reverseGrad * other.value

                    elif node.operation == "DIV":

                        if node.parents[0] == parent:
                            parent.reverseGrad += node.reverseGrad * (
                                1 / node.parents[1].value
                            )
                        else:
                            parent.reverseGrad += (
                                node.reverseGrad
                                * node.parents[0].value
                                * -1
                                / node.parents[1].value ** 2
                            )

                    elif node.operation == "NLOG":
                        parent.reverseGrad += 1 / parent.value * node.reverseGrad
                    elif node.operation == "SIN":
                        parent.reverseGrad += math.cos(parent.value) * node.reverseGrad
                    elif node.operation == "COS":
                        parent.reverseGrad += -math.sin(parent.value) * node.reverseGrad
                    elif node.operation == "TAN":
                        parent.reverseGrad += (
                            (1 / math.cos(parent.value)) ** 2
                        ) * node.reverseGrad

                    stack.append(parent)

    # Overload Operators
    def __add__(self, other):
        output = Node(self.value + other.value)
        output.parents.append(self)
        output.parents.append(other)
        output.operation = "ADD"
        output.gradient = self.gradient + other.gradient
        return output

    def __sub__(self, other):
        output = Node(self.value - other.value)
        output.parents.append(self)
        output.parents.append(other)
        output.operation = "SUB"
        output.gradient = self.gradient - other.gradient
        return output

    def __mul__(self, other):
        output = Node(self.value * other.value)
        output.parents.append(self)
        output.parents.append(other)
        output.operation = "MUL"
        output.gradient = self.gradient * other.value + other.gradient * self.value
        return output

    def __truediv__(self, other):
        output = Node(self.value / other.value)
        output.parents.append(self)
        output.parents.append(other)
        output.operation = "DIV"
        output.gradient = (
            self.gradient * other.value - other.gradient * self.value
        ) / other.value**2
        return output

    # utils function
    def __str__(self):
        return f"Node(value={self.value})"

    def __repr__(self):
        return f"Node(value={self.value},operation = {self.operation},gradient = {self.gradient} parents={[parent.value for parent in self.parents]})"

    def listParents(self):
        if len(self.parents) != 0:
            for n in self.parents:
                print(repr(n))
                n.listParents()


x = Node(2, gradient=1)
y = Node(5)
z = ((x.tan()).cos()).sin()

z.reverse()
print(f"Gradient wrt to x is: {x.reverseGrad}")
print(f"Gradient wrt to y is {y.reverseGrad}")
