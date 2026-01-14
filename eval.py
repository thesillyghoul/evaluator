from math import sin, cos, tan, lcm, gcd, log, log10, sqrt, factorial
import re

div_ops   = { "/", "d", "%" }
operators = { "+", "-", "*", "^", *div_ops }
all_ops   = { "(", ")", *operators }

deg = 0.017453292519943295

calc_extra = {
    "lcm"  : lambda x: lcm(*x),
    "gcd"  : lambda x: gcd(*x),
    "sin"  : lambda x: sin(x * deg),
    "cos"  : lambda x: cos(x * deg),
    "tan"  : lambda x: tan(x * deg),
    "ln"   : lambda x: log(x),
    "log"  : lambda x: log10(x),
    "sqrt" : lambda x: sqrt(x),
    "fact" : lambda x: factorial(x)
}

calculate = {
    "+" : lambda a, b: a + b,
    "-" : lambda a, b: a - b,
    "*" : lambda a, b: a * b,
    "/" : lambda a, b: a / b,
    "%" : lambda a, b: a % b,
    "^" : lambda a, b: a ** b,
    "d" : lambda a, b: a // b
}

precedence = {
    "(" : 0,
    "+" : 1, "-" : 1,
    "*" : 2, "/" : 2, "d" : 2, "%" : 2,
    "^" : 3
}

tokens        = re.compile(r"(?:(?<=[-+*^/%d()])-)?\d*\.?\d+(?:E-?\d+)?|[-+*^/%()d]")
symbols       = re.compile(r"[-+*^/%()\d,.eE]+|pi|ans|(?:sin|cos|tan|lcm|gcd|ln|log|fact|sqrt)\(")
operand       = re.compile(r"\d*\.?\d+(?:E-?\d+)?")
unary_minus   = re.compile(r"(?<=[-+*^/%(dE])-(?=[\d.sctlgf])")
implict_multi = re.compile(r"(?:ns|[ei)])(?=[\d.(peasctlgf])|[)\d](?=[peasctlgf(])")
pseudo_num    = re.compile(r"[\d.]+")
negation      = re.compile(r"-(?=\()")
lcm_gcd       = re.compile(r"(?:lcm|gcd)\(-?\d+(?:,-?\d+)*\)")
extra         = re.compile(r"sin|cos|tan|lcm|gcd|ln|log|fact|sqrt")

def validate(expression):
    expression = "".join(symbols.findall(expression))

    if any(num.count(".") > 1 or num == "." for num in pseudo_num.findall(expression)):
        raise Exception("invalid decimal format")

    stack = []
    for char in expression:
        if char == "(":
            stack.append(char)
        elif char == ")":
            if not stack or stack[-1] != "(":
                raise Exception("invalid parenthesis order")
            stack.pop()
    if stack:
        raise Exception("invalid parenthesis count")

    expression = f"({expression})".replace("//", "d")
    expression = negation.sub("-1*", implict_multi.sub(r"\g<0>*", expression))
    expression = expression.replace("e", "2.718281828459045").replace("pi", "3.141592653589793").replace("ans", prev_ans)

    test_exp = lcm_gcd.sub("1", unary_minus.sub("", expression))

    if "lcm" in test_exp or "gcd" in test_exp:
        raise Exception("invalid lcm or gcd arguments")

    if len(operand.findall(test_exp)) - 1 != sum(1 for char in test_exp if char in operators):
        raise Exception("invalid operators and operands count")

    matches = list(re.finditer(extra, expression)) 
    while matches:
        m = matches.pop()
        fn = m.group()
        arg_start = m.end()

        i = arg_start + 1
        c = 1
        while c != 0:
            ch = expression[i]
            c += (ch == "(") - (ch == ")")
            i += 1

        raw_arg = expression[arg_start : i]
        res_arg = map(int, raw_arg[1:-1].split(",")) if fn[1] == "c" else evaluate(raw_arg)

        if fn == "tan" and ((res_arg - 90) / 180).is_integer():
            raise Exception("tan(90 + 180n) tends to infinity")

        expression = expression.replace(f"{fn}{raw_arg}", f"{calc_extra[fn](res_arg):.14f}".rstrip("0").rstrip("."))

    return expression

def evaluate(expression):
    infix = [c if c in all_ops else round(float(c), 14) if "." in c or "E" in c else int(c) for c in tokens.findall(expression)]
    stack = []
    postfix = []

    for char in infix:
        if char == "(":
            stack.append(char)
        elif char == ")":
            while stack[-1] != "(":
                postfix.append(stack.pop())
            stack.pop()
        elif not isinstance(char, str):
            postfix.append(char)
        else:
            while (
                precedence[stack[-1]] > precedence[char]
            ) or (
                    stack[-1] != "^" and precedence[stack[-1]] == precedence[char]
                ):
                postfix.append(stack.pop())
            stack.append(char)

    for char in postfix:
        if not isinstance(char, str):
            stack.append(char)
        else:
            op2 = stack.pop()
            stack.append(calculate[char](stack.pop(), op2))

    result = stack.pop()
    return int(result) if result == int(result) else round(float(result), 14)

print("\nSymbols: +  -  *  /  ^  %  //  (  )  pi  e  E  ans  exit")
print("Functions: sin() cos() tan() ln() log() sqrt() fact() lcm(,) gcd(,)")
prev_ans = ""

while True:
    try:
        expression = input("\nExpression: ")
        if expression == "exit": break

        expression = validate(expression)
        expression = evaluate(expression)

        print(f"Answer: {expression:,.14f}".rstrip("0").rstrip("."))
        prev_ans = str(expression)

    except Exception as error:
        print(f"Error: {error}!")
