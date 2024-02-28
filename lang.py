from enum import IntEnum
from sys import argv

stack = []
iota_c = -1

def die(msg):
    print(f"error: {msg}"); exit(1)

if len(argv) < 2:
    die("Missing filename argument")

program_path = argv[1]
source = open(program_path).readlines()

def iota():
    global iota_c

    iota_c += 1
    return iota_c

class Ops(IntEnum):
    OP_PUSH = iota()
    OP_ADD = iota()
    OP_SUB = iota()
    OP_MUL = iota()
    OP_DIV = iota()
    OP_MOD = iota()
    OP_POW = iota()

    OP_EQUAL = iota()
    OP_NEQUAL = iota()
    OP_LESS = iota()
    OP_LESSEQ = iota()
    OP_GRTR = iota()
    OP_GRTREQ = iota()

    OP_DISPLAY = iota()
    OP_DUP = iota()
    OP_SWAP = iota()
    OP_DROP = iota()

def op_str(op):
    match op:
        case Ops.OP_PUSH: return op # we know it's numerical
        case Ops.OP_ADD: return "+"
        case Ops.OP_SUB: return "-"
        case Ops.OP_MUL: return "*"
        case Ops.OP_DIV: return "/"
        case Ops.OP_MOD: return "mod"
        case Ops.OP_POW: return "^"
        case Ops.OP_EQUAL: return "="
        case Ops.OP_NEQUAL: return "!="
        case Ops.OP_LESS: return "<"
        case Ops.OP_LESSEQ: return "<="
        case Ops.OP_GRTR: return ">"
        case Ops.OP_GRTREQ: return ">="
        case Ops.OP_DISPLAY: return "."
        case Ops.OP_DUP: return "dup"
        case Ops.OP_SWAP: return "swap"
        case Ops.OP_DROP: return "drop"

def push(x):
    return (Ops.OP_PUSH, x)

def add():
    return (Ops.OP_ADD, )

def sub():
    return (Ops.OP_SUB, )

def mul():
    return (Ops.OP_MUL, )

def div():
    return (Ops.OP_DIV, )

def mod():
    return (Ops.OP_MOD, )

def poww():
    return (Ops.OP_POW, )

def display():
    return (Ops.OP_DISPLAY, )

def dup():
    return (Ops.OP_DUP, )

def swap():
    return (Ops.OP_SWAP, )

def drop():
    return (Ops.OP_DROP, )

def eq():
    return (Ops.OP_EQUAL, )

def neq():
    return (Ops.OP_NEQUAL, )

def less():
    return (Ops.OP_LESS, )

def lesseq():
    return (Ops.OP_LESSEQ, )

def grtr():
    return (Ops.OP_GRTR, )

def grtreq():
    return (Ops.OP_GRTREQ, )

def op_from_word(word):
    if word.isnumeric():
        return push(int(word))

    match word:
        # Operators
        case "+": return add()
        case "-": return sub()
        case "*": return mul()
        case "/": return div()
        case "mod": return mod()
        case "^": return poww()
        case ".": return display()

        # Boolean
        case "=": return eq()
        case "!=": return neq()
        case "<": return less()
        case "<=": return lesseq()
        case ">": return grtr()
        case ">=": return grtreq()

        # Builtins
        case "dup": return dup()
        case "swap": return swap()
        case "drop": return drop()

def load_program_from_str(inpt):
    return [op_from_word(word) for word in inpt.split()]

def load_program_from_file(path):
    with open(path, "r") as f:
        return load_program_from_str(f.read())

def interpret_program(prog):
    for op in prog:
        match op[0]:
            # Operators
            case Ops.OP_PUSH:
                stack.append(op[1])
            case Ops.OP_ADD:
                b = stack.pop()
                a = stack.pop()
                stack.append(a + b)
            case Ops.OP_SUB:
                b = stack.pop()
                a = stack.pop()
                stack.append(a - b)
            case Ops.OP_MUL:
                b = stack.pop()
                a = stack.pop()
                stack.append(a * b)
            case Ops.OP_DIV:
                b = stack.pop()
                a = stack.pop()
                if b == 0:
                    die_interpreter("Division by 0 is not allowed", op[0])
                stack.append(a // b)
            case Ops.OP_MOD:
                b = stack.pop()
                a = stack.pop()
                if b == 0:
                    die_interpreter("Modulo a % 0 is not allowed", op[0])
                stack.append(a % b)
            case Ops.OP_POW:
                b = stack.pop()
                a = stack.pop()
                stack.append(a ** b)
            case Ops.OP_DISPLAY:
                if len(stack) <= 0:
                    die_interpreter("Stack is empty, cannot display", op[0])

                print(stack.pop())

            # Boolean expressions
            case Ops.OP_EQUAL:
                b = stack.pop()
                a = stack.pop()
                stack.append(a == b)
            case Ops.OP_NEQUAL:
                b = stack.pop()
                a = stack.pop()
                stack.append(a != b)
            case Ops.OP_LESS:
                b = stack.pop()
                a = stack.pop()
                stack.append(a < b)
            case Ops.OP_LESSEQ:
                b = stack.pop()
                a = stack.pop()
                stack.append(a <= b)
            case Ops.OP_GRTR:
                b = stack.pop()
                a = stack.pop()
                stack.append(a > b)
            case Ops.OP_GRTREQ:
                b = stack.pop()
                a = stack.pop()
                stack.append(a >= b)

            # Builtins
            case Ops.OP_DUP:
                if len(stack) <= 0:
                    die_interpreter("Stack is empty, cannot dup", op[0])
                stack.append(stack[-1])
            case Ops.OP_SWAP:
                if len(stack) < 2:
                    die_interpreter("Not enough items to swap", op[0])
                stack[-1], stack[-2] = stack[-2], stack[-1]
            case Ops.OP_DROP:
                if len(stack) <= 0:
                    die_interpreter("Stack is empty, cannot drop", op[0])
                stack.pop()

program = load_program_from_file(program_path)
interpret_program(program)
