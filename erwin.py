import math
import sys

# erwin interpreter
# by las-r

class QuantumCollapseError(Exception):
    pass

class TokenStream:
    def __init__(self, tokens):
        self.tokens = tokens
        self.i = 0
        
    def push(self):
        token = self.tokens[self.i]
        self.i += 1
        return token
    
    def can_push(self):
        return self.i < len(self.tokens)

    def peek(self, offset=0):
        if self.i + offset >= len(self.tokens):
            return None
        return self.tokens[self.i + offset]

def lex(code):
    tokens = []
    for line in code.splitlines():
        if "#" in line:
            line = line.split("#")[0]
        words = line.split()
        for w in words:
            try:
                if "." in w:
                    tokens.append(float(w))
                else:
                    tokens.append(int(w))
            except ValueError:
                tokens.append(w)
    return tokens

def evaluate(stream, lvalues):
    expr = stream.push()
    
    if isinstance(expr, (int, float)):
        return expr
    
    if expr in lvalues:
        return lvalues[expr]
    
    if expr == "not": return not evaluate(stream, lvalues)
    if expr == "and": return evaluate(stream, lvalues) and evaluate(stream, lvalues)
    if expr == "or": return evaluate(stream, lvalues) or evaluate(stream, lvalues)
    if expr == "eq": return evaluate(stream, lvalues) == evaluate(stream, lvalues)
    if expr == "ls": return evaluate(stream, lvalues) < evaluate(stream, lvalues)
    if expr == "gr": return evaluate(stream, lvalues) > evaluate(stream, lvalues)
    if expr == "els": return evaluate(stream, lvalues) <= evaluate(stream, lvalues)
    if expr == "egr": return evaluate(stream, lvalues) >= evaluate(stream, lvalues)
    
    if expr == "add": return evaluate(stream, lvalues) + evaluate(stream, lvalues)
    if expr == "sub":
        left = evaluate(stream, lvalues)
        right = evaluate(stream, lvalues)
        return left - right
    if expr == "mul": return evaluate(stream, lvalues) * evaluate(stream, lvalues)
    if expr == "div":
        left = evaluate(stream, lvalues)
        right = evaluate(stream, lvalues)
        return left / right
    if expr == "pow":
        left = evaluate(stream, lvalues)
        right = evaluate(stream, lvalues)
        return left ** right
    
    if expr == "floor": return math.floor(evaluate(stream, lvalues))
    if expr == "ceil": return math.ceil(evaluate(stream, lvalues))
    
    raise Exception(f"'{expr}' could not be evaluated.")

entanglements = {}

def apply_entanglement(base_val, op, modifier):
    if op == "add": return base_val + modifier
    if op == "sub": return base_val - modifier
    if op == "mul": return base_val * modifier
    if op == "div": return base_val / modifier
    if op == "pow": return base_val ** modifier
    return base_val

def solve(stream, values):
    lvalues = values.copy()
    
    while stream.can_push():
        cmd = stream.push()
        
        if cmd == "LET":
            vname = stream.push()
            if stream.peek() == "super":
                stream.push()
                low = int(evaluate(stream, lvalues))
                high = int(evaluate(stream, lvalues))
                pli = stream.i
                for poss in range(low, high + 1):
                    lvalues[vname] = poss
                    if vname in entanglements:
                        for target_var, op, modifier in entanglements[vname]:
                            lvalues[target_var] = apply_entanglement(poss, op, modifier)
                    try:
                        stream.i = pli
                        return solve(stream, lvalues)
                    except QuantumCollapseError as e:
                        if "-i" in sys.argv:
                            print(f"INTERCEPTION ON {vname}={poss}: {e}")
                        continue
                raise QuantumCollapseError()
            else:
                lvalues[vname] = evaluate(stream, lvalues)
                
        elif cmd == "ENT":
            target_var = stream.push()
            source_var = stream.push()
            op = stream.push()
            modifier = evaluate(stream, lvalues)
            if source_var not in entanglements:
                entanglements[source_var] = []
            entanglements[source_var].append((target_var, op, modifier))
            if source_var in lvalues:
                lvalues[target_var] = apply_entanglement(lvalues[source_var], op, modifier)
        
        elif cmd == "PEP":
            count = int(evaluate(stream, lvalues))
            seen = []
            for _ in range(count):
                vname = stream.push()
                val = lvalues.get(vname)
                if val in seen:
                    raise QuantumCollapseError("Exclusion principle violated: Duplicate states detected.")
                seen.append(val)
        
        elif cmd == "CHK":
            cond = evaluate(stream, lvalues)
            if not cond:
                raise QuantumCollapseError("Reality collapse: constraint violation.")
        
        elif cmd == "OBS":
            vname = stream.push()
            print(f"{vname} = {lvalues.get(vname, 'UNDEFINED')}")
            
        elif cmd == "MUT":
            vname = stream.push()
            if vname in lvalues:
                del lvalues[vname]
                
        else:
            raise Exception(f"'{cmd}' could not be solved.")
            
    return lvalues

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python erwin.py <file.cat> [-i]")
        sys.exit(1)
        
    with open(sys.argv[1]) as f:
        code = f.read()
        
    tokens = lex(code)
    stream = TokenStream(tokens)
    try:
        solve(stream, {})
    except QuantumCollapseError:
        print("Error: Total Quantum Collapse. Reality is unsustainable.")