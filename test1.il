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
       [1]  int32 v,
       [2]  float32 b,
       [3]  int32 c,
       [4]  int32 k,
       [5]  float32 s,
       [6]  int32 u,
       [7]  int32 w,
       [8]  int32 inp1,
       [9]  float32 inp2,
       [10]  int32 i1,
       [11]  int32 i2,
       [12]  int32 i3,
       [13]  int32 sw1,
       [14]  int32 sw2,
       [15]  int32 sw3,
       [16]  int32 sw4,
       [17]  int32 a,
       [18]  float32 exp1,
       [19]  float32 exp2,
       [20]  float32 exp3
     )
       [21]  float32 d
     )

   .entrypoint
   //.maxstack  8
    ldloca    b
    ldc.i4    7
    ldc.i4    2
    sub
    ldc.i4    1
    add
    stind.i4
    ldloca    s
    ldc.r4    0.50
    stind.i4
    ldloca    u
    ldc.i4    0
    stind.i4
    ldloca    w
    ldc.i4    0
    stind.i4
    ldloca    sw1
    stind.i4
    ldloca    sw4
    ldc.i4    0
    stind.i4
    ldloc    s
    ldc.r4    4.50
    brfalse    m1
    ldloca    s
    ldloc    s
    ldc.i4    5
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
m2:
    ldloc    w
    ldc.i4    5
    brfalse    m1
    ldloca    w
    ldloc    w
    ldc.i4    1
    add
    stind.i4
    br    m2
m1:
m2:
    ldloc    u
    ldc.i4    10
    brfalse    m1
    br    m3
m1:
    ldloca    u
    ldloc    u
    ldc.i4    2
    add
    stind.i4
    br    m2
m3:
    ldloca    sw1
    stind.i4
m2:
    ldloc    sw1
    clt
    brfalse    m1
    ldloca    sw4
    ldloc    sw4
    ldc.i4    1
    add
    stind.i4
    ldloca    sw1
    ldloc    sw1
    ldc.i4    1
    add
    stind.i4
    br    m2
m1:
	ret    
}
}