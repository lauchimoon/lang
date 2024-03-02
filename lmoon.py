from enum import IntEnum
import sys
import string

stack = []
iota_c = -1
variables = {}
builtin_ops = [
    "true", "false", "mod", "and", "or", "xor",
    "if", "else", "end", "dup", "swap", "drop",
    "while", "do", "strb", "stre",

    ".", "+", "-", "*", "/", "^", "==", "!=",
    "<", "<=", ">", ">=", "!", "=",
]

def die(msg):
    print(f"error: {msg}"); exit(1)

argv = sys.argv
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

    OP_SYMBOL = iota()
    OP_SET = iota()

    OP_WHILE = iota()
    OP_DO = iota()

    OP_STRB = iota()
    OP_STRE = iota()
    OP_STRING = iota()

    OP_UNKNOWN = iota()

def op_str(op):
    match op:
        case Ops.OP_PUSH: return op
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
        case Ops.OP_SYMBOL: return op
        case Ops.OP_SET: return "="
        case Ops.OP_WHILE: return "while"
        case Ops.OP_DO: return "do"
        case Ops.OP_STRB: return "strb"
        case Ops.OP_STRE: return "stre"

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

def symbol(name):
    return (Ops.OP_SYMBOL, name, )

def sett():
    return (Ops.OP_SET, )

def whilee():
    return (Ops.OP_WHILE, )

def do():
    return (Ops.OP_DO, )

def strb():
    return (Ops.OP_STRB, )

def stre():
    return (Ops.OP_STRE, )

def stringg(text):
    return (Ops.OP_STRING, text, )

def isalnum(s):
    return s.isprintable()

def op_from_word(word):
    if word.isnumeric():
        return push(int(word))

    if isalnum(word) and word not in builtin_ops:
        return push(symbol(word))

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

        # Variables
        case "=": return sett()

        # Loops
        case "while": return whilee()
        case "do": return do()

        # Strings (very hacky)
        case "strb": return strb()
        case "stre": return stre()

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
                if prog[block_idx][0] == Ops.OP_IF or prog[block_idx][0] == Ops.OP_ELSE:
                    prog[block_idx] = (prog[block_idx][0], i) # if or else references end
                    prog[i] = (Ops.OP_END, i + 1)
                elif prog[block_idx][0] == Ops.OP_DO:
                    prog[i] = (Ops.OP_END, prog[block_idx][1]) # do references end
                    prog[block_idx] = (Ops.OP_DO, i + 1)
            case Ops.OP_WHILE:
                stck.append(i)
            case Ops.OP_DO:
                while_idx = stck.pop()
                prog[i] = (Ops.OP_DO, while_idx)
                stck.append(i)
            case Ops.OP_STRB:
                stck.append(i)
            case Ops.OP_STRE:
                begin_idx = stck.pop()
                prog[i] = (Ops.OP_STRE, begin_idx + 1)

    return prog

def prepare_strings(prog):
    stck = []
    i = 0

    while i < len(prog):
        op = prog[i]
        match op[0]:
            case Ops.OP_STRB:
                stck.append(i)
            case Ops.OP_STRE:
                begin_idx = stck.pop() + 1
                text_separate = []
                for _ in range(begin_idx, i):
                    i -= 1
                    x = prog.pop(i)
                    text_separate.append(x)

                text_separate.reverse()
                text_str = " ".join([x[1][1] for x in text_separate])
                prog[i] = stringg(text_str)

        i += 1

    return prog

def load_program_from_str(inpt):
    return prepare_strings(crossreference_blocks([op_from_word(word) for word in inpt.split()]))

def load_program_from_file(path):
    with open(path, "r") as f:
        return load_program_from_str(f.read())

def check_if_symbol(arg1, arg2, operator):
    a = 0
    b = 0
    ret_val = 0

    if arg1 is not None:
        if type(arg1) == tuple:
            if arg1[0] == Ops.OP_SYMBOL:
                a = variables[arg1[1]]
        else:
            a = arg1

    if arg2 is not None:
        if type(arg2) == tuple:
            if arg2[0] == Ops.OP_SYMBOL:
                b = variables[arg2[1]]
        else:
            b = arg2

    match operator:
        case Ops.OP_ADD: ret_val = a + b
        case Ops.OP_SUB: ret_val = a - b
        case Ops.OP_MUL: ret_val = a * b
        case Ops.OP_DIV:
            if b == 0:
                die("division by 0 is not allowed")
            ret_val = a // b
        case Ops.OP_POW: ret_val = a ** b
        case Ops.OP_MOD:
            if b == 0:
                die("modulo by 0 is not allowed")
            ret_val = a % b
        case Ops.OP_POW: ret_val = a ** b

        case Ops.OP_EQUAL: ret_val = (a == b)
        case Ops.OP_NEQUAL: ret_val = (a != b)
        case Ops.OP_LESS: ret_val = (a < b)
        case Ops.OP_LESSEQ: ret_val = (a <= b)
        case Ops.OP_GRTR: ret_val = (a > b)
        case Ops.OP_GRTREQ: ret_val = (a >= b)
        case Ops.OP_NOT: ret_val = not a
        case Ops.OP_AND: ret_val = bool(a) and bool(b)
        case Ops.OP_OR: ret_val = bool(a) or bool(b)
        case Ops.OP_XOR: ret_val = bool(a) ^ bool(b)
        case Ops.OP_BOOL_VAL: ret_val = arg1

    return ret_val

def perform_operator(operator):
    if len(stack) < 2:
        die(f"Two operands are required for '{op_str(op[0])}'")

    b = stack.pop()
    a = stack.pop()
    ret = check_if_symbol(a, b, operator)
    stack.append(ret)

def interpret_program(prog):
    len_prog = len(prog)
    i = 0

    while i < len_prog:
        op = prog[i]
        match op[0]:
            # Operators
            case Ops.OP_PUSH:
                stack.append(op[1])
                i += 1
            case Ops.OP_ADD:
                perform_operator(op[0])
                i += 1
            case Ops.OP_SUB:
                perform_operator(op[0])
                i += 1
            case Ops.OP_MUL:
                perform_operator(op[0])
                i += 1
            case Ops.OP_DIV:
                perform_operator(op[0])
                i += 1
            case Ops.OP_MOD:
                perform_operator(op[0])
                i += 1
            case Ops.OP_POW:
                perform_operator(op[0])
                i += 1

            # Boolean/logic
            case Ops.OP_EQUAL:
                perform_operator(op[0])
                i += 1
            case Ops.OP_NEQUAL:
                perform_operator(op[0])
                i += 1
            case Ops.OP_LESS:
                perform_operator(op[0])
                i += 1
            case Ops.OP_LESSEQ:
                perform_operator(op[0])
                i += 1
            case Ops.OP_GRTR:
                perform_operator(op[0])
                i += 1
            case Ops.OP_GRTREQ:
                perform_operator(op[0])
                i += 1

            case Ops.OP_NOT:
                if len(stack) < 1:
                    die(f"One operand is required for '{op_str(op[0])}'")
                a = stack.pop()
                ret = check_if_symbol(a, None, op[0])
                stack.append(ret)
                i += 1
            case Ops.OP_AND:
                perform_operator(op[0])
                i += 1
            case Ops.OP_OR:
                perform_operator(op[0])
                i += 1
            case Ops.OP_XOR:
                perform_operator(op[0])
                i += 1
            case Ops.OP_BOOL_VAL:
                arg = op[1]
                ret = check_if_symbol(arg, None, op[0])
                stack.append(ret)
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
                i = op[1]

            # Variables
            case Ops.OP_SYMBOL:
                i += 1
            case Ops.OP_SET:
                value = stack.pop()
                name = stack.pop()
                if type(value) == tuple and value[0] == Ops.OP_SYMBOL:
                    variables[name[1]] = variables[value[1]]
                else:
                    variables[name[1]] = value

                i += 1

            # Loops
            case Ops.OP_WHILE:
                i += 1
            case Ops.OP_DO:
                cond = stack.pop()
                if cond:
                    i += 1
                else:
                    if len(op) < 2:
                        die("while block missing end")
                    i = op[1]

            # Strings (very hacky)
            case Ops.OP_STRB:
                i += 1
            case Ops.OP_STRING:
                stack.append(op[1])
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
            case Ops.OP_DISPLAY:
                if len(stack) <= 0:
                    print()
                else:
                    a = stack.pop()
                    if type(a) == tuple and a[0] == Ops.OP_SYMBOL:
                        var = variables[a[1]]
                        print(("true" if var else "false") if type(var) == bool else var)
                    elif type(a) == str:
                        raw = ""
                        j = 0
                        while j < len(a):
                            c = a[j]
                            if a[j] == '\\':
                                match a[j + 1]:
                                    case 'n': raw += '\n'; j += 2
                                    case '\\': raw += '\\'
                            else:
                                raw += c

                            j += 1

                        print(raw, end='')
                    else:
                        print(("true" if a else "false") if type(a) == bool else a)

                i += 1

            # Unknown
            case Ops.OP_UNKNOWN:
                word = op[1]
                die(f"Unknown word '{word}'")

program = load_program_from_file(program_path)
#print(program)
interpret_program(program)
