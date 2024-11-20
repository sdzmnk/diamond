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
            res = True
        elif lex == 'to_f':
            parseToken('to_f', 'keyword')
            resType = 'float'
            res = True
        else:
            numLine, lex, tok = getSymb()
            failParse('невідповідність інструкцій', (numLine, lex, tok, 'to_i або to_f'))
            res = False
    else:
        res = False
    indent = predIndt()
    return resType, res


def parseDeclaration():
    global numRow
    indent = nextIndt()
    print(indent + 'parseDeclaration():')
    numLine, lex, tok = getSymb()

    resType = None
    # Розбираємо ідентифікатори з лівого боку присвоєння
    lType = parseIdentList()  # Отримуємо список ідентифікаторів

    # Переконатися, що токен '=' правильно розібраний
    parseToken('=', 'assign_op')

    # Розбираємо вирази з правого боку присвоєння
    rType = parseExpressionList()  # Отримуємо список виразів

    # Перевіряємо, чи кількість ідентифікаторів відповідає кількості виразів
    if len(lType) != len(rType):
        failParse('кількість ідентифікаторів не дорівнює кількості значень', (numLine))

    # Обробка пар ідентифікаторів і виразів
    i = 0
    n = 2
    while i < len(lType):  # Проходимо по всіх ідентифікаторах
        # Отримуємо тип операції
        resType = getTypeOp(lType[i], '=', rType[i])

        # Оновлення таблиці змінних для поточного ідентифікатора
        tableOfVar[lex] = (n, resType, 'assigned')
        n += 1
        # Отримання наступного ключа після поточного
        next_lex = get_next_key(tableOfVar, lex)
        if next_lex:
            lex = next_lex  # Оновлюємо lex на наступний ключ
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

                resType = getTypeOp(lTypebrac, '+', rType)
                tableOfVar[lex] = (tableOfVar[lex][0], resType, 'assigned')  # Оновлюємо тип змінної

                if resType == 'type_error':
                    failParse(resType, (numLine, lexN,))
                res = True
            if isExtendedExpression == False:
                resType = getTypeOp(lType, '=', rType)

                tableOfVar[lex] = (tableOfVar[lex][0], resType, 'assigned')  # Оновлюємо тип змінної

                if resType == 'type_error':
                    failParse(resType, (numLine, lexN,))
                res = True

        else:

            rType = parseExpression()
            resType = getTypeOp(lType, '=', rType)
            tableOfVar[lex] = (tableOfVar[lex][0], resType, 'assigned')  # Оновлюємо тип
            if resType == 'type_error':
                failParse(resType, (numLine, lexN,))
            res = True
    elif lexT == ',':
        parseToken(',', 'punct')
        parseDeclaration()
        type = tableOfConst[firstNumber][0]
        resType = getTypeOp(lex, '=', type)
        tableOfVar[lex] = (tableOfVar[lex][0], resType, 'assigned')

        res = True
    else:
        res = False
    isInitVar(lex)
    indent = predIndt()
    return resType, res


def parseExpression():
    global numRow
    # відступ збільшити
    indent = nextIndt()
    print(indent + 'parseExpression():')
    numLine, lex, tok = getSymb()
    lType = parseTerm()
    # print(lex)
    if lType == 'id':
        lType = getTypeVar(lex)
        if lType == 'undeclared_variable':
            failParse('використання неоголошеної змінної', (numLine, lex, tok))
        else:
            if tableOfVar[lex][2] == 'undefined':  # Перевірка, чи змінна має значення
                tpl = (numLine)  # Використання неоголошеної або неініціалізованої змінної
                failParse('використання змінної, що не набула значення', tpl)
            else:
                var_type = tableOfVar[lex][1]
                lType = var_type
    resType = lType
    F = True
    while F:
        numLineT, lexT, tokT = getSymb()

        if tokT in ('add_op', 'rel_op', 'mult_op', 'pow_op'):
            numRow += 1
            numLineR, lexR, tokR = getSymb()
            print(indent + 'в рядку {0} - токен {1}'.format(numLineT, (lexT, tokT)))
            rType = parseTerm()

            if lexT == '/' and lexR == '0':
                tpl = (numLine)  # Використання неоголошеної або неініціалізованої змінної
                failParse('ділення на нуль', tpl)
            if rType == 'id':
                if tableOfVar[lexR][2] == 'undefined':  # Перевірка, чи змінна має значення
                    tpl = (numLine)  # Використання неоголошеної або неініціалізованої змінної
                    failParse('використання змінної, що не набула значення', tpl)
                else:
                    var_type = tableOfVar[lexR][1]
                    rType = var_type


            resType = getTypeOp(lType, lexT, rType)
            if resType != 'type_error':
                lType = resType
            else:
                tpl = (numLine, lType, lex, rType)  # для повiдомлення про помилку
                failParse(resType, tpl)

        else:
            F = False
    # перед поверненням - зменшити відступ
    indent = predIndt()
    return resType



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

def parseSwitch():
    global numRow
    # відступ збільшити
    indent = nextIndt()
    numLine, lex, tok = getSymb()
    if lex == 'switch' and tok == 'keyword':
        print(indent + 'в рядку {0} - токен {1}'.format(numLine, (lex, tok)))
        numRow += 1
        parseDigit() or parseIdent()
        parseToken('do', 'keyword')
        while parseCaseBlock():
            pass  # Виконуємо парсинг блоків case, поки це можливо
        parseDefaultBlock()
        parseToken('end', 'keyword')
        res = True
    else:
        res = False
    # перед поверненням - зменшити відступ
    indent = predIndt()
    return res

def parseCaseBlock():
    global numRow
    # відступ збільшити
    indent = nextIndt()
    numLine, lex, tok = getSymb()
    if lex == 'case' and tok == 'keyword':
        print(indent + 'в рядку {0} - токен {1}'.format(numLine, (lex, tok)))
        numRow += 1
        #getIdent()
        parseDigit() or parseIdent()
        parseToken(':', 'punct')
        parseStatementListSwitch()
        res = True
    else:
        res = False
    # перед поверненням - зменшити відступ
    indent = predIndt()
    return res

def parseDefaultBlock():
    global numRow
    indent = nextIndt()
    numLine, lex, tok = getSymb()
    if lex == 'default' and tok == 'keyword':
        print(indent + 'в рядку {0} - токен {1}'.format(numLine, (lex, tok)))
        numRow += 1
        parseToken(':', 'punct')
        parseStatementList()
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
                lex = str(-float(lex)) if '.' in lex else str(-int(lex))  # Застосовуємо унарний мінус
            elif unary_op == '+':
                lex = str(float(lex)) if '.' in lex else str(int(lex))  # Унарний плюс не змінює значення
            numRow += 1  # Переходимо до наступної лексеми
            print(indent + 'в рядку {0} - токен {1}'.format(numLine, (lex, tok)))
            return 'float' if '.' in lex else 'int'  # Повертаємо тип числа
        else:
            failParse('Унарний оператор застосовано не до числа', (numLine, lex, tok))

    if tok in ('int', 'float', 'id', 'add_op', 'mult_op'):
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

def parseIf():
    global numRow
    # відступ збільшити
    indent = nextIndt()
    numLine, lex, tok = getSymb()
    resType = None
    if lex == 'if' and tok == 'keyword':
        print(indent + 'в рядку {0} - токен {1}'.format(numLine, (lex, tok)))
        numRow += 1
        parseBoolExpr()
        parseStatementList()  # Виконуємо парсинг блоку if
        #parseToken('elif', 'keyword')
        while True:
            numLine, lex, tok = getSymb()
            if lex == 'elif' and tok == 'keyword':
                print(indent + 'в рядку {0} - токен {1}'.format(numLine, (lex, tok)))
                numRow += 1
                parseBoolExpr() # Парсинг логічного виразу в elif
                parseStatementList()  # Парсинг блоку elif
            elif lex == 'else' and tok == 'keyword':
                print(indent + 'в рядку {0} - токен {1}'.format(numLine, (lex, tok)))
                numRow += 1
                parseStatementList()  # Парсинг блоку else
                break  # Вийти з циклу після обробки else
            else:
                # Якщо токен не elif або else, повертаємося до завершення if
                break
        parseToken('end', 'keyword')
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
    if lex == 'while' and tok == 'keyword':
        print(indent + 'в рядку {0} - токен {1}'.format(numLine, (lex, tok)))
        numRow += 1
        parseBoolExpr()
        parseToken('do', 'keyword')
        parseStatementList()
        parseToken('end', 'keyword')
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

    numLine, lex, tok = getSymb()
    if lex == 'until' and tok == 'keyword':
        print(indent + 'в рядку {0} - токен {1}'.format(numLine, (lex, tok)))
        numRow += 1
        parseBoolExpr()
        parseToken('do', 'keyword')
        parseStatementList()
        parseToken('end', 'keyword')
        res = True
    else:
        res = False
    # перед поверненням - зменшити відступ
    indent = predIndt()
    return res

def parseFor():
    global numRow
    # відступ збільшити
    indent = nextIndt()
    numLine, lex, tok = getSymb()
    if lex == 'for' and tok == 'keyword':
        print(indent + 'в рядку {0} - токен {1}'.format(numLine, (lex, tok)))
        numRow += 1
        parseIdent()
        parseToken('in', 'keyword')
        parseRange()
        parseToken('do', 'keyword')
        parseStatementList()
        parseToken('end', 'keyword')
        res = True
    else:
        res = False
    # перед поверненням - зменшити відступ
    indent = predIndt()
    return res


def parseRange():
    global numRow
    indent = nextIndt()
    print(indent + 'parseRange():')

    # Очікувати лексему '['
    parseToken('[', 'brackets_op')

    # Розбирати перше значення діапазону
    parseExpression()

    # Очікувати лексему '..' для визначення діапазону
    parseToken('..', 'range_op')

    # Розбирати друге значення діапазону
    parseExpression()

    # Очікувати лексему ']'
    parseToken(']', 'brackets_op')

    # перед поверненням - зменшити відступ
    indent = predIndt()
    return True

# розбір логічного виразу за правиллом
# BoolExpr = Expression ('='|'<='|'>='|'<'|'>'|'<>') Expression
def parseBoolExpr():
    global numRow
    # відступ збільшити
    indent = nextIndt()
    print(indent + 'parseBoolExpr():')
    numLine, lex, tok = getSymb()
    parseTerm()
    F = True
    # продовжувати розбирати Доданки (Term)
    # розділені лексемами '+' або '-'
    while F:
        numLine, lex, tok = getSymb()
        if tok in ('rel_op'):
            numRow += 1
            print(indent + 'в рядку {0} - токен {1}'.format(numLine, (lex, tok)))
            parseTerm()
        else:
            failParse('mismatch in BoolExpr', (numLine, lex, tok, 'rel_op'))
            F = False
    # перед поверненням - зменшити відступ
    indent = predIndt()
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
            res = True
            numRow += 1  # Переходимо до наступної лексеми

        elif next_tok == 'punct' and next_lex == '"':
            parseToken(next_lex, next_tok)
            # Перевіряємо на ідентифікатор всередині лапок
            if parseIdent():
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
    numLine, lex, tok = getSymb()
    indent = nextIndt()  # Збільшуємо відступ для виводу
    print(indent + 'parseExpressionList():')  # Виводимо назву функції

    resType = []  # Ініціалізуємо список для збереження типів виразів
    firstNumber = lex  # Зберігаємо значення першого виразу

    # Розбираємо перше вираження, але не додаємо до списку
    parseExpression()

    # Поки є символи коми, продовжуємо розбір виражень
    while True:
        numLine, lex, tok = getSymb()  # Отримуємо наступний токен

        if tok == 'punct' and lex == ',':
            parseToken(',', 'punct')  # Розбираємо кому
            resType.append(parseExpression())  # Додаємо наступний вираз до списку
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


# запуск парсера
if FSuccess == ('Lexer', True):
    parseProgram()


