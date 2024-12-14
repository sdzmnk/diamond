#dcd
def saveCIL(fileName,tableOfVar,postfixCodeCLR):
  fname = fileName + ".il"
  f = open(fname, 'w')
  header = """// Referenced Assemblies.
.assembly extern mscorlib
{
  .publickeytoken = (B7 7A 5C 56 19 34 E0 89 ) 
  .ver 4:0:0:0
}

// Our assembly.
.assembly """ +fileName+ """
{
  .hash algorithm 0x00008004
  .ver 0:0:0:0
}

.module """ +fileName+ """.exe

// Definition of Program class.
.class private auto ansi beforefieldinit Program
  extends [mscorlib]System.Object
{
    
    .method private hidebysig static void Main(string[] args) cil managed
    {
    .locals (
"""


  cntVars = len(tableOfVar)      
  localVars = ""
  comma = ","
  for x in tableOfVar:
    index,tp,_ = tableOfVar[x]
    if tp == 'int': tpil = 'int32' 
    else: tpil = 'float32'
    localVars += "       [{0}]  {1} {2}".format(index-1,tpil, x) + comma + "\n"
    if index == cntVars-1: comma = "\n     )"
  # print((x,a))
  entrypoint = """
   .entrypoint
   //.maxstack  16\n"""
  code = ""
  for instr in postfixCodeCLR:
    code += instr + "\n"
    
  # виведення значень усіх змінних
  values = ""
  for x in tableOfVar:
    values += "\t" + 'ldstr "' + x + ' = "\n'
    values += "\t" + "call void [mscorlib]System.Console::Write(string) \n"
    _,tp,_ = tableOfVar[x]
    tp += '32'
    values += "\t" + "ldloc  " + x + "\n"
    values += "\t" + "call void [mscorlib]System.Console::WriteLine(" +tp + ") \n"
    
  f.write(header + localVars + entrypoint + code  + values +"\tret    \n}\n}")
  f.close()
  print(f"IL-програма для CLR збережена у файлі {fname}")