import re

div_ops   = { "/", "d", "%" }
operators = { "+", "-", "*", "^", *div_ops }
all_ops   = { "(", ")", *operators }

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
symbols       = re.compile(r"[-+*^/%()\d.eE]+|pi|ans")
operand       = re.compile(r"\d*\.?\d+(?:E-?\d+)?")
unary_minus   = re.compile(r"(?<=[-+*^/%(dE])-(?=[\d.])")
implict_multi = re.compile(r"[sei)](?=[\d.(pea])|[)\d](?=[pea(])")
pseudo_num    = re.compile(r"[\d.]+")
negation      = re.compile(r"-(?=\()")

def evaluate(expression):
    expression = "".join(symbols.findall(expression))

    if any(num.count(".") > 1 or num == "." for num in pseudo_num.findall(expression)):
        raise Exception("Invalid Decimal Format")

    stack = []
    for char in expression:
        if char == "(":
            stack.append(char)
        elif char == ")":
            if not stack or stack[-1] != "(":
                raise Exception("Invalid Parenthesis Order")
            stack.pop()
    if stack:
        raise Exception("Invalid Parenthesis Count")

    expression = f"({expression})".replace("//", "d") 
    expression = negation.sub("-1*", implict_multi.sub(r"\g<0>*", expression))
    expression = expression.replace("e", "2.718281828459045").replace("pi", "3.141592653589793").replace("ans", prev_ans)

    if len(operand.findall(expression)) - 1 != sum(1 for char in unary_minus.sub("", expression) if char in operators):
        raise Exception("Invalid Operators & Operands Count")

    infix = [c if c in all_ops else float(c) for c in tokens.findall(expression)]
    stack = []
    postfix = []

    for char in infix:
        if char == "(":
            stack.append(char)
        elif char == ")":
            while stack[-1] != "(":
                postfix.append(stack.pop())
            stack.pop()
        elif isinstance(char, float):
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
        if isinstance(char, float):
            stack.append(char)
        else:
            op2 = stack.pop()
            stack.append(calculate[char](stack.pop(), op2))

    return stack.pop()

print("\nSymbols: +  -  *  /  ^  %  //  (  )  pi  e  E  ans  exit")
prev_ans = ""

while True:
    try:
        expression = input("\nExpression: ")
        if expression == "exit": break
        result = evaluate(expression)

        print(f"Answer: {result:,.15f}".rstrip("0").rstrip("."))
        prev_ans = str(result)

    except Exception as error:
        print(f"Error: {error}!")
