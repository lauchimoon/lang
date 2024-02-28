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

    OP_IF = iota()
    OP_ELSE = iota()
    OP_END = iota()

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
        case Ops.OP_EQUAL: return "=="
        case Ops.OP_NEQUAL: return "!="
        case Ops.OP_LESS: return "<"
        case Ops.OP_LESSEQ: return "<="
        case Ops.OP_GRTR: return ">"
        case Ops.OP_GRTREQ: return ">="
        case Ops.OP_NOT: return "!"
        case Ops.OP_AND: return "and"
        case Ops.OP_OR: return "or"
        case Ops.OP_XOR: return "xor"
        case Ops.OP_IF: return "if"
        case Ops.OP_ELSE: return "else"
        case Ops.OP_END: return "end"
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

def iff():
    return (Ops.OP_IF, )

def elsee():
    return (Ops.OP_ELSE, )

def end():
    return (Ops.OP_END, )

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
        case "==": return eq()
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

        # Control flow
        case "if": return iff()
        case "else": return elsee()
        case "end": return end()

        # Builtins
        case "dup": return dup()
        case "swap": return swap()
        case "drop": return drop()

        case _: return (Ops.OP_UNKNOWN, word)

def crossreference_blocks(prog):
    stck = []
    for i in range(len(prog)):
        op = prog[i]
        match op[0]:
            case Ops.OP_IF:
                stck.append(i)
            case Ops.OP_ELSE: # if references else
                if_idx = stck.pop()
                prog[if_idx] = (Ops.OP_IF, i + 1) # if gets sent to else block
                stck.append(i)
            case Ops.OP_END:
                block_idx = stck.pop()
                prog[block_idx] = (prog[block_idx][0], i) # if or else references end

    return prog

def load_program_from_str(inpt):
    return crossreference_blocks([op_from_word(word) for word in inpt.split()])

def load_program_from_file(path):
    with open(path, "r") as f:
        return load_program_from_str(f.read())

def interpret_program(prog):
    len_prog = len(prog)
    i = 0
    while i < len_prog:
        op = prog[i]
        match op[0]:
            # Operators
            case Ops.OP_PUSH:
                arg = op[1]
                stack.append(arg)
                i += 1
            case Ops.OP_ADD:
                if len(stack) < 2:
                    die(f"Two operands are required for '{op_str(op[0])}'")
                b = stack.pop()
                a = stack.pop()
                stack.append(a + b)
                i += 1
            case Ops.OP_SUB:
                if len(stack) < 2:
                    die(f"Two operands are required for '{op_str(op[0])}'")
                b = stack.pop()
                a = stack.pop()
                stack.append(a - b)
                i += 1
            case Ops.OP_MUL:
                if len(stack) < 2:
                    die(f"Two operands are required for '{op_str(op[0])}'")
                b = stack.pop()
                a = stack.pop()
                stack.append(a * b)
                i += 1
            case Ops.OP_DIV:
                if len(stack) < 2:
                    die(f"Two operands are required for '{op_str(op[0])}'")
                b = stack.pop()
                a = stack.pop()
                i += 1
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
                i += 1
            case Ops.OP_POW:
                if len(stack) < 2:
                    die(f"Two operands are required for '{op_str(op[0])}'")
                b = stack.pop()
                a = stack.pop()
                stack.append(a ** b)
                i += 1
            case Ops.OP_DISPLAY:
                if len(stack) <= 0:
                    print()
                else:
                    a = stack.pop()
                    print(("true" if a else "false") if type(a) == bool else a)

                i += 1

            # Boolean/logic
            case Ops.OP_EQUAL:
                if len(stack) < 2:
                    die(f"Two operands are required for '{op_str(op[0])}'")
                b = stack.pop()
                a = stack.pop()
                stack.append(a == b)
                i += 1
            case Ops.OP_NEQUAL:
                if len(stack) < 2:
                    die(f"Two operands are required for '{op_str(op[0])}'")
                b = stack.pop()
                a = stack.pop()
                stack.append(a != b)
                i += 1
            case Ops.OP_LESS:
                if len(stack) < 2:
                    die(f"Two operands are required for '{op_str(op[0])}'")
                b = stack.pop()
                a = stack.pop()
                stack.append(a < b)
                i += 1
            case Ops.OP_LESSEQ:
                if len(stack) < 2:
                    die(f"Two operands are required for '{op_str(op[0])}'")
                b = stack.pop()
                a = stack.pop()
                stack.append(a <= b)
                i += 1
            case Ops.OP_GRTR:
                if len(stack) < 2:
                    die(f"Two operands are required for '{op_str(op[0])}'")
                b = stack.pop()
                a = stack.pop()
                stack.append(a > b)
                i += 1
            case Ops.OP_GRTREQ:
                if len(stack) < 2:
                    die(f"Two operands are required for '{op_str(op[0])}'")
                b = stack.pop()
                a = stack.pop()
                stack.append(a >= b)
                i += 1

            case Ops.OP_NOT:
                if len(stack) < 1:
                    die(f"One operand is required for '{op_str(op[0])}'")
                a = stack.pop()
                stack.append(not a)
                i += 1
            case Ops.OP_AND:
                if len(stack) < 2:
                    die(f"Two operands are required for '{op_str(op[0])}'")
                b = stack.pop()
                a = stack.pop()
                pushb = bool(a) and bool(b)
                stack.append(pushb)
                i += 1
            case Ops.OP_OR:
                if len(stack) < 2:
                    die(f"Two operands are required for '{op_str(op[0])}'")
                b = stack.pop()
                a = stack.pop()
                pushb = bool(a) or bool(b)
                stack.append(pushb)
                i += 1
            case Ops.OP_XOR:
                if len(stack) < 2:
                    die(f"Two operands are required for '{op_str(op[0])}'")
                b = stack.pop()
                a = stack.pop()
                pushb = bool(a)^bool(b)
                stack.append(pushb)
                i += 1
            case Ops.OP_BOOL_VAL:
                arg = op[1]
                stack.append(arg)
                i += 1

            # Control flow
            case Ops.OP_IF:
                cond = stack.pop()
                if cond:
                    i += 1
                else:
                    if len(op) < 2:
                        die("if block missing end")
                    i = op[1]
            case Ops.OP_ELSE:
                if len(op) < 2:
                    die("else block missing end")
                i = op[1]
            case Ops.OP_END:
                i += 1

            # Builtins
            case Ops.OP_DUP:
                if len(stack) <= 0:
                    die("Stack is empty, cannot dup")
                stack.append(stack[-1])
                i += 1
            case Ops.OP_SWAP:
                if len(stack) < 2:
                    die("Not enough items to swap")
                stack[-1], stack[-2] = stack[-2], stack[-1]
                i += 1
            case Ops.OP_DROP:
                if len(stack) <= 0:
                    die("Stack is empty, cannot drop")
                stack.pop()
                i += 1

            # Unknown
            case Ops.OP_UNKNOWN:
                word = op[1]
                die(f"Unknown word '{word}'")

program = load_program_from_file(program_path)
#print(program)
interpret_program(program)
