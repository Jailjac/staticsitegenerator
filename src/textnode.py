from enum import Enum

class TextType(Enum):
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text, text_type, url = None):
        self.text = text
        if text_type in TextType:
            self.text_type = text_type
        else:
            raise Exception("Invalid TextType")
        self.url =  url
        
    def __eq__(self, other):
        if type(other) is TextNode:
            return (self.text == other.text and
                    self.text_type == other.text_type and
                    self.url == other.url)
        else:
            raise Exception(f"Can't compare TextNode to {type(other)}")
        
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"