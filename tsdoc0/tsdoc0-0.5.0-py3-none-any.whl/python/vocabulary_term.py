from tsdoc0.python.segment import Segment
from tsdoc0.python.utils import repr_parent
from typing import Final
from typing import Optional
from typing import TYPE_CHECKING

# Conditional import used because there would be a circular dependency
# https://mypy.readthedocs.io/en/latest/common_issues.html#import-cycles
if TYPE_CHECKING:
    from tsdoc0.python.vocabulary import Vocabulary  # noqa: F401

import attr


@attr.s(auto_attribs=True, kw_only=True)
class VocabularyTerm(Segment):
    # Forward reference used because there would be a circular dependency
    # https://mypy.readthedocs.io/en/latest/kinds_of_types.html#class-name-forward-references
    parent: Optional["Vocabulary"] = attr.ib(eq=False, repr=repr_parent)
    text: Final[str]  # type: ignore[misc]

    @property
    def name(self) -> str:
        names = {
            "Equal to": "Equal to (==)",
            "Greater than": "Greater than (>)",
            "Less than": "Less than (<)",
            "Not equal to": "Not equal to (!=)",
        }

        return names.get(self.text, self.text)

    @property
    def definition(self) -> str:
        definitions = {
            "and operator": "True if all parts are True",
            "Argument": "Information that a function needs to know in order to run",
            "Assignment": "Storing information in a variable",
            "Attribute": "A piece of information an object knows about itself",
            "Boolean": "A True or False value",
            "Boolean zen": "Using a boolean as a complete condition",
            "break statement": "Immediately end a loop",
            "Chained comparison": "An expression with more than one comparison operator",  # noqa: E501
            "Class": "A blueprint for creating something specific",
            "Comment": "A note that the computer ignores",
            "Comparison operator": "Compares two values and gives a yes or no answer",
            "Compound assignment operator": "Changes a variable based on the current value",  # noqa: E501
            "Compound boolean expression": "A boolean expression made of up of other boolean expressions",  # noqa: E501
            "Condition": "Asks a yes or no question",
            "Conditional": "Runs the first section of code where the condition is true",
            "Constant": "A variable that stores a value that does not change",
            "continue statement": "Immediately end an iteration",
            "Coordinates": "Horizontal (x) and vertical (y) position",
            "Data type": "The category a piece of information belongs to",
            "Decrement": "Decrease a variable by an amount",
            "Documentation": "A written explanation of how to use code",
            "elif clause": "When all prior conditions are false, runs a section of code when the condition is true",  # noqa: E501
            "else clause": "When all prior conditions are false, runs a section of code as a last alternative",  # noqa: E501
            "Equal to": "Are the two values the same?",
            "Error": "When the computer encounters something unexpected in your code",  # noqa: E501
            "Exponentiation operator": "Multiplies a number by itself some number of times",  # noqa: E501
            "Expression": "A piece of code that produces a value",
            "Float": "A number with a decimal point",
            "Floor division operator": "Rounds the quotient down to a whole number after division",  # noqa: E501
            "Function": "A named code action that can be used in a program",
            "Greater than": "Is the left value bigger than the right value?",
            "Header comment": 'A multi-line comment at the top of a program surrounded by `"""` marks',  # noqa: E501
            "if statement": "Runs a section of code when the condition is true",
            "Increment": "Increase a variable by an amount",
            "Infinite loop": "A loop with a condition that will always be True",
            "Instance": "A specific copy created from a class",
            "Integer": "A whole number",
            "Iteration": "One repetition of a loop",
            "Less than": "Is the left value smaller than the right value?",
            "Library": "A collection of code from outside the program",
            "Literal": "A value you can literally see",
            "Logical operator": "Combines or modifies a boolean",
            "Loop else clause": "A clause following a loop that runs unless the loop ends with break",  # noqa: E501
            "Main loop": "Keeps a window open and updated",
            "Method": "A function that belongs to an instance",
            "Modulo operator": "Calculates the remainder after division",
            "Nested conditional": "A conditional inside another conditional",
            "None": 'A special literal that means "no value"',
            "Not equal to": "Are the two values different?",
            "not operator": "Gives the opposite boolean value",
            "or operator": "True if one or more parts are True",
            "Output": "Information a program gives to the user, such as text",
            "random library": "A library with code to create unpredictable values",
            "Return value": "Information given back by a function",
            "Sprite": "An on-screen graphic based on an image",
            "Statement": "A single line of code that performs an action",
            "String": "A group of letters, symbols and/or numbers inside double quotation marks",  # noqa: E501
            "String concatenation": "Join two strings together with the + operator",
            "String multiplication": "Repeat a string a certain number of times with the * operator",  # noqa: E501
            "Syntax": "The exact spelling, symbols, and order of code",
            "Text": "An on-screen graphic based on a string",
            "Then block": "A section of code that might get run",
            "tsapp library": "A library used to create programs with graphics",
            "Typecast": "Treat one data type like another",
            "User input": "Information the program receives from the user",
            "Variable": "A storage container for information",
            "while loop": "Repeats a section of code until a condition is no longer True",  # noqa: E501
            "Window": "A container for displaying graphics",
        }

        return definitions[self.text]

    @property
    def instruction(self) -> str:
        instructions = {
            "and operator": "2.4.1",
            "Argument": "1.2.1",
            "Assignment": "1.1.3",
            "Attribute": "3.3.1",
            "Boolean": "2.4.1",
            "Boolean zen": "2.4.2",
            "break statement": "3.2.1",
            "Chained comparison": "2.2.2",
            "Class": "3.3.1",
            "Comment": "1.1.2",
            "Comparison operator": "2.1.2",
            "Compound assignment operator": "1.4.1",
            "Compound boolean expression": "2.4.2",
            "Condition": "2.1.1",
            "Conditional": "2.2.1",
            "Constant": "3.4.2",
            "continue statement": "3.2.1",
            "Coordinates": "3.4.1",
            "Data type": "1.3.1",
            "Decrement": "1.4.1",
            "Documentation": "1.2.2",
            "elif clause": "2.2.1",
            "else clause": "2.2.1",
            "Equal to": "2.1.1",
            "Error": "1.1.2",
            "Exponentiation operator": "2.3.2",
            "Expression": "1.4.1",
            "Float": "1.3.1",
            "Floor division operator": "2.3.2",
            "Function": "1.2.1",
            "Greater than": "2.1.2",
            "Header comment": "1.1.2",
            "if statement": "2.1.1",
            "Increment": "1.4.1",
            "Infinite loop": "3.1.1",
            "Instance": "3.3.1",
            "Integer": "1.3.1",
            "Iteration": "3.1.1",
            "Less than": "2.1.2",
            "Library": "1.2.1",
            "Literal": "1.3.1",
            "Logical operator": "2.4.1",
            "Loop else clause": "3.2.1",
            "Main loop": "3.4.1",
            "Method": "3.3.1",
            "Modulo operator": "2.3.2",
            "Nested conditional": "2.2.2",
            "None": "1.4.2",
            "Not equal to": "2.1.1",
            "not operator": "2.4.1",
            "or operator": "2.4.1",
            "Output": "1.1.1",
            "random library": "2.3.1",
            "Return value": "1.4.2",
            "Sprite": "3.4.1",
            "Statement": "1.1.1",
            "String": "1.1.1",
            "String concatenation": "1.3.2",
            "String multiplication": "1.3.2",
            "Syntax": "1.1.1",
            "Text": "3.4.2",
            "Then block": "2.2.1",
            "tsapp library": "3.4.1",
            "Typecast": "1.3.2",
            "User input": "1.1.3",
            "Variable": "1.1.3",
            "while loop": "3.1.1",
            "Window": "3.4.1",
        }

        return instructions[self.text]
