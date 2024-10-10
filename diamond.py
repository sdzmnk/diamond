# Write# Таблиця лексем мови
tokenTable = {
    'true': 'boolval', 'false': 'boolval', 'puts': 'keyword', 'for': 'keyword', 'chomp': 'keyword',
    'end': 'keyword', 'if': 'keyword', 'gets': 'keyword', 'to_i': 'keyword', 'to_f': 'keyword',
    '=': 'assign_op', '+': 'add_op', '-': 'add_op', '*': 'mult_op', '/': 'mult_op',
    '<': 'rel_op', '>': 'rel_op', '**': 'pow_op', '<=': 'rel_op', '>=': 'rel_op', '==': 'rel_op',
    '!=': 'rel_op', '(': 'brackets_op', ')': 'brackets_op', '.': 'punct', ',': 'punct', '"': 'punct',
    ':': 'punct', '#': 'sharp', ' ': 'ws', '\t': 'ws', '\n': 'eol', '\r\n': 'eol',
    'until': 'keyword', 'switch': 'keyword', 'case': 'keyword', 'elif': 'keyword', 'default': 'keyword',
    'split': 'keyword', 'do': 'keyword', 'else': 'keyword', 'in': 'keyword', 'while': 'keyword',
    ']': 'brackets_op', '[': 'brackets_op', '..': 'range_op'
}
# Решту токенів визначаємо не за лексемою, а за заключним станом
tokStateTable = {2: 'id', 5: 'float', 6: 'int', 9: 'rel_op or assign_op', 11: 'mult_op', 24: 'comment', 28:'dot', 29:'add_op'}

# Діаграма станів
#               Q                                                                                                               q0          F
# M = ({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,22, 23, 24, 25, 26, 27, 28, 101, 102}, Σ,   , 0 ,  {2, 5, 6, 8, 9, 11, 12, 13, 17, 18, 20, 24, 25, 27, 28, 101, 102})

#  - state-transition_function
stf = {(0, 'Letter'): 1, (1, 'Letter'): 1, (1, 'Digit'): 1, (1, 'underline'): 1, (1, 'other'): 2,
       (0, 'Digit'): 3, (3, 'Digit'): 3, (3, 'dot'): 4, (3, 'other'): 6,
       (4, 'Digit'): 4,  (4, 'other'): 5,

       (0, '<'): 7, (0, '>'): 7, (0, '='): 7, (7, '='): 8,
                                              (7, 'other'): 9,
       (0, '*'): 10, (10, '*'): 12,
       (10, 'other'): 11,
       (0, '['): 13, (0, ']'): 13, (0, '('): 13, (0, ')'): 13, (0, '/'): 13,
       (0, ','): 13,(0, '"'): 13, (0, ':'): 13,
       (0, '+'): 14, (0, '-'): 14, (14, 'other'): 29, (14, 'Digit'): 3,
       (0, '!'): 19, (19, '='): 20,
       (19, 'other'): 102,
       (0, '#'): 22, (22, 'Digit'): 22, (22, 'Letter'): 22, (22, '-'): 22,  (22, '['): 22, (22, ']'): 22,
       (22, '('): 22, (22, ')'): 22, (22, '/'): 22, (22, ','): 22,(22, '"'): 22, (22, ':'): 22, (22, '+'): 22,
       (22, '-'): 22, (22, 'dot'): 22,  (22, 'ws'): 22, (22, 'eol'): 24,
       (0, 'eol'): 25,
       (0, 'dot'): 26, (26, 'dot'): 27, (26, 'Letter'): 30,
                    (27, 'other'): 28, (26, 'other'): 101, (30, 'other'): 101,
       (0, 'other'): 101,
       (0, 'ws'): 0,
       }

initState = 0  # q0 - стартовий стан
F = {2, 5, 6, 8, 9, 11, 12, 13, 20, 24, 25, 27, 28, 29, 30, 101, 102}
Fstar = {2, 5, 6, 9, 11, 17, 18, 29, 30}  # зірочка
Ferror = {101, 102}  # обробка помилок

tableOfId = {}  # Таблиця ідентифікаторів
tableOfConst = {}  # Таблиць констант
tableOfSymb = {}  # Таблиця символів програми (таблиця розбору)

state = initState  # поточний стан

f = open('test.my_lang', 'r')
sourceCode = f.read()
f.close()

# щоб коректно обробити код у випадку,
# якщо після останньої лексеми немає пробільного символу
# або символа нового рядка
sourceCode+=' '

# FSuccess - ознака успішності/неуспішності розбору
FSuccess = ('Lexer',False)

lenCode = len(sourceCode) - 1  # номер останнього символа у файлі з кодом програми
numLine = 1  # лексичний аналіз починаємо з першого рядка
numChar = -1  # з першого символа (в Python'і нумерація - з 0)
char = ''  # ще не брали жодного символа
lexeme = ''  # ще не починали розпізнавати лексеми


def lex():
    global state, numLine, char, lexeme, numChar, FSuccess
    try:
        while numChar < lenCode:
            char = nextChar()  # прочитати наступний символ
            classCh = classOfChar(char)  # до якого класу належить
            state = nextState(state, classCh)  # обчислити наступний стан
            if (is_final(state)):  # якщо стан заключний
                processing()  # виконати семантичні процедури
            elif state == initState:
                lexeme = ''  # якщо стан НЕ заключний, а стартовий - нова лексема
            else:
                lexeme += char  # якщо стан НЕ закл. і не стартовий - додати символ до лексеми
        print('Lexer: Лексичний аналіз завершено успішно')
        FSuccess = ('Lexer', True)
        return FSuccess
    except SystemExit as e:
        # Повідомити про факт виявлення помилки
        print('Lexer: Аварійне завершення програми з кодом {0}'.format(e))


#Мой код
def processing():
  global state,lexeme,char,numLine,numChar, tableOfSymb

  if state==25:		# \n
    numLine+=1
    state=initState

  if state in (2,5,6,17,18):	# keyword, id, float, int
    token=getToken(state,lexeme)
    if token!='keyword': # не keyword
      index=indexIdConst(state,lexeme)
      # print('{0:<3d} {1:<10s} {2:<10s} {3:<5d} '.format(numLine,lexeme,token,index))
      print(numLine, "  ",  lexeme,  "  ", token, "  ", index)
      tableOfSymb[len(tableOfSymb)+1] = (numLine,lexeme,token,index)
    else: # якщо keyword
      # print('{0:<3d} {1:<10s} {2:<10s} '.format(numLine,lexeme,token))
      print(numLine, "  ",  lexeme,  "  ", token)
      tableOfSymb[len(tableOfSymb)+1] = (numLine,lexeme,token,'')
    lexeme=''
    numChar=putCharBack(numChar) # зірочка
    state=initState

  if state == 27:  # Оператор діапазону
      lexeme += char
      token = 'range_op'
      print(numLine, "  ", lexeme, "  ", token)
      tableOfSymb[len(tableOfSymb) + 1] = (numLine, lexeme, token, '')
      lexeme = ''
      state = initState

  if state == 24:  # коментар
      # Коментарі ігноруються, тому не додаються до таблиці символів
      lexeme = ''  # Очищаємо лексему, щоб не зберігати коментар
      numChar = putCharBack(numChar)  # Повертаємо останній символ для подальшої обробки
      state = initState  # Повертаємось до початкового стану

  if state in (12,13,20,8,11,28):
    lexeme+=char
    token=getToken(state,lexeme)
    print('{0:<3d} {1:<10s} {2:<10s} '.format(numLine,lexeme,token))
    tableOfSymb[len(tableOfSymb)+1] = (numLine,lexeme,token,'')
    lexeme=''
    state=initState

  if state == 9:  # real_op or assign_op
      token = getToken(state, lexeme)
      if token == '':
          token = 'rel_op'  # Якщо токен не знайдено, вважаємо його операцією порівняння
      print('{0:<3d} {1:<10s} {2:<10s} '.format(numLine, lexeme, token))
      tableOfSymb[len(tableOfSymb) + 1] = (numLine, lexeme, token, '')
      lexeme = ''
      state = initState


  if state in (29, 30):  # punct (стан пунктуації)
      token = getToken(state, lexeme)
      print('{0:<3d} {1:<10s} {2:<10s} '.format(numLine, lexeme, token))
      tableOfSymb[len(tableOfSymb) + 1] = (numLine, lexeme, token, '')
      lexeme = ''
      numChar = putCharBack(numChar)  # зірочка
      state = initState


  if state in Ferror:  #(101,102):  # ERROR
    fail()

def fail():
    global state, numLine, char
    print(numLine)
    if state == 101:
        print('Lexer: у рядку ', numLine, ' неочікуваний символ ' + char)
        exit(101)
    if state == 102:
        print('Lexer: у рядку ', numLine, ' очікувався символ =, а не ' + char)
        exit(102)


def is_final(state):
    if (state in F):
        return True
    else:
        return False


def nextState(state, classCh):
    try:
        return stf[(state, classCh)]
    except KeyError:
        return stf[(state, 'other')]


def nextChar():
    global numChar
    numChar += 1
    return sourceCode[numChar]


def putCharBack(numChar):
    return numChar - 1


def classOfChar(char):
    if char in '.':
        res = "dot"
    elif char in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ':
        res = "Letter"
    elif char in "0123456789":
        res = "Digit"
    elif char in " ":
        res = "ws"
    elif char in "_":
        res = "underline"
    elif char in "\n":
        res = "eol"
    elif char in ",;:<>!+-=*/()[]#\"":
        res = char

    else:
        res = 'символ не належить алфавіту'
    return res


def getToken(state, lexeme):
    try:
        return tokenTable[lexeme]
    except KeyError:
        return tokStateTable[state]


def indexIdConst(state, lexeme):
    indx = 0
    if state == 2:
        indx = tableOfId.get(lexeme)
        if indx is None:
            indx = len(tableOfId) + 1
            tableOfId[lexeme] = indx
    if state in (5, 6, 9):
        indx = tableOfConst.get(lexeme)
        if indx is None:
            indx = len(tableOfConst) + 1
            tableOfConst[lexeme] = (tokStateTable[state], indx)
    return indx



# запуск лексичного аналізатора
lex()

# Таблиці: розбору, ідентифікаторів та констант
print('-' * 30)
print('tableOfSymb:{0}'.format(tableOfSymb))
print('tableOfId:{0}'.format(tableOfId))
print('tableOfConst:{0}'.format(tableOfConst))

