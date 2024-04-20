from bs4 import Tag, ResultSet

class HTMLElementExecption(Exception):
    """Error element is not found"""

def isElementNone(element: Tag|None):
    """Raise an HTMLElmentException if
    element is None"""

    if (element is None):
        raise HTMLElementExecption("Error element is not found")
    else:
        return element

def isListEmpty(elements: ResultSet[Tag]):
    """Raise an HTMLElmentException if
    a list of elements is empty"""

    if (not elements):
        raise HTMLElementExecption("Error elements are not found")