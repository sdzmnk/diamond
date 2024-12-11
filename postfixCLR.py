
postfixCodeCLR = []
tl = "    "

def suffixTypeCLR(Type):
    if Type == 'int':
        return 'i4'
    elif Type == 'float':
        return 'r4'

def relopCLR(lex):
    global relopCLR
    if lex == '<' : relopCLR = 'clt'
    if lex == '>': relopCLR = 'cgt'
    if lex == '==': relopCLR = 'ceq'
    return relopCLR

def postfixCLR_codeGen(case,toTran):
    global val
    if case == 'lval':
        lex = toTran
        # postfixCodeCLR.append(tl + 'ldloca'+ tb('ldloca') + lex)
        postfixCodeCLR.append(tl + 'ldloca'+ tl + lex)
    elif case == '=':
        typeVar = toTran
        postfixCodeCLR.append(tl + 'stind.' + suffixTypeCLR(typeVar))
    elif case == '+':
        postfixCodeCLR.append(tl + 'add')
    elif case == '-':
        postfixCodeCLR.append(tl + 'sub')
    elif case == '**':
        postfixCodeCLR.append(tl + 'pow')
    elif case == '*':
        postfixCodeCLR.append(tl + 'mul')
    elif case == '/':
        postfixCodeCLR.append(tl + 'div')
    elif case == 'rval':
        lex = toTran
        # postfixCodeCLR.append(tl + 'ldloca'+ tb('ldloca') + lex)
        postfixCodeCLR.append(tl + 'ldloc' + tl + lex)
    elif case == 'const':
        lex, typeVar = toTran
        postfixCodeCLR.append(tl + 'ldc.' + suffixTypeCLR(typeVar)+ tl + lex)
    elif case == 'boolval':
        if toTran == 'true':
            val = '1'
        elif toTran == 'false':
            val = '0'
        postfixCodeCLR.append(tl + 'ldc.i4' + val)
    elif case == 'rel_op':
        lex = toTran
        relop = relopCLR(lex)
        postfixCodeCLR.append(tl+relop)
    elif case == 'jf':
        lex = toTran
        postfixCodeCLR.append(tl + 'brfalse' + lex)
    elif case == 'jump':
        lex = toTran
        postfixCodeCLR.append(tl + 'br' + lex)
    elif case == 'label':
        lex = toTran + ':'
        postfixCodeCLR.append(lex)
    return True

