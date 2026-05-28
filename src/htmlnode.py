
class HTMLNode():
    def __init__(self, tag=None, value=None, children= None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    def to_html(self):
        raise NotImplementedError
    def props_to_html(self):
        formatted_string = ""
        if self.props is None:
            return formatted_string
        for key, value in self.props.items():
            formatted_string += f' {key}="{value}"'
        return formatted_string
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})" 

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
        
        self.tag = tag
        self.value = value
        self.props = props
    def to_html(self):
        if self.value is None:
            raise ValueError
        if self.tag is None:

            return f"{self.value}"
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})" 

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, children, props)
        self.tag = tag
        self.children = children
        self.props = props
    
    def to_html(self):
        if self.tag is None:
            raise ValueError
        if self.children is None:
            raise ValueError("no children")

        else:
            children_string = ""
            for child in self.children:
                if child is None:
                    break
                else:
                    children_string += child.to_html()
            return f"<{self.tag}{self.props_to_html()}>{children_string}</{self.tag}>"

