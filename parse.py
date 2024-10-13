from sre_parse import parse

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


# Функція для розбору за правилом
# Program = program StatementList end=
# читає таблицю розбору tableOfSymb
def parseProgram():
    try:
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


    # try:
    #   # перевірити синтаксичну коректність списку інструкцій IdentList1
    #   parseIdentList1()
    #
    #   return True
    # except SystemExit as e:
    #   # Повідомити про факт виявлення помилки
    #   print('Parser: Написати помилку №№№№ {0}'.format(e))

    # якщо токен - ідентифікатор
    # обробити інструкцію присвоювання
    if tok == 'id':
        parseAssign()
        res = True

    # якщо лексема - ключове слово 'if'
    # обробити інструкцію розгалуження
    elif (lex, tok) == ('if', 'keyword'):
        parseIf()
        res = True

        # elif (lex, tok) == ('elif','keyword'):
    #     parseElif()
    #     res = True

    elif (lex, tok) == ('for', 'keyword'):
      parseFor()
      res = True

    # elif (lex, tok) == ('while','keyword'):
    #     parseWhile()
    #     res = True

    # elif (lex, tok) == ('switch', 'keyword'):
    #     parseSwitch()
    #     res = True

    elif (lex, tok) == ('until', 'keyword'):
        parseUntil()
        res = True

    # elif (lex, tok) == ('gets','keyword'):
    #     parseInp()
    #     res = True
    #
    elif (lex, tok) == ('puts', 'keyword'):
        parseOut()
        res = True
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


# def parseIdentList1():
#   indent = nextIndt()
#   print(indent+'parseIdentList1():')
#   while parseIndt1(): #для індент через ","
#     pass
#   # перед поверненням - зменшити відступ
#   indent = predIndt()
#   return True
#

def parseInp():
    # відступ збільшити
    indent = nextIndt()
    print(indent + 'parseInp:')

    # встановити номер нової поточної лексеми
    if parseToken('gets', 'keyword'):
        parseToken('.', 'punct')
        parseToken('chomp', 'keyword')
        numLine, lex, tok = getSymb()
        if lex == '.':
            parseToken('.', 'punct')
            if lex == 'to_i':
                parseToken('to_i', 'keyword')
                res = True

            elif lex == 'to_f':
                parseToken('to_f', 'keyword')
                res = True
            else:
                failParse('невідповідність інструкцій', (numLine, lex, tok, 'to_i або to_f'))
                res = False
        res = True

    else:
        res = False
    # перед поверненням - зменшити відступ
    indent = predIndt()
    return res


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

    # print('\t'*5+'в рядку {0} - {1}'.format(numLine,(lex, tok)))
    # якщо була прочитана лексема - '='
    if parseToken('=', 'assign_op'):
        numLine, lex, tok = getSymb()

        if lex == 'gets' and tok == 'keyword':
            parseInp()
        else:
            parseExpression()
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
        if tok in ('add_op'):
            numRow += 1
            print(indent + 'в рядку {0} - токен {1}'.format(numLine, (lex, tok)))
            parseTerm()
        else:
            F = False
    # перед поверненням - зменшити відступ
    indent = predIndt()
    return True


def parseFor():
    global numRow
    # відступ збільшити
    indent = nextIndt()
    numLine, lex, tok = getSymb()
    if lex == 'for' and tok == 'keyword':
        print(indent + 'в рядку {0} - токен {1}'.format(numLine, (lex, tok)))
        numRow += 1
        parseToken('id', 'id')
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
    parseToken('[', 'range_op')

    # Розбирати перше значення діапазону
    parseExpression()

    # Очікувати лексему '..' для визначення діапазону
    parseToken('..', 'range_op')

    # Розбирати друге значення діапазону
    parseExpression()

    # Очікувати лексему ']'
    parseToken(']', 'range_op')

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
    ##### print('\t'*7+'parseFactor():=============рядок: {0}\t (lex, tok):{1}'.format(numLine,(lex, tok)))

    # перша і друга альтернативи для Factor
    # якщо лексема - це константа або ідентифікатор
    if tok in ('int', 'float', 'id'):
        numRow += 1
        print(indent + 'в рядку {0} - токен {1}'.format(numLine, (lex, tok)))

    # третя альтернатива для Factor
    # якщо лексема - це відкриваюча дужка
    elif lex == '(':
        numRow += 1
        parseExpression()
        parseToken(')', 'par_op')
        print(indent + 'в рядку {0} - токен {1}'.format(numLine, (lex, tok)))
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
        parseToken('then', 'keyword')
        parseStatement()
        parseToken('else', 'keyword')
        parseStatement()
        parseToken('endif', 'keyword')
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


# розбір логічного виразу за правиллом
# BoolExpr = Expression ('='|'<='|'>='|'<'|'>'|'<>') Expression
def parseBoolExpr():
    global numRow
    # відступ збільшити
    indent = nextIndt()

    print(indent + 'parseBoolExpr()')
    parseExpression()
    numLine, lex, tok = getSymb()
    if tok in ('rel_op'):
        numRow += 1
        print(indent + 'в рядку {0} - токен {1}'.format(numLine, (lex, tok)))
    else:
        failParse('mismatch in BoolExpr', (numLine, lex, tok, 'relop'))
    parseExpression()
    # перед поверненням - зменшити відступ
    indent = predIndt()
    return True
def parseOut():
    global numRow
    # збільшити відступ
    indent = nextIndt()
    print(indent + 'parseOut():')

    # Отримуємо поточну лексему
    numLine, lex, tok = getSymb()

    # Перевіряємо, чи це ключове слово 'puts'
    if (lex, tok) == ('puts', 'keyword'):
        numRow += 1
        print(indent + 'в рядку {0} токен {1}'.format(numLine, (lex, tok)))
        res = False

        # Спочатку перевіряємо, чи йде після 'puts' число без лапок
        if parseDigit():
            print(indent + 'parseOut(): Коректний синтаксис (число без лапок)')
            res = True
        # Якщо це не число, перевіряємо, чи є лапки
        elif parseToken('"', 'punct'):
            # Перевіряємо на ідентифікатор всередині лапок
            if parseIdent():
                # Перевіряємо на закриваючі лапки
                if parseToken('"', 'punct'):
                    res = True
                else:
                    failParse('Очікувалась закриваюча лапка', (numLine, lex, tok, '"'))
                    res = False
            else:
                failParse('Очікувався ідентифікатор в лапках', (numLine, lex, tok))
                res = False
    else:
        failParse('Невідповідність інструкцій, очікувалось "puts"', (numLine, lex, tok, 'puts'))
        res = False

    # Зменшити відступ
    indent = predIndt()
    return res




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

# Функция для разбора IdentList
def parseIdentList():
    indent = nextIndt()
    print(indent + 'parseIdentList():')

    # Разбираем первый идентификатор
    parseIdent()

    # Пока есть символы запятой, продолжаем разбор идентификаторов
    while parseToken(',', 'punct'):
        parseIdent()

    # уменьшить отступ перед возвратом
    indent = predIndt()
    return True


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

