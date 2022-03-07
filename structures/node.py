
class Node:

    def __init__(self, value) -> None:
        self.value = value
        self.children = []

    def add_child(self, child : any) -> None:
        self.children.append(child)

    def get_children(self) -> list:
        return self.children

    def __str__(self) -> str:
        return f"Value {str(self.value)} children {str(self.children)}"