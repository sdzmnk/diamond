#dcd
def saveForJVM(fileName,postfixCodeJVM,compatibility):
  # для асемблерів
  # Krakatau або Oolong
  # ------------------
  # Krakatau:
  #   мітка має обов'язково
  #   починатись з символа 'L'
  # ------------------
  # Oolong:
  #   інструкції для типу float
  #   fload n та fstore n
  #   працюють тільки для 0 <= n <= 3
  fname = fileName + ".j"
  f = open(fname, 'w')
  header = '.class public ' + fileName + '\n'
  header += '.super java/lang/Object' +'\n'
  # ------------------
  headerOolong = '; для асемблера Oolong\n'
  headerOolong += '.method public static main([Ljava/lang/String;)V ; ' + '\n'
  headerOolong += '.limit stack 8 \n'
  headerOolong += '.limit locals 10 \n'
  # ------------------
  headerKrakatau = '; для асемблера Krakatau\n'
  headerKrakatau += '.method public static main : ([Ljava/lang/String;)V ' + '\n'
  headerKrakatau += '  .code stack 8 locals 10 \n'
  # ------------------
  footer = '.end method \n'
  footer += '.end class \n'
  # ------------------
  footerOolong = ' '*5+'return'+'\n\n'
  # ------------------
  footerKrakatau = ' '*3+'return'+ '\n' +' '*2+'.end code \n' 
  # 
  if compatibility == 'K' or compatibility == 'Krakatau':
    header = header + headerKrakatau
    footer = footerKrakatau + footer
    labelPrefix = 'L'
  elif compatibility == 'O' or compatibility == 'Oolong':
    header = header + headerOolong
    footer = footerOolong + footer
    labelPrefix = ''
  code = ''
  for instr in postfixCodeJVM:
    code += instr + "\n"
  f.write(header+code+footer)
  f.close()
  print(f"j-програма для JVM збережена у файлі {fname}")
