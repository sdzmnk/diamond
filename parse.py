from diamond import lex
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
        print('tableOfVar:{0}'.format(tableOfVar))
        parseToken('begin', 'keyword')
        # Перевіряємо синтаксичну коректність списку інструкцій
        parseStatementList()
        # Очікуємо ключове слово "end" в кінці
        parseToken('end', 'keyword')
        # повідомити про синтаксичну коректність програми
        print('Parser: Синтаксичний аналіз завершився успішно')

        return True
    except SystemExit as e:
        # Повідомити про факт виявлення помилки
        print('Parser: Аварійне завершення програми з кодом {0}'.format(e))


def parseDeclarList():
    global numRow
    numLine, lex, tok = getSymb()

    while (lex, tok) != ('begin', 'keyword'):  # Доки не зустріли 'begin'
        if tok == 'id':  # Якщо токен - це ідентифікатор
            numRow += 1
            parseToken('^', 'type_var')  # Очікуємо знак типу змінної
            numLineT, lexT, tokT = getSymb()
            numRow += 1
            if lexT in ('int', 'float'):  # Якщо тип змінної - int або float
                procTableOfVar(numLine, lex, tokT, 'undefined')  # Додаємо змінну в таблицю
            else:
                failParse('неприпустимий тип', (numLineT, lexT, tokT))  # Помилка: неправильний тип
        else:
            failParse('очікувався ідентифікатор', (numLine, lex, tok))  # Помилка: очікувався ідентифікатор

        numLine, lex, tok = getSymb()  # Читання наступного токену


def procTableOfVar(numLine, lexeme, type, value):
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
def failParse(str, tuple):
    if str == 'неочікуваний кінець програми':
        (lexeme, token, numRow) = tuple
        print(
            'Parser ERROR: \n\t Неочікуваний кінець програми - в таблиці символів (розбору) немає запису з номером {1}. \n\t Очікувалось - {0}'.format(
                (lexeme, token), numRow))
        exit(1001)
    if str == 'неприпустимий тип':
        (numLine, lexeme, token) = tuple
        print(
            f'Parser ERROR: \n\t Неприпустимий тип - в таблиці символів (розбору) немає запису з номером {numLine}.')
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

# Функція для розбору за правилом для StatementList
# StatementList = Statement  { Statement }
# викликає функцію parseStatement() доти,
# доки parseStatement() повертає True
def parseStatementList():
    # відступ збільшити
    indent = nextIndt()
    print(indent + 'parseStatementList():')
    while parseStatement():
        pass
    # перед поверненням - зменшити відступ
    indent = predIndt()
    return True


def parseStatement():
    # відступ збільшити
    indent = nextIndt()
    print(indent + 'parseStatement():')

    # прочитаємо поточну лексему в таблиці розбору
    numLine, lex, tok = getSymb()


    if tok == 'id':
        parseAssign()
        res = True

    # якщо лексема - ключове слово 'if'
    # обробити інструкцію розгалуження
    elif (lex, tok) == ('if', 'keyword'):
        parseIf()
        res = True

    elif (lex, tok) == ('for', 'keyword'):
      parseFor()
      res = True

    elif (lex, tok) == ('while','keyword'):
        parseWhile()
        res = True

    elif (lex, tok) == ('switch', 'keyword'):
        parseSwitch()
        res = True

    elif (lex, tok) == ('until', 'keyword'):
        parseUntil()
        res = True

    elif (lex, tok) == ('puts', 'keyword'):
        parseOut()
        res = True

    elif (lex, tok) == ('elif', 'keyword'):
        res = False

    elif (lex, tok) == ('else', 'keyword'):
        res = False

    # Перевірка на ключове слово 'end'
    elif (lex, tok) == ('end', 'keyword'):
        res = False  # Повертаємо False, щоб завершити список інструкцій
    else:
        # жодна з інструкцій не відповідає
        # поточній лексемі у таблиці розбору,
        failParse('невідповідність інструкцій', (numLine, lex, tok, 'id або if'))
        res = False
    # перед поверненням - зменшити відступ
    indent = predIndt()
    return res


def parseInp():
    # відступ збільшити
    indent = nextIndt()
    print(indent + 'parseInp():')

    # встановити номер нової поточної лексеми
    if parseToken('gets', 'keyword'):
        parseToken('.', 'punct')
        parseToken('chomp', 'keyword')
        numLine, lex, tok = getSymb()
        if lex == '.':
            parseToken('.', 'punct')
            numLine, lex, tok = getSymb()
            if lex == 'to_i':
                parseToken('to_i', 'keyword')
                res = True

            elif lex == 'to_f':
                parseToken('to_f', 'keyword')
                res = True
            else:
                numLine, lex, tok = getSymb()
                failParse('невідповідність інструкцій', (numLine, lex, tok, 'to_i або to_f'))
                res = False
        res = True

    else:
        res = False
    # перед поверненням - зменшити відступ
    indent = predIndt()
    return res


def parseDeclaration():
    indent = nextIndt()
    print(indent + 'parseDeclaration():')

    # Розбираємо ідентифікатори з лівого боку присвоєння
    parseIdentList()

    # Переконатися, що токен '=' правильно розібраний
    parseToken('=', 'assign_op')

    # Розбираємо вирази з правого боку присвоєння
    parseExpressionListOrInpSplit()

    indent = predIndt()
    return True


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
    numLine, lex, tok = getSymb()

    if lex == '=':
        parseToken('=', 'assign_op')
        numLine, lex, tok = getSymb()

        if lex == 'gets' and tok == 'keyword':
            parseInp()
        else:
            parseExpression()
        res = True

    elif lex == ',':
        parseToken(',', 'punct')
        parseDeclaration()
        res = True
    else:
        res = False
    # перед поверненням - зменшити відступ
    indent = predIndt()
    return res


def parseExpression():
    global numRow
    # відступ збільшити
    indent = nextIndt()
    print(indent + 'parseExpression():')
    numLine, lex, tok = getSymb()
    parseTerm()
    F = True
    # продовжувати розбирати Доданки (Term)
    # розділені лексемами '+' або '-'
    while F:
        numLine, lex, tok = getSymb()
        if tok in ('add_op', 'rel_op', 'mul_op', 'pow_op'):
            numRow += 1
            print(indent + 'в рядку {0} - токен {1}'.format(numLine, (lex, tok)))
            parseTerm()
        else:
            F = False
    # перед поверненням - зменшити відступ
    indent = predIndt()
    return True


# Функція для розбору ідентифікатора
def parseIdent():
    global numRow
    # збільшити відступ
    indent = nextIndt()
    print(indent + 'parseIdent():')

    # взяти поточну лексему
    numLine, lex, tok = getSymb()

    # перевірити, чи є лексема ідентифікатором
    if tok == 'id':
        numRow += 1  # переміщуємося до наступної лексеми
        print(indent + 'в рядку {0} - токен {1}'.format(numLine, (lex, tok)))
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
    while True:
        numLine, lex, tok = getSymb()
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
    parseFactor()
    F = True
    # продовжувати розбирати Множники (Factor)
    # розділені лексемами '*' або '/'
    while F:
        numLine, lex, tok = getSymb()
        if tok in ('mult_op'):
            numRow += 1
            print(indent + 'в рядку {0} - токен {1}'.format(numLine, (lex, tok)))
            parseFactor()
        else:
            F = False
    # перед поверненням - зменшити відступ
    indent = predIndt()
    return True


def parseFactor():
    global numRow
    # відступ збільшити
    indent = nextIndt()
    print(indent + 'parseFactor():')
    numLine, lex, tok = getSymb()

    if tok in ('int', 'float', 'id', 'add_op'):
        numRow += 1
        print(indent + 'в рядку {0} - токен {1}'.format(numLine, (lex, tok)))
        if tok in ('add_op'):
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
    return True


# розбір інструкції розгалуження за правилом
# IfStatement = if BoolExpr then Statement else Statement endif
# функція названа parseIf() замість parseIfStatement()

def parseIf():
    global numRow
    # відступ збільшити
    indent = nextIndt()
    numLine, lex, tok = getSymb()

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
    return res


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

    # Розбираємо перший ідентифікатор
    parseIdent()

    # Поки є символи коми, продовжуємо розбір ідентифікаторів
    while True:
        numLine, lex, tok = getSymb()  # Отримуємо наступний токен

        if tok == 'punct' and lex == ',':
            parseToken(',', 'punct')  # Розбираємо кому
            parseIdent()  # Розбираємо наступний ідентифікатор
        else:
            # Якщо токен не кома, виходимо з циклу
            break

    indent = predIndt()  # Зменшуємо відступ перед поверненням
    return True  # Повертаємо True, якщо розбір пройшов успішно


def parseExpressionList():
    indent = nextIndt()  # Збільшуємо відступ для виводу
    print(indent + 'parseExpressionList():')  # Виводимо назву функції

    # Розбираємо перше вираження
    parseExpression()

    # Поки є символи коми, продовжуємо розбір виражень
    while True:
        numLine, lex, tok = getSymb()  # Отримуємо наступний токен

        if tok == 'punct' and lex == ',':
            parseToken(',', 'punct')  # Розбираємо кому
            parseExpression()  # Розбираємо наступне вираження
        else:
            # Якщо токен не кома, виходимо з циклу
            break

    indent = predIndt()  # Зменшуємо відступ перед поверненням
    return True  # Повертаємо True, якщо розбір пройшов успішно



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


