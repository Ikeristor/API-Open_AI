import json
from pyparsing import Word, alphas, nums, Literal, Forward, Group, ZeroOrMore, oneOf

def simplify_cfg(json_file):

    with open(json_file, 'r') as file:
        data = json.load(file)
    
    # Extract the CFG
    cfg = data.get("generated_cfg", "")
    
    # Simplify (remove duplicates and format consistently)
    simplified_cfg = "\n".join(sorted(set(cfg.splitlines()), key=str.strip))
    
    print("Simplified CFG:\n", simplified_cfg)
    return simplified_cfg

def normalize_cfg(cfg):
        return cfg.replace("<expression>", "expr").replace("<term>", "term").replace("<factor>", "factor").replace("<number>", "number")

def compare_cfg(generated_cfg, predefined_cfg):
    gen_rules = set(generated_cfg.splitlines())
    predef_rules = set(predefined_cfg.splitlines())
    
    # Find common, missing, and extra rules
    common = gen_rules & predef_rules
    missing = predef_rules - gen_rules
    extra = gen_rules - predef_rules
    
    print("Common Rules:\n", "\n".join(common))
    print("Missing Rules:\n", "\n".join(missing))
    print("Extra Rules:\n", "\n".join(extra))
    
    return common, missing, extra

def create_arithmetic_parser():
    # Define grammar tokens
    identifier = Word(alphas, alphas + nums + "_")  # variable names
    number = Word(nums)                             # numbers
    plus = Literal("+")
    minus = Literal("-")
    mult = Literal("*")
    div = Literal("/")
    lpar = Literal("(").suppress()
    rpar = Literal(")").suppress()

    # Define grammar structure
    expr = Forward()
    term = Forward()
    factor = Forward()

    factor <<= (identifier | number | Group(lpar + expr + rpar))
    term <<= factor + ZeroOrMore((mult | div) + factor)
    expr <<= term + ZeroOrMore((plus | minus) + term)

    return expr

def validate_expression(expression):
    parser = create_arithmetic_parser()
    try:
        parser.parseString(expression, parseAll=True)
        return True  # Valid expression
    except:
        return False  # Invalid expression

# Test with examples
examples = [
    "3 + 5",           # Valid
    "3 ++ 5",          # Invalid
    "3 / (4 - x",      # Invalid
    "a * (b + c) / d", # Valid
    "((1 + 2) * 3))",  # Invalid
    "x * y + z - w"    # Valid
]

# Test the function
simplified_cfg = simplify_cfg("cfg_output.json")

normalized_cfg = normalize_cfg(simplified_cfg)

# Define the predefinido CFG for arithmetic expressions
predefined_cfg = """
expr → expr + term | expr - term | term
term → term * factor | term / factor | factor
factor → ( expr ) | number | identifier
"""
common, missing, extra = compare_cfg(simplified_cfg, predefined_cfg)

for example in examples:
    is_valid = validate_expression(example)
    print(f"Expression: {example} | Valid: {is_valid}")



