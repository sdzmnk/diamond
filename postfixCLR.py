from Tools.scripts.make_ctype import values

postfixCodeCLR = []
tl = "    "

def suffixTypeCLR(Type):
    if Type == 'int':
        return 'i4'
    elif Type == 'float':
        return 'r4'

# def relopCLR(lex):
#     global relopCLR
#     if lex == '<' : relopCLR = 'clt'
#     if lex == '>': relopCLR = 'cgt'
#     if lex == '==': relopCLR = 'ceq'
#     if lex == '<=': relopCLR = 'clt'
#     if lex == '>=': relopCLR = 'cgt'
#     return relopCLR

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
        values=""
        values += tl + 'call float64 [mscorlib]System.Math::Pow(float64, float64)\n'  # Вызываем Pow
        values += tl + 'conv.r4\n'
        postfixCodeCLR.append(values)

    elif case == '*':
        postfixCodeCLR.append(tl + 'mul')
    elif case == '/':
        postfixCodeCLR.append(tl + 'div')
    elif case == 'neg_op':
        postfixCodeCLR.append(tl + 'neg')

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

        relopCLR = ''
        if lex == '<': relopCLR = 'clt'
        if lex == '>': relopCLR = 'cgt'
        if lex == '==': relopCLR = 'ceq'
        if lex == '<=': relopCLR = 'clt'
        if lex == '>=': relopCLR = 'cgt'
        postfixCodeCLR.append(tl+relopCLR)

    elif case == 'jf':
        lex = toTran
        postfixCodeCLR.append(tl + 'brfalse' + tl + lex)
    elif case == 'jump':
        lex = toTran
        postfixCodeCLR.append(tl + 'br' + tl + lex)
    elif case == 'label':
        lex = toTran + ':'
        postfixCodeCLR.append(lex)

    elif case == 'out_op':
        values = ""
        lex = toTran

        tp = "int"
        tp += '32'
        values += "\t" + "ldloc  " + lex + "\n"
        values += "\t" + "call void [mscorlib]System.Console::WriteLine(" + tp + ") \n"

        postfixCodeCLR.append(values)

    elif case == 'out':
        values = ""
        lex = toTran
        values += "\tldstr \"" + lex + "\"\n"
        values += "\tcall void [mscorlib]System.Console::Write(string) \n"

        postfixCodeCLR.append(values)

    elif case == 'input':
        values = ""
        lex, Type = toTran
        if Type == 'int':
            values += "\t" + 'ldstr "' + lex + ' -> "\n'
            values += tl + ' call void [mscorlib]System.Console::Write(string)\n'
            values+= tl + ' call string [mscorlib]System.Console::ReadLine()\n'
            values+=tl + ' call int32 [mscorlib]System.Convert::ToInt32(string)\n'
            values += tl + ' stloc ' + lex + '\n'
        else:
            values += "\t" + 'ldstr "' + lex + ' -> "\n'
            values += tl + ' call void [mscorlib]System.Console::Write(string)\n'
            values += tl + ' call string [mscorlib]System.Console::ReadLine()\n'
            values += tl + ' call float32 [mscorlib]System.Convert::ToSingle(string)\n'
            values += tl + ' stloc ' + lex + '\n'
        postfixCodeCLR.append(values)

    return True

