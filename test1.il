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
       [11]  float32 sw2,
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
    ldloca    w
    ldc.i4    0
    stind.i4
    ldloca    b
    ldc.i4    2
    stind.i4
    ldloca    c
    ldc.i4    3
    stind.i4
    ldloca    k
    ldc.i4    0
    stind.i4
    ldloca    v
    ldc.i4    0
    stind.i4
    ldloca    u
    ldc.i4    0
    stind.i4
m2:
    ldloc    w
    ldc.i4    5
    clt
    brfalse    m1
    ldloca    w
    ldloc    w
    ldc.i4    1
    add
    stind.i4
    br    m2
m1:
    ldloc    b
    ldc.i4    1
    ceq
    brfalse    m3
    ldloc    c
    ldc.i4    1
    ceq
    brfalse    m5
    ldloca    k
    ldc.i4    11
    stind.i4
    br    m6
m5:
    ldloc    c
    ldc.i4    2
    ceq
    brfalse    m7
    ldloca    k
    ldc.i4    22
    stind.i4
    br    m6
m7:
    ldloca    k
    ldc.i4    33
    stind.i4
m6:
    br    m4
m3:
    ldloc    b
    ldc.i4    3
    ceq
    brfalse    m8
    ldloca    v
    ldc.i4    2
    stind.i4
    br    m4
m8:
    ldloca    v
    ldc.i4    4
    stind.i4
m4:
m10:
    ldloc    u
    ldc.i4    10
    ceq
    brfalse    m9
    br    m11
m9:
    ldloca    u
    ldloc    u
    ldc.i4    2
    add
    stind.i4
    br    m10
m11:
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
    ldloca    i1
    ldc.i4    1
    stind.i4
    ldloca    i2
    ldc.r4    3.6
    stind.r4
    ldloca    i3
    ldc.i4    9
    stind.i4
    ldloca    sw1
    ldc.i4    2
    neg
    stind.r4
    ldloca    sw2
    ldc.i4    2
    ldc.i4    3
    call float64 [mscorlib]System.Math::Pow(float64, float64)
    conv.r4

    stind.i4
    ldloca    sw3
    ldc.i4    6
    stind.i4
    ldloca    sw4
    ldc.i4    0
    stind.i4
    ldloca    sw1
    ldc.i4    6
    stind.i4
m13:
    ldc.i4    10
    ldloc    sw1
    cgt
    brfalse    m12
    ldloca    sw4
    ldloc    sw4
    ldc.i4    1
    add
    stind.i4
	ldloc  sw4
	call void [mscorlib]System.Console::WriteLine(int32) 

    ldloca    sw3
    ldc.i4    6
    stind.i4
m15:
    ldc.i4    8
    ldloc    sw3
    cgt
    brfalse    m14
	ldloc  sw3
	call void [mscorlib]System.Console::WriteLine(int32) 

    ldloca    sw3
    ldloc    sw3
    ldc.i4    1
    add
    stind.i4
    br    m15
m14:
    ldloca    sw1
    ldloc    sw1
    ldc.i4    1
    add
    stind.i4
    br    m13
m12:
    ldloca    a
    ldc.i4    2
    stind.i4
    ldloc    a
    ldc.i4    1
    ceq
    brfalse    m19
    ldloca    sw4
    ldc.i4    166
    stind.i4
    br    m20
m19:
m20:
    ldloc    a
    ldc.i4    2
    ceq
    brfalse    m21
    ldloca    sw4
    ldc.i4    266
    stind.i4
    br    m22
m21:
m22:
    ldloc    a
    ldc.i4    3
    ceq
    brfalse    m23
    ldloca    sw4
    ldc.i4    366
    stind.i4
    br    m24
m23:
m24:
    ldloca    exp1
    ldc.i4    2
    ldc.i4    3
    ldc.i4    2
    call float64 [mscorlib]System.Math::Pow(float64, float64)
    conv.r4

    call float64 [mscorlib]System.Math::Pow(float64, float64)
    conv.r4

    stind.r4
	ldloc  a
	call void [mscorlib]System.Console::WriteLine(int32) 

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
	call void [mscorlib]System.Console::WriteLine(float32) 
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
	call void [mscorlib]System.Console::WriteLine(float32) 
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