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
       [0]  int32 a,
       [1]  int32 b,
       [2]  int32 c,
       [3]  int32 k,
       [4]  int32 v
     )

   .entrypoint
   //.maxstack  8
    ldloca    b
    ldc.i4    3
    stind.i4
    ldloca    c
    ldc.i4    0
    stind.i4
    ldloca    k
    ldc.i4    0
    stind.i4
    ldloca    v
    ldc.i4    0
    stind.i4
    ldloc    b
    ldc.i4    1
    ceq
    brfalse    m1
    ldloca    v
    ldc.i4    1
    stind.i4
    br    m2
m1:
    ldloca    v
    ldc.i4    4
    stind.i4
m2:
	ldstr "a = "
	call void [mscorlib]System.Console::Write(string) 
	ldloc  a
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
	ldstr "v = "
	call void [mscorlib]System.Console::Write(string) 
	ldloc  v
	call void [mscorlib]System.Console::WriteLine(int32) 
	ret    
}
}