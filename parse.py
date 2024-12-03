from diamond import lex, tableOfConst
from diamond import tableOfSymb

FSuccess = lex()

print('-' * 30)
print('tableOfSymb:{0}'.format(tableOfSymb))
print('-' * 30)

# номер рядка таблиці розбору/лексем/символів ПРОГРАМИ tableOfSymb
numRow = 1

# довжина таблиці символів програми
# він же - номер останнього запису
len_tableOfSymb = len(tableOfSymb)
print(('len_tableOfSymb', len_tableOfSymb))
tableOfVar = {}
tableOfLabel = {}
postfixCode = []
toView = True

# Функція для розбору за правилом
# Program = {Comment | StatementList} end
# читає таблицю розбору tableOfSymb
def parseProgram():
    try:
        parseDeclarList()
        parseToken('begin', 'keyword')
        # Перевіряємо синтаксичну коректність списку інструкцій
        parseStatementList()
        # Очікуємо ключове слово "end" в кінці
        parseToken('finish', 'keyword')
        # повідомити про синтаксичну коректність програми
        print('Parser: Синтаксичний аналіз завершився успішно')
        print('tableOfVar:{0}'.format(tableOfVar))
        print('tableOfLabel:{0}'.format(tableOfLabel))
        print('postfixCode:{0}'.format(postfixCode))
        print('tableOfConst:{0}'.format(tableOfConst))
        return True
    except SystemExit as e:
        # Повідомити про факт виявлення помилки
        print('Parser: Аварійне завершення програми з кодом {0}'.format(e))


def parseDeclarList():
    global numRow
    indent = nextIndt()
    print(indent + 'parseDeclarList():')
    numLine, lex, tok = getSymb()
    while (lex, tok) != ('begin', 'keyword'):  # Доки не зустріли 'begin'
        print(indent + 'в рядку {0} - токен {1}'.format(numLine, (lex, tok)))
        if tok == 'id':  # Якщо токен - це ідентифікатор
            numRow += 1
            parseToken('^', 'type_var')  # Очікуємо знак типу змінної
            numLineT, lexT, tokT = getSymb()
            numRow += 1
            if lexT in ('int', 'float', 'boolval'):  # Якщо тип змінної - int або float
                print(indent + 'в рядку {0} - токен {1}'.format(numLineT, (lexT, tokT)))
                procTableOfVar(numLine, lex, tokT, 'undefined')  # Додаємо змінну в таблицю
            else:
                failParse('неприпустимий тип', (numLineT, lexT, tokT))  # Помилка: неправильний тип
        else:
            failParse('очікувався ідентифікатор', (numLine, lex, tok))  # Помилка: очікувався ідентифікатор

        numLine, lex, tok = getSymb()  # Читання наступного токену




def procTableOfVar(numLine, lexeme, type, value='undefined'):
    indx = tableOfVar.get(lexeme)  # Перевірка на наявність змінної в таблиці
    if indx is None:  # Якщо змінна ще не була оголошена
        indx = len(tableOfVar) + 1  # Додаємо її в таблицю
        tableOfVar[lexeme] = (indx, type, value)
    else:
        failParse('повторне оголошення змінної', (numLine, lexeme, type, value))  # Якщо змінна вже оголошена


def getTypeVar(id):
    try:
        return tableOfVar[id][1]  # Повертаємо тип змінної
    except KeyError:
        return 'undeclared_variable'  # Якщо змінна не знайдена, повертаємо 'undeclared_variable'


def isInitVar(id):
    try:
        # Перевірка на наявність змінної в таблиці
        if tableOfVar[id][2] == 'undefined':  # Якщо змінна має значення "undefined"
            # Змінюємо статус на "assigned"
            tableOfVar[id] = (tableOfVar[id][0], tableOfVar[id][1], 'assigned')
            return True
        elif tableOfVar[id][2] == 'assigned':
            return True
        else:
            return False
    except KeyError:
        return 'undeclared_variable'


def getTypeConst(literal):
    # tableOfConst - словник {literal:(indx,type)}
    return tableOfConst[literal][1]

def getTypeOp(lType, op, rType):
    # Check if types are the same
    typesAreSame = lType == rType or rType==None or lType==None
    # Check if types are arithmetic
    typesArithm = lType in ('int', 'float') and rType in ('int', 'float')
    typesAreDif = lType != rType

    if typesAreSame and typesArithm and op in '+-* /':
        typeRes = lType
    elif typesAreSame and typesArithm and op in ('<', '<=', '>', '>=', '==', '!='):
        typeRes = 'boolval'
    elif op in ('**'):
        typeRes = 'float'
    elif typesAreDif and typesArithm and op in ('<', '<=', '>', '>=', '==', '!='):
        typeRes = 'boolval'
    elif typesAreDif and op == '=':
        typeRes = rType
    elif typesArithm and op in '+-* /':
        if lType == 'int' and rType == 'int':
            typeRes = 'int'
        elif lType == 'int' and rType == 'float':
            typeRes = 'float'
        elif lType == 'float' and rType == 'int':
            typeRes = 'float'
        elif lType == 'float' and rType == 'float':
            typeRes = 'float'
    # elif op == '=' and typesAreSame:
    #     typeRes = 'void'
    elif op == '=' and typesAreSame:
        typeRes = rType
    elif (lType in ('boolval') and rType in ('int', 'float')) or (rType in ('boolval') and lType in ('int', 'float')):
        tpl = (lType,rType)
        failParse('несумісність типів', tpl)
    else:
        typeRes = 'type_error'
    return typeRes

# Функція перевіряє, чи у поточному рядку таблиці розбору зустрілась вказана лексема lexeme з токеном token параметр indent - відступ при виведенні у консоль
def parseToken(lexeme, token):
    # доступ до поточного рядка таблиці розбору
    global numRow

    # відступ збільшити
    indent = nextIndt()

    # якщо всі записи таблиці розбору прочитані,
    # а парсер ще не знайшов якусь лексему
    if numRow > len_tableOfSymb:
        failParse('неочікуваний кінець програми', (lexeme, token, numRow))

    # прочитати з таблиці розбору
    # номер рядка програми, лексему та її токен
    numLine, lex, tok = getSymb()

    # тепер поточним буде наступний рядок таблиці розбору
    numRow += 1

    # чи збігаються лексема та токен таблиці розбору з заданими
    if (lex, tok) == (lexeme, token):
        # вивести у консоль номер рядка програми та лексему і токен
        print(indent + 'parseToken: В рядку {0} токен {1}'.format(numLine, (lexeme, token)))
        res = True
    else:
        # згенерувати помилку та інформацію про те, що
        # лексема та токен таблиці розбору (lex,tok) відрізняються від
        # очікуваних (lexeme,token)
        failParse('невідповідність токенів', (numLine, lex, tok, lexeme, token))
        res = False
    # перед поверненням - зменшити відступ
    indent = predIndt()
    return res


# Прочитати з таблиці розбору поточний запис
# Повертає номер рядка програми, лексему та її токен
def getSymb():
    if numRow > len_tableOfSymb:
        failParse('getSymb(): неочікуваний кінець програми', numRow)
    # таблиця розбору реалізована у формі словника (dictionary)
    # tableOfSymb[numRow]={numRow: (numLine, lexeme, token, indexOfVarOrConst)
    numLine, lexeme, token, _ = tableOfSymb[numRow]
    return numLine, lexeme, token
# Обробити помилки
# вивести поточну інформацію та діагностичне повідомлення

#failParse('кількість ідентифікаторів не дорівнює кількості значень', (numLine))
def failParse(str, tuple):
    if str == 'неочікуваний кінець програми':
        (lexeme, token, numRow) = tuple
        print(
            'Parser ERROR: \n\t Неочікуваний кінець програми - в таблиці символів (розбору) немає запису з номером {1}. \n\t Очікувалось - {0}'.format(
                (lexeme, token), numRow))
        exit(1001)
    if str == 'використання змінної, що не набула значення':
        (numRow) = tuple
        print(
            f'Використання змінної, що не набула значення -  в рядку {numRow}. \n\t ')
        exit(1001)
    if str == 'ділення на нуль':
        (numRow) = tuple
        print(
            f'Помилка: ділення на нуль у рядку  {numRow}. \n\t ')
        exit(1001)
    if str == 'кількість ідентифікаторів не дорівнює кількості значень':
        (numRow) = tuple
        print(
            f'Помилка: кількість ідентифікаторів не дорівнює кількості значень у рядку  {numRow}. \n\t ')
        exit(1001)
    if str == 'несумісність типів':
        (lType, rType) = tuple
        print(
            f'Несумісність типів  {lType}, {rType} . \n\t ')
        exit(1001)
    if str == 'неприпустимий тип':
        (numLine, lexeme, token) = tuple
        print(
            f'Parser ERROR: \n\t Неприпустимий тип - в таблиці символів (розбору) немає запису з номером {numLine}.')
        exit(1001)
    if str == 'використання неоголошеної змінної':
        (numLine, lexeme, tok) = tuple
        print(
            f'Parser ERROR: \n\t Використання неоголошеної змінної -  в рядку {numLine}: ({lexeme}, {tok}).')
        exit(1001)

    if str == 'повторне оголошення змінної':
        (numLine, lexeme, type, value) = tuple
        print(
            f'Parser ERROR: \n\t Повторне оголошення змінної в рядку {numLine}: ({lexeme}, {type}) вже існує в таблиці символів.')
        exit(1001)
    if str == 'getSymb(): неочікуваний кінець програми':
        numRow = tuple
        print(
            'Parser ERROR: \n\t Неочікуваний кінець програми - в таблиці символів (розбору) немає запису з номером {0}. \n\t Останній запис - {1}'.format(
                numRow, tableOfSymb[numRow - 1]))
        exit(1002)
    elif str == 'невідповідність токенів':
        (numLine, lexeme, token, lex, tok) = tuple
        print('Parser ERROR: \n\t В рядку {0} неочікуваний елемент ({1},{2}). \n\t Очікувався - ({3},{4}).'.format(
            numLine, lexeme, token, lex, tok))
        exit(1)
    elif str == 'невідповідність інструкцій':
        (numLine, lex, tok, expected) = tuple
        print(
            'Parser ERROR: \n\t В рядку {0} неочікуваний елемент ({1},{2}). \n\t Очікувався - {3}.'.format(numLine, lex,
                                                                                                           tok,
                                                                                                           expected))
        exit(2)
    elif str == 'невідповідність у Expression.Factor':
        (numLine, lex, tok, expected) = tuple
        print(
            'Parser ERROR: \n\t В рядку {0} неочікуваний елемент ({1},{2}). \n\t Очікувався - {3}.'.format(numLine, lex,
                                                                                                           tok,
                                                                                                           expected))
        exit(3)
    elif str == 'невідповідність типів операндів':
        (numLine, lexeme1, type1, lexeme2, type2) = tuple
        print(
            f'Parser ERROR: \n\t Невідповідність типів операндів в рядку {numLine}: ({lexeme1}, {type1}) і ({lexeme2}, {type2}) не можуть бути використані разом.')
        exit(4)
    elif str == 'невідповідність типів операндів для присвоювання':
        (numLine, lex, lType, rType) = tuple
        print(
            f'Parser ERROR: \n\t Невідповідність типів операндів для присвоювання в рядку {numLine}: змінна типу {lType} не може бути присвоєна значенню типу {rType}.')
        exit(1004)

# Функція для розбору за правилом для StatementList
# StatementList = Statement  { Statement }
# викликає функцію parseStatement() доти,
# доки parseStatement() повертає True
def parseStatementList():
    # Збільшуємо відступ
    indent = nextIndt()
    print(indent + 'parseStatementList():')

    while True:
        # Отримуємо поточну лексему, щоб перевірити, чи досягли кінця
        numLine, lex, tok = getSymb()

        # Перевіряємо наявність ключового слова 'finish' для завершення списку інструкцій
        if (lex, tok) == ('finish', 'keyword'):
            break

        # Обробка інструкції
        resType, sucParse = parseStatement()

        # Якщо інструкцію не було оброблено, завершуємо цикл
        if not sucParse:
            break

    # Зменшуємо відступ перед поверненням
    indent = predIndt()
    return resType


def parseStatement():
    # відступ збільшити
    indent = nextIndt()
    print(indent + 'parseStatement():')

    # прочитаємо поточну лексему в таблиці розбору
    numLine, lex, tok = getSymb()
    # Ініціалізуємо змінні
    resType = None
    res = False
    if tok == 'id':
        resType = parseAssign()
        res = True

    # якщо лексема - ключове слово 'if'
    # обробити інструкцію розгалуження
    elif (lex, tok) == ('if', 'keyword'):
        resType = parseIf()
        res = True

    elif (lex, tok) == ('for', 'keyword'):
      resType = parseFor()
      res = True

    elif (lex, tok) == ('while','keyword'):
        resType = parseWhile()
        res = True

    elif (lex, tok) == ('switch', 'keyword'):
        resType = parseSwitch()
        res = True

    elif (lex, tok) == ('until', 'keyword'):
        resType = parseUntil()
        res = True

    elif (lex, tok) == ('puts', 'keyword'):
        resType = parseOut()
        res = True

    elif (lex, tok) == ('gets', 'keyword'):
        resType = parseInp()
        res = True

    elif (lex, tok) == ('elif', 'keyword'):
        res = False

    elif (lex, tok) == ('else', 'keyword'):
        res = False

    # Перевірка на ключове слово 'end'
    elif (lex, tok) == ('end', 'keyword'):
        res = False  # Повертаємо False, щоб завершити список інструкцій
    elif (lex, tok) == ('finish', 'keyword'):
        res = False  # Повертаємо False, щоб завершити список інструкцій
    else:
        # жодна з інструкцій не відповідає
        # поточній лексемі у таблиці розбору,
        failParse('невідповідність інструкцій', (numLine, lex, tok, 'id або if'))
        res = False
    # перед поверненням - зменшити відступ
    indent = predIndt()
    return resType,res


def parseInp():
    # відступ збільшити
    indent = nextIndt()
    print(indent + 'parseInp():')
    resType = None
    # встановити номер нової поточної лексеми
    if parseToken('gets', 'keyword'):
        parseToken('.', 'punct')
        numLine, lex, tok = getSymb()
        if lex == 'to_i':

            parseToken('to_i', 'keyword')
            resType = 'int'
            postfixCode.append(('INP', 'inp_op'))
            res = True
        elif lex == 'to_f':

            parseToken('to_f', 'keyword')
            resType = 'float'
            postfixCode.append(('INP', 'inp_op'))
            res = True

        else:
            numLine, lex, tok = getSymb()
            failParse('невідповідність інструкцій', (numLine, lex, tok, 'to_i або to_f'))
            res = False

    else:
        res = False
    indent = predIndt()
    return resType, res

global lex10,tok10

def parseDeclaration():
    global numRow
    global lex10,tok10
    indent = nextIndt()
    print(indent + 'parseDeclaration():')
    numLine10, lex10, tok10 = getSymb()
    resType = None
    # Розбираємо ідентифікатори з лівого боку присвоєння
    numLine11, lex11, tok11 = getSymb()
    # postfixCodeGen('lval', (lex11, tok11))
    # postfixCodeGen('=', ('=', 'assign_op'))
    lType = parseIdentList()  # Отримуємо список ідентифікаторів

    # Переконатися, що токен '=' правильно розібраний
    parseToken('=', 'assign_op')

    # Розбираємо вирази з правого боку присвоєння
    rType = parseExpressionList()  # Отримуємо список виразів

    # Перевіряємо, чи кількість ідентифікаторів відповідає кількості виразів
    if len(lType) != len(rType):
        failParse('кількість ідентифікаторів не дорівнює кількості значень', (numLine10))

    # Обробка пар ідентифікаторів і виразів
    i = 0
    n1 = int(tableOfVar[lex10][0])
    while i < len(lType):  # Проходимо по всіх ідентифікаторах
        # Отримуємо тип операції
        resType = getTypeOp(lType[i], '=', rType[i])

        # Оновлення таблиці змінних для поточного ідентифікатора
        tableOfVar[lex10] = (n1, resType, 'assigned')
        n1 += 1
        # Отримання наступного ключа після поточного
        next_lex = get_next_key(tableOfVar, lex10)
        if next_lex:
            lex = next_lex  # Оновлюємо lex на наступний ключ
            lex10 = lex
            # postfixCodeGen('lval', (lex10, tok10))
            # postfixCodeGen('=', ('=', 'assign_op'))
        else:
            break  # Якщо наступного ключа немає, припиняємо цикл

        i += 1  # Переходимо до наступної пари

    indent = predIndt()
    return resType


def get_next_key(tableOfVar, current_key):
    # Отримуємо список всіх ключів таблиці
    keys = list(tableOfVar.keys())

    # Знайдемо індекс поточного ключа
    try:
        current_index = keys.index(current_key)
    except ValueError:
        raise KeyError(f"Ключ {current_key} не знайдений у таблиці змінних.")

    # Якщо поточний ключ не є останнім, повертаємо наступний
    if current_index + 1 < len(keys):
        next_key = keys[current_index + 1]
        return next_key
    else:
        # Якщо поточний ключ останній, то повертаємо None або будь-яке значення за замовчуванням
        return None

def postfixCodeGen(case,toTran):
    if case == 'lval':
        lex,tok = toTran
        postfixCode.append((lex,'l-val'))
    elif case == 'rval':
        lex,tok = toTran
        postfixCode.append((lex,'r-val'))
    else:
        lex,tok = toTran
        postfixCode.append((lex,tok))

def parseAssign():
    # номер запису таблиці розбору
    global numRow
    # відступ збільшити
    indent = nextIndt()
    print(indent + 'parseAssign():')
    # взяти поточну лексему
    numLine, lex, tok = getSymb()

    print(indent + 'в рядку {0} - токен {1}'.format(numLine, (lex, tok)))
    # встановити номер нової поточної лексеми
    numRow += 1
    numLineT, lexT, tokT = getSymb()
    lType = getTypeVar(lex)


    postfixCodeGen('lval', (lex, tok))

    if toView: configToPrint(lex, numRow)

    if lType == 'undeclared_variable':
        failParse('використання неоголошеної змінної', (numLine, lex, tok))
    resType = None
    isExtendedExpression = False
    if lexT == '=':
        parseToken('=', 'assign_op')
        numLineN, lexN, tokN = getSymb()
        if lexN == 'gets':
            parseInp()
            res = True
        elif lexN == '(':
            parseToken('(', 'brackets_op')
            rType = parseExpression()  # Отримуємо тип виразу всередині дужок
            parseToken(')', 'brackets_op')

            # Перевіряємо, чи є продовження виразу після закритої дужки (+)
            numLineNext, lexNext, tokNext = getSymb()
            if tokNext in ['add_op','mult_op', 'pow_op']:
                isExtendedExpression = True
                lTypebrac = rType
                numRow += 1  # Переходимо до наступного токена (після операції)
                numLineNextN, lexNextN, tokNextN = getSymb()  # Оновлюємо поточний токен
                if lexNext == '/' and lexNextN == '0':
                    tpl = (numLineNext)  # Використання неоголошеної або неініціалізованої змінної
                    failParse('ділення на нуль', tpl)

                rType = parseExpression()  # Продовжуємо обробку всього виразу


                postfixCodeGen(tokNext, (lexNext, tokNext))

                if toView: configToPrint(lexNext, numLineNext)

                # resType = getTypeOp(lTypebrac, '+', rType)
                # tableOfVar[lex] = (tableOfVar[lex][0], resType, 'assigned')  # Оновлюємо тип змінної

                if resType == 'type_error':
                    failParse(resType, (numLine, lexN,))
                res = True
            if isExtendedExpression == False:
                # resType = getTypeOp(lType, '=', rType)
                #
                # tableOfVar[lex] = (tableOfVar[lex][0], resType, 'assigned')  # Оновлюємо тип змінної

                if resType == 'type_error':
                    failParse(resType, (numLine, lexN,))
                res = True



            postfixCodeGen(lexT, (lexT, tokT))
            if toView: configToPrint(lex, numRow)


        else:

            rType = parseExpression()
            resType = getTypeOp(lType, '=', rType)
            tableOfVar[lex] = (tableOfVar[lex][0], resType, 'assigned')  # Оновлюємо тип


            postfixCodeGen(lexT, (lexT, tokT))
            if toView: configToPrint(lex, numRow)

            if resType == 'type_error':
                failParse(resType, (numLine, lexN,))
            res = True
    elif lexT == ',':
        parseToken(',', 'punct')
        parseDeclaration()
        # postfixCodeGen('=', ('=', 'assign_op'))
        type = tableOfConst[firstNumber][0]
        resType = getTypeOp(lex, '=', type)
        tableOfVar[lex] = (tableOfVar[lex][0], resType, 'assigned')

        res = True
    else:
        res = False
    isInitVar(lex)
    # postfixCodeGen('=', ('=', 'assign_op'))
    # if toView: configToPrint(lex, numRow)
    indent = predIndt()
    return resType, res


# def parseExpression():
#     global numRow
#     # відступ збільшити
#     indent = nextIndt()
#     print(indent + 'parseExpression():')
#     numLine, lex, tok = getSymb()
#     lType = parseTerm()
#     if lType == 'id':
#         lType = getTypeVar(lex)
#         if lType == 'undeclared_variable':
#             failParse('використання неоголошеної змінної', (numLine, lex, tok))
#         else:
#             if tableOfVar[lex][2] == 'undefined':  # Перевірка, чи змінна має значення
#                 tpl = (numLine)  # Використання неоголошеної або неініціалізованої змінної
#                 failParse('використання змінної, що не набула значення', tpl)
#             else:
#                 var_type = tableOfVar[lex][1]
#                 lType = var_type
#     resType = lType
#     F = True
#     while F:
#         numLineT, lexT, tokT = getSymb()
#
#         if tokT in ('add_op', 'rel_op', 'mult_op', 'pow_op'):
#
#             numRow += 1
#             numLineR, lexR, tokR = getSymb()
#
#
#             print(indent + 'в рядку {0} - токен {1}'.format(numLineT, (lexT, tokT)))
#             rType = parseTerm()
#
#             if lexT == '/' and lexR == '0':
#                 tpl = (numLine)  # Використання неоголошеної або неініціалізованої змінної
#                 failParse('ділення на нуль', tpl)
#             if rType == 'id':
#                 if tableOfVar[lexR][2] == 'undefined':  # Перевірка, чи змінна має значення
#                     tpl = (numLine)  # Використання неоголошеної або неініціалізованої змінної
#                     failParse('використання змінної, що не набула значення', tpl)
#                 else:
#                     var_type = tableOfVar[lexR][1]
#                     rType = var_type
#
#
#             resType = getTypeOp(lType, lexT, rType)
#             if resType != 'type_error':
#                 lType = resType
#             else:
#                 tpl = (numLine, lType, lex, rType)  # для повiдомлення про помилку
#                 failParse(resType, tpl)
#
#             if tokT == 'pow_op':
#                 postfixCodeGen('**', ('**', 'pow_op'))
#                 if toView: configToPrint(lexT, numLineT)
#
#             elif tokT != 'pow_op':
#                 postfixCodeGen(lexT, (lexT, tokT))
#                 if toView: configToPrint(lexT, numLineT)
#
#         else:
#             F = False
#     # перед поверненням - зменшити відступ
#     indent = predIndt()
#     return resType
#


def parseExpression():
    global numRow
    operator_stack = []  # Для зберігання операторів
    operand_stack = []   # Для зберігання операндів (для генерації коду)

    indent = nextIndt()
    print(indent + 'parseExpression():')
    numLine, lex, tok = getSymb()
    lType = parseTerm()  # Починаємо з першого терма

    if lType == 'id':
        lType = getTypeVar(lex)
        if lType == 'undeclared_variable':
            failParse('використання неоголошеної змінної', (numLine, lex, tok))
        elif tableOfVar[lex][2] == 'undefined':
            failParse('використання змінної, що не набула значення', (numLine, lex, tok))
        else:
            lType = tableOfVar[lex][1]

    operand_stack.append(lex)  # Додаємо операнд в стек
    resType = lType

    F = True
    while F:
        numLineT, lexT, tokT = getSymb()

        if tokT in ('add_op', 'rel_op', 'mult_op', 'pow_op'):  # Якщо оператор
            while operator_stack:
                top_op, top_tok = operator_stack[-1]

                # Перевіряємо, чи потрібно витягнути оператори зі стека
                if should_pop_operator(top_op, lexT):
                    operator_stack.pop()
                    right_operand = operand_stack.pop()
                    left_operand = operand_stack.pop()

                    # Генерація коду для поточної операції
                    postfixCodeGen(top_op, (top_op, top_tok))
                    operand_stack.append(f"temp_{numRow}")  # Результат операції
                else:
                    break

            operator_stack.append((lexT, tokT))  # Додаємо поточний оператор в стек
            numRow += 1
            rType = parseTerm()

            if lexT == '/' and operand_stack[-1] == '0':  # Перевірка ділення на нуль
                failParse('ділення на нуль', (numLineT, lexT, tokT))

            if rType == 'id' and tableOfVar[operand_stack[-1]][2] == 'undefined':
                failParse('використання змінної, що не набула значення', (numLineT, lexT, tokT))
            elif rType == 'id':
                rType = tableOfVar[operand_stack[-1]][1]

            resType = getTypeOp(lType, lexT, rType)
            if resType == 'type_error':
                failParse('невідповідність типів', (numLineT, lType, lexT, rType))

            operand_stack.append(f"temp_{numRow}")  # Додаємо результат в стек

        elif tokT == 'open_paren':  # Відкриваюча дужка
            operator_stack.append((lexT, tokT))
        elif tokT == 'close_paren':  # Закриваюча дужка
            while operator_stack and operator_stack[-1][0] != '(':
                op, tok_op = operator_stack.pop()
                right_operand = operand_stack.pop()
                left_operand = operand_stack.pop()

                # Генерація коду для операції
                postfixCodeGen(op, (op, tok_op))
                operand_stack.append(f"temp_{numRow}")

            operator_stack.pop()  # Прибираємо '(' зі стека

        else:
            F = False

    # Завершуємо обробку виразу
    while operator_stack:
        op, tok_op = operator_stack.pop()
        right_operand = operand_stack.pop()
        left_operand = operand_stack.pop()

        # Генерація коду для залишкових операторів
        postfixCodeGen(op, (op, tok_op))
        operand_stack.append(f"temp_{numRow}")

    indent = predIndt()
    return resType



# Функция для задания приоритета операций
def precedence(operator):
    priorities = {'+': 1, '-': 1, '*': 2, '/': 2, '**': 3}
    return priorities.get(operator, 0)


def should_pop_operator(top_op, current_op):
    top_precedence = precedence(top_op)
    current_precedence = precedence(current_op)

    if current_op == '**':
        return top_precedence > current_precedence
    return top_precedence >= current_precedence


# Функція для розбору ідентифікатора

def parseIdent():
    global numRow
    # збільшити відступ
    indent = nextIndt()
    print(indent + 'parseIdent():')
    resType = None

    # взяти поточну лексему
    numLine, lex, tok = getSymb()

    # перевірити, чи є лексема ідентифікатором
    if tok == 'id':
        numRow += 1  # переміщуємося до наступної лексеми
        print(indent + 'в рядку {0} - токен {1}'.format(numLine, (lex, tok)))
        if lex in tableOfVar:
            var_info = tableOfVar[lex]  # Отримуємо поточний запис змінної
            if var_info[2] == 'undefined':  # Перевіряємо статус
                tableOfVar[lex] = (var_info[0], var_info[1], 'assigned')  # Оновлюємо статус
                resType = tableOfVar[lex][1]
                return resType
        else:
            failParse('використання неоголошеної змінної', (numLine, lex, tok))
        res = True
    else:
        # якщо лексема не ідентифікатор — помилка
        failParse('невідповідність токенів', (numLine, lex, tok, 'id'))
        res = False

    # зменшити відступ
    indent = predIndt()
    return res

global lexCase, tokCase


def parseSwitch():
    global numRow, lexCase, tokCase
    # відступ збільшити
    indent = nextIndt()
    numLine, lex, tok = getSymb()

    m1 = createLabel()  # Мітка для початку switch
    m2 = createLabel()  # Мітка для завершення switch
    m3 = createLabel()  # Мітка для початку switch


    res = None

    if lex == 'switch' and tok == 'keyword':
        print(indent + f'в рядку {numLine} - токен {(lex, tok)}')
        numRow += 1

        numLine1, lex1, tok1 = getSymb()

        lexCase = lex1
        tokCase = tok1

        parseDigit() or parseIdent()

        parseToken('do', 'keyword')

        while parseCaseBlock():
            pass  # Виконуємо парсинг блоків case, поки це можливо

        # parseDefaultBlock()

        # Завершення switch
        parseToken('end', 'keyword')

        res = True
    else:
        res = False
    # перед поверненням - зменшити відступ
    indent = predIndt()
    return res

global lexDefault,tokDefault

def parseCaseBlock():
    global numRow,lexCase, tokCase, lexDefault,tokDefault
    # відступ збільшити
    indent = nextIndt()
    m1 = createLabel()
    m2 = createLabel()
    numLine, lex, tok = getSymb()
    if lex == 'case' and tok == 'keyword':
        print(indent + 'в рядку {0} - токен {1}'.format(numLine, (lex, tok)))
        numRow += 1
        #getIdent()

        numLine1, lex1, tok1 = getSymb()

        lexDefault = lex1
        tokDefault = tok1

        postfixCodeGen('rval', (lexCase, tokCase))
        postfixCodeGen(tok1, (lex1, tok1))
        postfixCodeGen('==', ('==', 'rel_op'))

        parseDigit() or parseIdent()

        postfixCode.append(m1)
        postfixCode.append(('JF', 'jf'))

        parseToken(':', 'punct')

        parseStatement()

        postfixCode.append(m2)
        postfixCode.append(('JMP', 'jump'))

        setValLabel(m1)
        postfixCode.append(m1)
        postfixCode.append((':', 'colon'))
        setValLabel(m2)
        postfixCode.append(m2)
        postfixCode.append((':', 'colon'))

        res = True
    else:
        res = False
    # перед поверненням - зменшити відступ
    indent = predIndt()
    return res

def parseDefaultBlock():
    global numRow, lexDefault,tokDefault
    indent = nextIndt()
    numLine, lex, tok = getSymb()

    m1 = createLabel()
    m2 = createLabel()

    if lex == 'default' and tok == 'keyword':
        print(indent + 'в рядку {0} - токен {1}'.format(numLine, (lex, tok)))
        numRow += 1

        postfixCodeGen('rval', (lexCase, tokCase))
        postfixCodeGen(tokDefault, (lexDefault, tokDefault))
        postfixCodeGen('!=', ('!=', 'rel_op'))

        postfixCode.append(m1)
        postfixCode.append(('JF', 'jf'))


        parseToken(':', 'punct')
        parseStatementList()

        postfixCode.append(m2)
        postfixCode.append(('JMP', 'jump'))

        setValLabel(m2)
        postfixCode.append(m2)
        postfixCode.append((':', 'colon'))

        res = True
    else:
        res = False
    indent = predIndt()
    return res

def parseStatementListSwitch():
    global numRow
    indent = nextIndt()  # Збільшити відступ
    print(indent + 'parseStatementListSwitch():')

    while True:
        numLine, lex, tok = getSymb()

        # Перевіряємо, чи досягнуто кінець блоку switch
        if (lex, tok) == ('end', 'keyword'):
            break

        if tok == 'keyword':
            if lex == 'case':
                # Якщо знайдено 'case', викликати parseCaseBlock
                if not parseCaseBlock():
                    print('Parser ERROR: Не вдалося обробити блок case.')
                    exit(2001)  # Код помилки для блоків case
            elif lex == 'default':
                # Якщо знайдено 'default', викликати parseDefaultBlock
                if not parseDefaultBlock():
                    print('Parser ERROR: Не вдалося обробити блок default.')
                    exit(2002)  # Код помилки для блоків default
                # Після обробки default завершити блок switch
                break
            else:
                # Тут можуть бути інші ключові слова чи оператори
                if not parseStatement():  # Якщо це не case чи default, викликати парсинг звичайних операторів
                    break  # Вийти з циклу, якщо парсинг не вдався
        else:
            # Якщо токен не є ключовим словом, вийти з циклу
            break

    # Повернутися на один рівень у відступі
    indent = predIndt()


def parseDigit():
    global numRow
    indent = nextIndt()
    print(indent + 'parseDigit():')

    # Отримуємо поточну лексему
    numLine, lex, tok = getSymb()

    # Перевіряємо, чи є лексема числом
    if tok == 'int':
        numRow += 1  # Переходимо до наступної лексеми
        print(indent + 'в рядку {0} - токен {1}'.format(numLine, (lex, tok)))
        res = True
    else:
        res = False  # Повертаємо False, якщо це не число

    indent = predIndt()
    return res

def parseTerm():
    global numRow
    # відступ збільшити
    indent = nextIndt()
    print(indent + 'parseTerm():')
    res = parseFactor()
    F = True
    # продовжувати розбирати Множники (Factor)
    # розділені лексемами '*' або '/'
    # перед поверненням - зменшити відступ
    indent = predIndt()
    return res


# def parseFactor():
#     global numRow
#     # відступ збільшити
#     indent = nextIndt()
#     print(indent + 'parseFactor():')
#     numLine, lex, tok = getSymb()
#
#     if tok in ('int', 'float', 'id', 'add_op', 'mult_op'):
#         numRow += 1
#         print(indent + 'в рядку {0} - токен {1}'.format(numLine, (lex, tok)))
#         if tok in ('add_op', 'mult_op'):
#             numLine, lex, tok = getSymb()
#             if lex == '(':
#                 print(indent + 'в рядку {0} - токен {1}'.format(numLine, (lex, tok)))
#                 numRow += 1
#                 parseExpression()
#                 parseToken(')', 'brackets_op')
#             if tok == 'id':
#                 print(indent + 'в рядку {0} - токен {1}'.format(numLine, (lex, tok)))
#                 numRow += 1
#
#     # третя альтернатива для Factor
#     # якщо лексема - це відкриваюча дужка
#     elif lex == '(':
#         print(indent + 'в рядку {0} - токен {1}'.format(numLine, (lex, tok)))
#         numRow += 1
#         parseExpression()
#         parseToken(')', 'brackets_op')
#     else:
#         failParse('невідповідність у Expression.Factor',
#                   (numLine, lex, tok, 'rel_op, int, float, id або \'(\' Expression \')\''))
#     # перед поверненням - зменшити відступ
#     indent = predIndt()
#     return tok


def parseFactor():
    global numRow
    # Збільшуємо відступ
    indent = nextIndt()
    print(indent + 'parseFactor():')
    numLine, lex, tok = getSymb()

    # Обробка унарних операторів
    if tok == 'add_op' and lex in ('+', '-'):  # Якщо це '+' або '-'
        unary_op = lex  # Зберігаємо оператор

        numRow += 1  # Переходимо до наступної лексеми
        numLine, lex, tok = getSymb()  # Отримуємо наступну лексему

        if tok in ('int', 'float'):  # Якщо наступна лексема - число
            if unary_op == '-':

                postfixCodeGen(lex, (lex, tok))
                if toView: configToPrint(lex, numLine)
                postfixCode.append(('NEG', 'neg_op'))

                lex = str(-float(lex)) if '.' in lex else str(-int(lex))  # Застосовуємо унарний мінус

            elif unary_op == '+':

                lex = str(float(lex)) if '.' in lex else str(int(lex))  # Унарний плюс не змінює значення
            numRow += 1  # Переходимо до наступної лексеми
            print(indent + 'в рядку {0} - токен {1}'.format(numLine, (lex, tok)))
            return 'float' if '.' in lex else 'int'  # Повертаємо тип числа
        else:
            failParse('Унарний оператор застосовано не до числа', (numLine, lex, tok))

    if tok in ('int', 'float', 'id', 'add_op', 'mult_op','boolval'):

        if tok == 'id':

            postfixCodeGen('rval', (lex, 'rval'))
            if toView: configToPrint(lex, numRow)
        else:
            postfixCodeGen('const',(lex, tok))
            if toView: configToPrint(lex, numRow)

        numRow += 1
        print(indent + 'в рядку {0} - токен {1}'.format(numLine, (lex, tok)))

        if tok in ('add_op', 'mult_op'):
            numLine, lex, tok = getSymb()
            if lex == '(':
                print(indent + 'в рядку {0} - токен {1}'.format(numLine, (lex, tok)))
                numRow += 1
                parseExpression()
                parseToken(')', 'brackets_op')
            if tok == 'id':
                print(indent + 'в рядку {0} - токен {1}'.format(numLine, (lex, tok)))
                numRow += 1

    # третя альтернатива для Factor
    # якщо лексема - це відкриваюча дужка
    elif lex == '(':
        print(indent + 'в рядку {0} - токен {1}'.format(numLine, (lex, tok)))
        numRow += 1
        parseExpression()
        parseToken(')', 'brackets_op')
    else:
        failParse('невідповідність у Expression.Factor',
                  (numLine, lex, tok, 'rel_op, int, float, id або \'(\' Expression \')\''))
    # перед поверненням - зменшити відступ
    indent = predIndt()
    return tok


# розбір інструкції розгалуження за правилом
# IfStatement = if BoolExpr then Statement else Statement endif
# функція названа parseIf() замість parseIfStatement()

# def parseIf():
# #     global numRow
# #     # відступ збільшити
# #     indent = nextIndt()
# #     numLine, lex, tok = getSymb()
# #     resType = None
# #
# #     if lex == 'if' and tok == 'keyword':
# #         print(indent + 'в рядку {0} - токен {1}'.format(numLine, (lex, tok)))
# #         numRow += 1
# #         parseBoolExpr()
# #
# #         m1 = createLabel()
# #         postfixCode.append(m1)
# #         postfixCode.append(('JF','jf'))
# #
# #         parseStatementList()  # Виконуємо парсинг блоку if
# #         while True:
# #             numLine, lex, tok = getSymb()
# #             if lex == 'elif' and tok == 'keyword':
# #                 print(indent + 'в рядку {0} - токен {1}'.format(numLine, (lex, tok)))
# #                 numRow += 1
# #                 parseBoolExpr() # Парсинг логічного виразу в elif
# #
# #                 m5 = createLabel()
# #                 postfixCode.append(m5)
# #                 postfixCode.append(('JF', 'jf'))
# #                 setValLabel(m1)
# #                 postfixCode.append(m1)
# #                 postfixCode.append((':', 'colon'))
# #
# #                 parseStatementList()  # Парсинг блоку elif
# #             elif lex == 'else' and tok == 'keyword':
# #
# #                 m2 = createLabel()
# #                 postfixCode.append(m2)
# #                 postfixCode.append(('JMP', 'jump'))
# #                 setValLabel(m1)
# #                 postfixCode.append(m1)
# #                 postfixCode.append((':','colon'))
# #                 setValLabel(m5)
# #                 postfixCode.append(m5)
# #                 postfixCode.append((':', 'colon'))
# #
# #                 print(indent + 'в рядку {0} - токен {1}'.format(numLine, (lex, tok)))
# #                 numRow += 1
# #                 parseStatementList()  # Парсинг блоку else
# #                 break  # Вийти з циклу після обробки else
# #             else:
# #                 # Якщо токен не elif або else, повертаємося до завершення if
# #                 break
# #         parseToken('end', 'keyword')
# #         setValLabel(m2)
# #         postfixCode.append(m2)
# #         postfixCode.append((':','colon'))
# #         res = True
# #     else:
# #         res = False
# #
# #     # перед поверненням - зменшити відступ
# #     indent = predIndt()
# #     return resType, res

# def parseIf():
#     global numRow
#     # відступ збільшити
#     indent = nextIndt()
#     numLine, lex, tok = getSymb()
#     resType = None
#
#     if lex == 'if' and tok == 'keyword':
#         print(indent + 'в рядку {0} - токен {1}'.format(numLine, (lex, tok)))
#         numRow += 1
#         parseBoolExpr()
#
#         m1 = createLabel()
#         postfixCode.append(m1)
#         postfixCode.append(('JF', 'jf'))
#
#         parseStatementList()  # Виконуємо парсинг блоку if
#
#         m5 = None  # Ініціалізуємо змінну мітки для elif
#         while True:
#             numLine, lex, tok = getSymb()
#             if lex == 'elif' and tok == 'keyword':
#                 print(indent + 'в рядку {0} - токен {1}'.format(numLine, (lex, tok)))
#                 numRow += 1
#                 parseBoolExpr()  # Парсинг логічного виразу в elif
#
#                 m5 = createLabel()
#                 postfixCode.append(m5)
#                 postfixCode.append(('JF', 'jf'))
#
#                 setValLabel(m1)
#                 postfixCode.append(m1)
#                 postfixCode.append((':', 'colon'))
#
#                 parseStatementList()  # Парсинг блоку elif
#
#             elif lex == 'else' and tok == 'keyword':
#                 m2 = createLabel()
#                 postfixCode.append(m2)
#                 postfixCode.append(('JMP', 'jump'))
#
#                 setValLabel(m1)
#                 postfixCode.append(m1)
#                 postfixCode.append((':', 'colon'))
#
#                 # Перевіряємо, чи було створено мітку m5
#                 if m5:
#                     setValLabel(m5)
#                     postfixCode.append(m5)
#                     postfixCode.append((':', 'colon'))
#
#                 print(indent + 'в рядку {0} - токен {1}'.format(numLine, (lex, tok)))
#                 numRow += 1
#                 parseStatementList()  # Парсинг блоку else
#                 break  # Вийти з циклу після обробки else
#             else:
#                 # Якщо токен не elif або else, повертаємося до завершення if
#                 break
#
#         parseToken('end', 'keyword')
#
#         setValLabel(m2)
#         postfixCode.append(m2)
#         postfixCode.append((':', 'colon'))
#         res = True
#     else:
#         res = False
#
#     # перед поверненням - зменшити відступ
#     indent = predIndt()
#     return resType, res

def parseIf():
    global numRow
    # відступ збільшити
    indent = nextIndt()
    numLine, lex, tok = getSymb()
    resType = None
    m1 = createLabel()
    m2 = createLabel()

    if lex == 'if' and tok == 'keyword':
        print(indent + 'в рядку {0} - токен {1}'.format(numLine, (lex, tok)))
        numRow += 1
        parseBoolExpr()

        postfixCode.append(m1)
        postfixCode.append(('JF', 'jf'))

        parseStatementList()  # Виконуємо парсинг блоку if

        postfixCode.append(m2)
        postfixCode.append(('JMP', 'jump'))

        m5 = None  # Ініціалізуємо змінну мітки для elif
        while True:
            numLine, lex, tok = getSymb()
            setValLabel(m1)
            postfixCode.append(m1)
            postfixCode.append((':', 'colon'))
            if lex == 'elif' and tok == 'keyword':
                print(indent + 'в рядку {0} - токен {1}'.format(numLine, (lex, tok)))
                numRow += 1

                parseBoolExpr()  # Парсинг логічного виразу в elif

                # m5 = createLabel()
                m1 = createLabel()
                postfixCode.append(m1)
                postfixCode.append(('JF', 'jf'))

                parseStatementList()  # Парсинг блоку elif
                postfixCode.append(m2)
                postfixCode.append(('JMP', 'jump'))


            # elif lex == 'else' and tok == 'keyword':

            # setValLabel(m1)
            # postfixCode.append(m1)
            # postfixCode.append((':', 'colon'))

            # Перевіряємо, чи було створено мітку m5
            # if m5:
            #    setValLabel(m5)
            #    postfixCode.append(m5)
            #    postfixCode.append((':', 'colon'))

            #    print(indent + 'в рядку {0} - токен {1}'.format(numLine, (lex, tok)))
            #    numRow += 1
            #    parseStatementList()  # Парсинг блоку else
            #    break  # Вийти з циклу після обробки else
            else:
                # Якщо токен не elif або else, повертаємося до завершення if
                break
        numLine, lex, tok = getSymb()
        if lex == 'else' and tok == 'keyword':
            print(indent + 'в рядку {0} - токен {1}'.format(numLine, (lex, tok)))
            numRow += 1
            parseStatementList()
        parseToken('end', 'keyword')
        setValLabel(m2)
        postfixCode.append(m2)
        postfixCode.append((':', 'colon'))
        res = True
    else:
        res = False

    # перед поверненням - зменшити відступ
    indent = predIndt()
    return resType, res


def parseWhile():
    global numRow
    # відступ збільшити
    indent = nextIndt()
    numLine, lex, tok = getSymb()

    m1 = createLabel()
    m2 = createLabel()

    if lex == 'while' and tok == 'keyword':
        print(indent + 'в рядку {0} - токен {1}'.format(numLine, (lex, tok)))
        numRow += 1

        setValLabel(m2)
        postfixCode.append(m2)
        postfixCode.append((':', 'colon'))
        parseBoolExpr()

        postfixCode.append(m1)
        postfixCode.append(('JF', 'jf'))

        parseToken('do', 'keyword')

        parseStatementList()
        postfixCode.append(m2)
        postfixCode.append(('JMP', 'jump'))

        parseToken('end', 'keyword')
        setValLabel(m1)
        postfixCode.append(m1)
        postfixCode.append((':', 'colon'))
        res = True
    else:
        res = False
    # перед поверненням - зменшити відступ
    indent = predIndt()
    return res


def parseUntil():
    global numRow
    # відступ збільшити
    indent = nextIndt()
    m1 = createLabel()
    m2 = createLabel()
    m3 = createLabel()

    numLine, lex, tok = getSymb()
    if lex == 'until' and tok == 'keyword':
        print(indent + 'в рядку {0} - токен {1}'.format(numLine, (lex, tok)))
        numRow += 1

        setValLabel(m2)
        postfixCode.append(m2)
        postfixCode.append((':', 'colon'))

        parseBoolExpr()

        postfixCode.append(m1)
        postfixCode.append(('JF', 'jf'))

        postfixCode.append(m3)
        postfixCode.append(('JMP', 'jump'))

        parseToken('do', 'keyword')

        setValLabel(m1)
        postfixCode.append(m1)
        postfixCode.append((':', 'colon'))

        parseStatementList()

        postfixCode.append(m2)
        postfixCode.append(('JMP', 'jump'))


        parseToken('end', 'keyword')
        setValLabel(m3)
        postfixCode.append(m3)
        postfixCode.append((':', 'colon'))
        res = True
    else:
        res = False
    # перед поверненням - зменшити відступ
    indent = predIndt()
    return res

# def parseFor():
#     global numRow
#     # відступ збільшити
#     indent = nextIndt()
#     numLine, lex, tok = getSymb()
#     if lex == 'for' and tok == 'keyword':
#         print(indent + 'в рядку {0} - токен {1}'.format(numLine, (lex, tok)))
#         numRow += 1
#         parseIdent()
#         parseToken('in', 'keyword')
#         parseRange()
#         parseToken('do', 'keyword')
#         parseStatementList()
#         parseToken('end', 'keyword')
#         res = True
#     else:
#         res = False
#     # перед поверненням - зменшити відступ
#     indent = predIndt()
#     return res

global firstLex,firstTok
global secondLex, secondTok
def parseFor():
    global numRow, postfixCode, firstLex, secondLex, secondTok
    indent = nextIndt()
    print(indent + 'parseFor():')

    m1 = createLabel()  # Мітка для тіла циклу
    m2 = createLabel()  # Мітка для перевірки умови циклу

    numLine, lex, tok = getSymb()
    if lex == 'for' and tok == 'keyword':
        print(indent + f'в рядку {numLine} - токен ({lex}, {tok})')

        numRow += 1

        # Стартове значення змінної
        numLine1, lex1, tok1 = getSymb()
        postfixCodeGen('lval', (lex1, tok1))  # Записуємо значення лівої частини
        if toView: configToPrint(lex1, numLine1)

        parseIdent()  # Парсимо ідентифікатор

        parseToken('in', 'keyword')  # Парсимо ключове слово 'in'
        parseRange()  # Парсимо діапазон

        # Генерація коду для правої частини
        if firstTok == 'id':
            postfixCodeGen('rval', (firstLex, firstTok))
        else:
            postfixCodeGen(firstTok, (firstLex, firstTok))
        postfixCodeGen('=', ('=', 'assign_op'))  # Присвоєння значення

        # Мітка для перевірки умови циклу
        setValLabel(m2)
        postfixCode.append(m2)
        postfixCode.append((':', 'colon'))

        # Генерація коду для правої частини умови циклу
        if secondTok == 'id':
            postfixCodeGen('rval', (secondLex, secondTok))
        else:
            postfixCodeGen(secondTok, (secondLex, secondTok))

        postfixCodeGen('rval', (lex1, tok1))  # Записуємо значення правої частини
        if toView: configToPrint(lex1, numLine1)
        postfixCodeGen('>=', ('>=', 'rel_op'))  # Оператор порівняння

        postfixCode.append(m1)  # Мітка для переходу
        postfixCode.append(('JF', 'jf'))  # Перехід, якщо умова не виконується

        # Обробка тіла циклу
        parseToken('do', 'keyword')  # Парсимо 'do'

        parseStatementList()  # Парсимо список операторів у тілі циклу

        postfixCodeGen('lval', (lex1, tok1))
        postfixCodeGen('rval', (lex1, tok1))
        postfixCodeGen('1', ('1', 'int'))
        postfixCodeGen('+', ('+', 'add_op'))
        postfixCodeGen('=', ('=', 'assign_op'))  # Оновлення лічильника циклу

        postfixCode.append(m2)  # Повернення до перевірки умови циклу
        postfixCode.append(('JMP', 'jump'))  # Перехід до перевірки умови циклу

        # Завершення циклу
        parseToken('end', 'keyword')  # Парсимо 'end'

        # Завершення циклу
        setValLabel(m1)
        postfixCode.append(m1)
        postfixCode.append((':', 'colon'))  # Мітка завершення циклу

        res = True
    else:
        failParse('Expected "for"', (numLine, lex, tok))

    # Повернення відступу
    indent = predIndt()
    return res




def parseRange():
    global numRow
    global firstLex,firstTok, secondLex,secondTok
    indent = nextIndt()
    print(indent + 'parseRange():')

    # Очікувати лексему '['
    parseToken('[', 'brackets_op')
    numLine, lex, tok = getSymb()
    firstLex = lex
    firstTok = tok
    # Розбирати перше значення діапазону
    parseDigit() or parseIdent()
    # Очікувати лексему '..' для визначення діапазону
    parseToken('..', 'range_op')

    numLine, lex, tok = getSymb()
    secondLex = lex
    secondTok = tok

    # Розбирати друге значення діапазону
    parseDigit() or parseIdent()

    # Очікувати лексему ']'
    parseToken(']', 'brackets_op')

    # перед поверненням - зменшити відступ
    indent = predIndt()
    return True

# розбір логічного виразу за правиллом
# BoolExpr = Expression ('='|'<='|'>='|'<'|'>'|'<>') Expression
def parseBoolExpr():
    global numRow
    indent = nextIndt()
    print(indent + 'parseBoolExpr():')
    numLine, lex, tok = getSymb()
    parseTerm()  # Розбираємо перший терм
    F = True

    while F:
        numLine, lex, tok = getSymb()  # Зчитуємо наступний токен
        if tok == 'rel_op':  # Очікуємо відношення
            print(indent + f'в рядку {numLine} - токен {lex, tok}')
            numRow += 1
            parseTerm()  # Розбираємо терм після rel_op
            postfixCode.append((lex, tok))  # Додаємо в постфікс
        elif tok in ('id', 'int', 'float', 'true', 'false', '('):  # Якщо це допустимий завершальний токен
            # postfixCode.append((lex, tok))
            F = False
        else:  # Якщо нічого не підходить, завершуємо
            failParse('mismatch in BoolExpr', (numLine, lex, tok, 'rel_op'))
            F = False

    indent = predIndt()  # Зменшуємо відступ
    return True


def parseOut():
    global numRow
    # Збільшити відступ
    indent = nextIndt()
    print(indent + 'parseOut():')

    # Отримуємо поточну лексему
    numLine, lex, tok = getSymb()

    # Перевіряємо, чи це ключове слово 'puts'
    if (lex, tok) == ('puts', 'keyword'):
        numRow += 1
        print(indent + 'в рядку {0} токен {1}'.format(numLine, (lex, tok)))
        res = False

        # Перевіряємо, чи наступний токен - число
        next_numLine, next_lex, next_tok = getSymb()  # Отримуємо наступний токен

        if next_tok == 'int':
            print(indent + 'в рядку {0} - токен {1}'.format(numLine, (next_lex, next_tok)))

            postfixCode.append((next_lex, 'int'))
            postfixCode.append(('OUT', 'out_op'))

            res = True
            #
            # postfixCodeGen('out_op', (next_lex,'out_op'))
            # if toView: configToPrint(next_lex, numRow)

            numRow += 1  # Переходимо до наступної лексеми

        elif next_tok == 'punct' and next_lex == '"':
            parseToken(next_lex, next_tok)

            # postfixCode.append((next_lex, 'r-val'))
            # postfixCode.append(('OUT', 'out_op'))
            # Перевіряємо на ідентифікатор всередині лапок
            numLineO, lexO, tokO = getSymb()

            if parseIdent():
                postfixCode.append((lexO, 'r-val'))
                postfixCode.append(('OUT', 'out_op'))
                # Перевіряємо на закриваючі лапки
                if parseToken('"', 'punct'):
                    res = True
        elif (next_tok == 'punct' or next_tok == 'add_op' or next_tok == 'mult_op'
              or next_tok == 'rel_op' or next_tok == 'assign_op' or next_tok == 'sharp' or next_tok == 'brackets_op'):
            print(indent + 'в рядку {0} - токен {1}'.format(numLine, (next_lex, next_tok)))

            res = True
            numRow += 1  # Переходимо до наступної лексеми
        else:
            failParse('Невідповідність інструкцій, очікувалось число або лапки', (numLine, lex, tok))

    else:
        failParse('Невідповідність інструкцій, очікувалось "puts"', (numLine, lex, tok, 'puts'))
        res = False

    # Зменшити відступ
    indent = predIndt()
    return res


def parseIdentList():
    global numRow
    global lex10
    indent = nextIndt()  # Збільшуємо відступ для виводу
    print(indent + 'parseIdentList():')  # Виводимо назву функції
    resType = []  # Ініціалізуємо порожній список для збереження ідентифікаторів

    # Розбираємо перший ідентифікатор
    resType.append(parseIdent())

    # Поки є символи коми, продовжуємо розбір ідентифікаторів
    while True:

        numLine, lex, tok = getSymb()  # Отримуємо наступний токен

        if tok == 'punct' and lex == ',':
            parseToken(',', 'punct')  # Розбираємо кому
            resType.append(parseIdent())  # Додаємо наступний ідентифікатор до списку
        else:
            # Якщо токен не кома, виходимо з циклу
            break

    indent = predIndt()  # Зменшуємо відступ перед поверненням
    return resType  # Повертаємо список ідентифікаторів


firstNumber = 1
def parseExpressionList():
    global numRow
    global firstNumber
    global lex10
    numLine, lex, tok = getSymb()
    indent = nextIndt()  # Збільшуємо відступ для виводу
    print(indent + 'parseExpressionList():')  # Виводимо назву функції

    resType = []  # Ініціалізуємо список для збереження типів виразів
    firstNumber = lex  # Зберігаємо значення першого виразу
    # Розбираємо перше вираження, але не додаємо до списку

    parseExpression()

    postfixCodeGen('=', ('=', 'assign_op'))
    # Поки є символи коми, продовжуємо розбір виражень
    while True:
        numLine, lex, tok = getSymb()  # Отримуємо наступний токен
        if tok == 'punct' and lex == ',':
            postfixCodeGen('lval', (lex10, tok10))
            parseToken(',', 'punct')  # Розбираємо кому
            resType.append(parseExpression())  # Додаємо наступний вираз до списку
            i = int(tableOfVar[lex10][0]) + 1
            for key, value in tableOfVar.items():
                if value[0] == i:  # Якщо перший елемент кортежу дорівнює i
                    lex10 = key
                    break
            postfixCodeGen('=', ('=', 'assign_op'))
        else:
            # Якщо токен не кома, виходимо з циклу
            break

    indent = predIndt()  # Зменшуємо відступ перед поверненням
    return resType  # Повертаємо список результатів



def parseExpressionListOrInpSplit():
    indent = nextIndt()
    print(indent + 'parseExpressionOrInpSplit():')

    # Отримуємо поточний токен
    numLine, lex, tok = getSymb()

    if tok == 'id':
        parseIdent()
        parseToken('.', 'punct')  # Розбираємо '.'
        parseToken('split', 'keyword')  # Розбираємо 'split'
        # Обробка завершена, присвоюємо результат
        res = True
    elif lex == 'gets':
        parseToken('gets', 'keyword')  # Розбираємо '.'
        parseToken('.', 'punct')  # Розбираємо '.'
        parseToken('split', 'keyword')  # Розбираємо 'split'
        res = True
    else:
        # В іншому випадку обробляємо як звичайний вираз
        parseExpressionList()
        res = True

    indent = predIndt()
    return res


stepIndt = 2
indt = 0  # або indt = 0


def nextIndt():
    global indt
    indt += stepIndt
    return ' ' * indt


def predIndt():
    global indt
    indt -= stepIndt
    return ' ' * indt

def compileToPostfix(fileName):
    global len_tableOfSymb , FSuccess
    print('compileToPostfix: lexer Start Up\n')
    FSuccess = lex()
    print('compileToPostfix: lexer-FSuccess ={0}'.format(FSuccess))
    # чи був успiшним лексичний розбiр
    if ('Lexer',True) == FSuccess:
        len_tableOfSymb = len(tableOfSymb)
        print('-'*55)
        print('compileToPostfix: Start Up compiler = parser + codeGenerator\n')
        FSuccess = False
        FSuccess = parseProgram()
        if FSuccess == (True):
            #serv()
            savePostfixCode('test1')
        if not FSuccess:
            fname = "test1.postfix"
            f = open(fname, 'w')

            f.close()
            print(f"Postfix-код не було збережено у файл {fname}")
    return FSuccess

def configToPrint(lex,numRow):
    stage = '\nКрок трансляцiї\n'
    stage += 'лексема: \'{0}\'\n'
    stage += 'postfixCode = {3}\n'
    print(stage.format(lex,numRow,str(tableOfSymb[numRow]),str(postfixCode)))


# Функція для збереження у файлі postfix-програми
# це інформація з таблиць:
# tableOfVar
# tableOfLabel
# tableOfConst
# postfixCodeTSM
def savePostfixCode(fileName):
    fname = fileName + ".postfix"
    f = open(fname, 'w')
    header = ".target: Postfix Machine\n.version: 0.2\n"
    f.write(header)

    f.write("\n" + ".vars" + "(\n")
    for id in tableOfVar:
        f.write("   {0:4}  {1:10} \n".format(id, tableOfVar[id][1]))
    f.write(")\n")

    f.write("\n" + ".labels" + "(\n")
    for lbl in tableOfLabel:
        f.write("   {0:4}{1:4} \n".format(lbl, tableOfLabel[lbl]))
    f.write(")\n")

    f.write("\n" + ".constants" + "(\n")
    for literal in tableOfConst:
        f.write("{0:4}  {1:10} \n".format( literal,tableOfConst[literal][0]))
    f.write(")\n")


    f.write("\n" + ".code" + "(\n")
    for instr in postfixCode:
        f.write("   " + str(instr[0]).ljust(6) + str(instr[1]).ljust(6) + "\n")
    f.write(")\n")

    f.close()
    print(f"postfix-код збережено у файлі {fname}")

def setValLabel(lbl):
    global tableOfLabel
    lex,_tok = lbl
    tableOfLabel[lex] = len(postfixCode)
    return True

def createLabel():
    global tableOfLabel
    nmb = len(tableOfLabel)+1
    lexeme = "m"+str(nmb)
    val = tableOfLabel.get(lexeme)
    if val is None:
        tableOfLabel[lexeme] = 'val_undef'
        tok = 'label'
    else:
        tok = 'Конфлiкт мiток'
        print(tok)
        exit(1003)

    return (lexeme,tok)


# запуск парсера
#if FSuccess == ('Lexer', True):
    #parseProgram()
compileToPostfix("test.my_lang")


