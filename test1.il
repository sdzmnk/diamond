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
       [1]  int32 c,
       [2]  float32 s,
       [3]  float32 d
     )

   .entrypoint
   //.maxstack  8
    ldloca    a
    ldc.i4    10
    ldc.i4    2
    add
    stind.i4
    ldloca    c
    ldc.i4    200
    stind.i4
    ldloca    s
    ldc.r4    0.5
    ldc.r4    1.0
    div
    stind.r4
    ldloc    s
    ldc.r4    4.50
    ceq
    brfalse    m1
    ldloca    s
    ldloc    s
    ldc.r4    0.5
    add
    stind.r4
    br    m2
m1:
    ldloca    s
    ldloc    s
    ldc.i4    5
    sub
    stind.r4
m2:
    ldloca    d
    ldc.r4    10.0
    stind.r4
	ldstr "a = "
	call void [mscorlib]System.Console::Write(string) 
	ldloc  a
	call void [mscorlib]System.Console::WriteLine(int32) 
	ldstr "c = "
	call void [mscorlib]System.Console::Write(string) 
	ldloc  c
	call void [mscorlib]System.Console::WriteLine(int32) 
	ldstr "s = "
	call void [mscorlib]System.Console::Write(string) 
	ldloc  s
	call void [mscorlib]System.Console::WriteLine(float32) 
	ldstr "d = "
	call void [mscorlib]System.Console::Write(string) 
	ldloc  d
	call void [mscorlib]System.Console::WriteLine(float32) 
	ret    
}
}