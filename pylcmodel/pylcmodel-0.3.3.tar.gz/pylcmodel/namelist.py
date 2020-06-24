import parsley

grammar = r"""
namelist = ws '$' name:n pairlist:p ws '$END'? -> (n, dict(p))

pairlist = (pair:first (pair)*:rest -> [first] + rest) | -> []
pair = ws name:k ws '=' ws valuelist:v ws ','? -> (k.upper(), v)

valuelist = ws (stringlist | numberlist | truth | falsehood):v -> v

numberlist = (number:first (ws number)+:rest -> [first] + rest) | number
number = ('-' | -> ''):sign (intPart:ds (floatPart(sign ds) | -> int(sign + ds)))
intPart = (digit:first digits:rest -> first + rest) | digit
digit1_9 = :x ?(x in '123456789') -> x
digits = <digit*>
floatPart :sign :ds = <('.' digits exponent?) | exponent>:tail -> float(sign + ds + tail)
exponent = ('e' | 'E') ('+' | '-')? digits

stringlist = (string:first (ws string)+:rest -> [first] + rest) | string
string = ('\'' (~'\'' anything)*:c '\'' -> ''.join(c)) | unquoted_string
unquoted_string = <letter (letterOrDigit | '_' | '-')*>:n ' '* (',' | '\n') -> n

name = <letter (letter | digit | '_')*>

truth = 'T' -> True
falsehood = 'F' -> False
"""

parser = parsley.makeGrammar(grammar, {})


def reads(text):
    """
    Reads a namelist from a string.

    Parameters
    ----------
    text : str
        A string containing a namelist

    Returns
    -------
    name : str
        The name of the namelist
    list : dict
        The set of key-value pairs from the namelist
    """
    return parser(text).namelist()


def dumps(name, namelist):
    """
    Writes a namelist to a string.

    Parameters
    ----------
    name : str
        The name of the namelist
    namelist : dict
        Members of the namelist

    Returns
    -------
    str
        String representation of the namelist
    """
    # start with the opening marker
    result = " ${0}\n".format(name)
    # write each key-value pair on a new line
    for key, value in namelist.items():
        # string values need to be exported in quotes
        if isinstance(value, str):
            value = "'{0}'".format(value)
        # boolean values need to be replace by T or F
        elif isinstance(value, bool):
            value = "T" if value else 'F'
        result += " {0} = {1},\n".format(key, value)
    # finish with the closing marker
    result += " $END\n"
    return result
