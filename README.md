# Simple Math Evaluator

A basic math evaluator written in Python that combines **Regular Expressions** for syntax validation/preprocessing and the **Shunting-Yard algorithm** for Postfix-based calculation.

## 🚀 Key Features

* **Implicit Multiplication:** `sin(-(45 - 90))(pie + .9)` as `sin(-1*(45 - 90))*(pi*e+0.9)`.
* **Scientific Notation:** `1.2E-5`, `-3.7E3` etc.
* **Number Theory:** includes `lcm(a,b,...)` and `gcd(a,b,...)`.
* **Trigonometry & Logarithms:** supports `sin`, `cos`, `tan` (degree-based), `ln`, and `log`.
* **Error Handling:** Custom validation for mismatched parentheses and more.

## 🛠️ The Architecture

The evaluator works in two distinct phases:

### Validation & Preprocessing
Before calculation, the script uses `re` to:
* Ignore unsupported characters and symbols.
* Standardize operators (e.g. converting `//` to `d` for easier single-char tokenization).
* Inject multiplication symbols where implicit (e.g. `2e(` becomes `2*e*(`).
* Replace constants and previous answer like `pi`, `e` and `ans`.
* Solve "extra" functions and replace them with their literal values.

### Postfix Conversion & Evaluation
Once the string is completely arithmetic, it is converted to **Reverse Polish Notation (RPN)**.
* **Shunting-Yard:** Handles operator precedence.
* **Stack Evaluation:** Processes the postfix list to arrive at the final result.

## 📋 Supported Symbols & Functions

| Category | Tokens |
| :--- | :--- |
| **Basic Operators** | `+`, `-`, `*`, `/`, `^`, `//` (floor division), `%` (modulo division) |
| **"Extra" Functions** | `sin`, `cos`, `tan`, `ln`, `log`, `sqrt`, `fact` (factorial) |
| **Number Theory** | `lcm(a,b)`, `gcd(a,b)` (`int` arguments only)|
| **Constants** | `pi`, `e`, `ans` (previous result) |

## 💻 Usage

Run the script directly to enter the interactive REPL:
```bash
python calc.py
python eval.py
```

### Example
```bash
Expression: pie
Answer: 8.53973422267357

Expression: tan(5 * 3 * 12 / 2)
Error: tan(90 + 180n) tends to infinity!

Expression: ans - .0097
Answer: 8.53003422267357

Expression: .1 + 0.2
Answer: 0.3

Expression: exit
```
