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

def test_cases():
    def test(func, params, expected):
        actual = ""
        try:
            actual = func(*params)
        except Exception as e:
            actual = e
        if expected == actual:
            print("Test Successful")
        else:
            print("Test Failed")
        print(f"Expected Result: \n{expected}")
        print(f"Actual Result: \n{actual}")
    
    base = TextNode("Hello!", TextType.NORMAL)
    eq_test1 = TextNode("Hello!", TextType.NORMAL)
    eq_test2 = TextNode("Hello!", TextType.NORMAL, "google.com")
    eq_test3 = "Hello!"
    eq_test4 = TextNode("Goodbye!", TextType.NORMAL)
    test(base.__eq__, [eq_test1], True)
    test(base.__eq__, [eq_test2], False)
    test(base.__eq__, [eq_test3], "Can't compare TextNode to <class 'str'>")
    test(base.__eq__, [eq_test4], False)
    test(base.__repr__, [], "TextNode(Hello!, normal, None)")

        
if __name__ == "__main__":
    test_cases()