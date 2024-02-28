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
    OP_NOT = iota()
    OP_AND = iota()
    OP_OR = iota()
    OP_XOR = iota()
    OP_BOOL_VAL = iota()

    OP_DISPLAY = iota()
    OP_DUP = iota()
    OP_SWAP = iota()
    OP_DROP = iota()

    OP_UNKNOWN = iota()

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
        case Ops.OP_NOT: return "!"
        case Ops.OP_AND: return "and"
        case Ops.OP_OR: return "or"
        case Ops.OP_XOR: return "xor"
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

def nott():
    return (Ops.OP_NOT, )

def andd():
    return (Ops.OP_AND, )

def orr():
    return (Ops.OP_OR, )

def xor():
    return (Ops.OP_XOR, )

def boolval(val):
    return (Ops.OP_BOOL_VAL, val)

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

        # Boolean/logic
        case "=": return eq()
        case "!=": return neq()
        case "<": return less()
        case "<=": return lesseq()
        case ">": return grtr()
        case ">=": return grtreq()
        case "!": return nott()
        case "and": return andd()
        case "or": return orr()
        case "xor": return xor()
        case "true": return boolval(True)
        case "false": return boolval(False)

        # Builtins
        case "dup": return dup()
        case "swap": return swap()
        case "drop": return drop()

        case _: return (Ops.OP_UNKNOWN, word)


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
                if len(stack) < 2:
                    die(f"Two operands are required for '{op_str(op[0])}'")
                b = stack.pop()
                a = stack.pop()
                stack.append(a + b)
            case Ops.OP_SUB:
                if len(stack) < 2:
                    die(f"Two operands are required for '{op_str(op[0])}'")
                b = stack.pop()
                a = stack.pop()
                stack.append(a - b)
            case Ops.OP_MUL:
                if len(stack) < 2:
                    die(f"Two operands are required for '{op_str(op[0])}'")
                b = stack.pop()
                a = stack.pop()
                stack.append(a * b)
            case Ops.OP_DIV:
                if len(stack) < 2:
                    die(f"Two operands are required for '{op_str(op[0])}'")
                b = stack.pop()
                a = stack.pop()
                if b == 0:
                    die("Division by 0 is not allowed", op[0])
                stack.append(a // b)
            case Ops.OP_MOD:
                if len(stack) < 2:
                    die(f"Two operands are required for '{op_str(op[0])}'")
                b = stack.pop()
                a = stack.pop()
                if b == 0:
                    die("Modulo a % 0 is not allowed", op[0])
                stack.append(a % b)
            case Ops.OP_POW:
                if len(stack) < 2:
                    die(f"Two operands are required for '{op_str(op[0])}'")
                b = stack.pop()
                a = stack.pop()
                stack.append(a ** b)
            case Ops.OP_DISPLAY:
                if len(stack) <= 0:
                    print()
                else:
                    a = stack.pop()
                    print(("true" if a else "false") if type(a) == bool else a)

            # Boolean/logic
            case Ops.OP_EQUAL:
                if len(stack) < 2:
                    die(f"Two operands are required for '{op_str(op[0])}'")
                b = stack.pop()
                a = stack.pop()
                stack.append(a == b)
            case Ops.OP_NEQUAL:
                if len(stack) < 2:
                    die(f"Two operands are required for '{op_str(op[0])}'")
                b = stack.pop()
                a = stack.pop()
                stack.append(a != b)
            case Ops.OP_LESS:
                if len(stack) < 2:
                    die(f"Two operands are required for '{op_str(op[0])}'")
                b = stack.pop()
                a = stack.pop()
                stack.append(a < b)
            case Ops.OP_LESSEQ:
                if len(stack) < 2:
                    die(f"Two operands are required for '{op_str(op[0])}'")
                b = stack.pop()
                a = stack.pop()
                stack.append(a <= b)
            case Ops.OP_GRTR:
                if len(stack) < 2:
                    die(f"Two operands are required for '{op_str(op[0])}'")
                b = stack.pop()
                a = stack.pop()
                stack.append(a > b)
            case Ops.OP_GRTREQ:
                if len(stack) < 2:
                    die(f"Two operands are required for '{op_str(op[0])}'")
                b = stack.pop()
                a = stack.pop()
                stack.append(a >= b)

            case Ops.OP_NOT:
                if len(stack) < 1:
                    die(f"One operand is required for '{op_str(op[0])}'")
                a = stack.pop()
                stack.append(not a)
            case Ops.OP_AND:
                if len(stack) < 2:
                    die(f"Two operands are required for '{op_str(op[0])}'")
                b = stack.pop()
                a = stack.pop()
                pushb = bool(a) and bool(b)
                stack.append(pushb)
            case Ops.OP_OR:
                if len(stack) < 2:
                    die(f"Two operands are required for '{op_str(op[0])}'")
                b = stack.pop()
                a = stack.pop()
                pushb = bool(a) or bool(b)
                stack.append(pushb)
            case Ops.OP_XOR:
                if len(stack) < 2:
                    die(f"Two operands are required for '{op_str(op[0])}'")
                b = stack.pop()
                a = stack.pop()
                pushb = bool(a)^bool(b)
                stack.append(pushb)
            case Ops.OP_BOOL_VAL:
                stack.append(op[1])

            # Builtins
            case Ops.OP_DUP:
                if len(stack) <= 0:
                    die("Stack is empty, cannot dup")
                stack.append(stack[-1])
            case Ops.OP_SWAP:
                if len(stack) < 2:
                    die("Not enough items to swap")
                stack[-1], stack[-2] = stack[-2], stack[-1]
            case Ops.OP_DROP:
                if len(stack) <= 0:
                    die("Stack is empty, cannot drop")
                stack.pop()

            # Unknown
            case Ops.OP_UNKNOWN:
                die(f"Unknown word '{op[1]}'")

program = load_program_from_file(program_path)
interpret_program(program)
