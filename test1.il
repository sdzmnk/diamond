// Referenced Assemblies.
.assembly extern mscorlib
{
  .publickeytoken = (B7 7A 5C 56 19 34 E0 89 ) 
  .ver 4:0:0:0
}

// Our assembly.
.assembly test1
{
  .hash algorithm 0x00008004
  .ver 0:0:0:0
}

.module test1.exe

// Definition of Program class.
.class private auto ansi beforefieldinit Program
  extends [mscorlib]System.Object
{
    
    .method private hidebysig static void Main(string[] args) cil managed
    {
    .locals (
       [0]  int32 v,
       [1]  int32 b,
       [2]  int32 c,
       [3]  int32 k,
       [4]  int32 s,
       [5]  int32 u,
       [6]  int32 w,
       [7]  int32 i1,
       [8]  float32 i2,
       [9]  int32 i3,
       [10]  int32 sw1,
       [11]  int32 sw2,
       [12]  int32 sw3,
       [13]  int32 sw4,
       [14]  int32 a,
       [15]  float32 exp1,
       [16]  int32 exp2,
       [17]  float32 exp3,
       [18]  int32 test,
       [19]  int32 inp1,
       [20]  float32 inp2
     )

   .entrypoint
   //.maxstack  16
    ldloca    exp2
    ldc.i4    11
    stind.r4
    ldloca    exp2
    ldc.i4    1
    ldc.i4    3
    add
    ldc.i4    2
    sub
    stind.i4
    ldloca    exp3
    ldc.i4    10
    ldc.i4    3
    sub
    ldc.i4    4
    ldc.i4    2
    add
    add
    stind.r4
	ldstr "v = "
	call void [mscorlib]System.Console::Write(string) 
	ldloc  v
	call void [mscorlib]System.Console::WriteLine(int32) 
	ldstr "b = "
	call void [mscorlib]System.Console::Write(string) 
	ldloc  b
	call void [mscorlib]System.Console::WriteLine(int32) 
	ldstr "c = "
	call void [mscorlib]System.Console::Write(string) 
	ldloc  c
	call void [mscorlib]System.Console::WriteLine(int32) 
	ldstr "k = "
	call void [mscorlib]System.Console::Write(string) 
	ldloc  k
	call void [mscorlib]System.Console::WriteLine(int32) 
	ldstr "s = "
	call void [mscorlib]System.Console::Write(string) 
	ldloc  s
	call void [mscorlib]System.Console::WriteLine(int32) 
	ldstr "u = "
	call void [mscorlib]System.Console::Write(string) 
	ldloc  u
	call void [mscorlib]System.Console::WriteLine(int32) 
	ldstr "w = "
	call void [mscorlib]System.Console::Write(string) 
	ldloc  w
	call void [mscorlib]System.Console::WriteLine(int32) 
	ldstr "i1 = "
	call void [mscorlib]System.Console::Write(string) 
	ldloc  i1
	call void [mscorlib]System.Console::WriteLine(int32) 
	ldstr "i2 = "
	call void [mscorlib]System.Console::Write(string) 
	ldloc  i2
	call void [mscorlib]System.Console::WriteLine(float32) 
	ldstr "i3 = "
	call void [mscorlib]System.Console::Write(string) 
	ldloc  i3
	call void [mscorlib]System.Console::WriteLine(int32) 
	ldstr "sw1 = "
	call void [mscorlib]System.Console::Write(string) 
	ldloc  sw1
	call void [mscorlib]System.Console::WriteLine(int32) 
	ldstr "sw2 = "
	call void [mscorlib]System.Console::Write(string) 
	ldloc  sw2
	call void [mscorlib]System.Console::WriteLine(int32) 
	ldstr "sw3 = "
	call void [mscorlib]System.Console::Write(string) 
	ldloc  sw3
	call void [mscorlib]System.Console::WriteLine(int32) 
	ldstr "sw4 = "
	call void [mscorlib]System.Console::Write(string) 
	ldloc  sw4
	call void [mscorlib]System.Console::WriteLine(int32) 
	ldstr "a = "
	call void [mscorlib]System.Console::Write(string) 
	ldloc  a
	call void [mscorlib]System.Console::WriteLine(int32) 
	ldstr "exp1 = "
	call void [mscorlib]System.Console::Write(string) 
	ldloc  exp1
	call void [mscorlib]System.Console::WriteLine(float32) 
	ldstr "exp2 = "
	call void [mscorlib]System.Console::Write(string) 
	ldloc  exp2
	call void [mscorlib]System.Console::WriteLine(int32) 
	ldstr "exp3 = "
	call void [mscorlib]System.Console::Write(string) 
	ldloc  exp3
	call void [mscorlib]System.Console::WriteLine(type_error32) 
	ldstr "test = "
	call void [mscorlib]System.Console::Write(string) 
	ldloc  test
	call void [mscorlib]System.Console::WriteLine(int32) 
	ldstr "inp1 = "
	call void [mscorlib]System.Console::Write(string) 
	ldloc  inp1
	call void [mscorlib]System.Console::WriteLine(int32) 
	ldstr "inp2 = "
	call void [mscorlib]System.Console::Write(string) 
	ldloc  inp2
	call void [mscorlib]System.Console::WriteLine(float32) 
	ret    
}
}