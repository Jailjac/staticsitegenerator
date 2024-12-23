class HTMLNode():
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props is None:
            return ""
        result = ""
        for k, v in self.props.items():
            result += f' {k}="{v}"'
        return result
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Leaf node has no value")
        html_string = self.value
        if self.tag:
            html_string = f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
        return html_string
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode missing tag")
        if self.children is None:
            raise ValueError("ParentNode missing children")
        html_string = ""
        for child in self.children:
            html_string += child.to_html()
        html_string = f'<{self.tag}{self.props_to_html()}>{html_string}</{self.tag}>'
        return html_string