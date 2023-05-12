#!/usr/bin/env python3

zipClasses = """class Zip{n}Sequence<{tparams}>({args}) extends Sequence<({tparams})> {{
  fun values(): mutable Iterator<({tparams})> {{
{values}
    loop {{
      ({nexts}) match {{
      | ({somes}) -> yield ({vals})
      | _ -> break void
      }}
    }}
  }}
  fun size(): Int {{
    Vector[{sizes}].min().fromSome()
  }}
}}"""

zipExtensions = """  static fun zip{n}<{tparams}>(
{sequences}
  ): Sequence<({tparams})> {{
    Zip{n}Sequence({ss})
  }}"""

TUPLE_MIN = 2
TUPLE_MAX = 10

def getZipClass(n):
    tparams = ", ".join(f"T{x}" for x in range(n))
    args = ", ".join(f"s{x}: Sequence<T{x}>" for x in range(n))
    values = "\n".join(f"    it{x} = this.s{x}.values();" for x in range(n))
    nexts = ", ".join(f"it{x}.next()" for x in range(n))
    somes = ", ".join(f"Some(val{x})" for x in range(n))
    vals = ", ".join(f"val{x}" for x in range(n))
    sizes = ", ".join(f"this.s{x}.size()" for x in range(n))
    return zipClasses.format(
        n=n,
        tparams=tparams,
        args=args,
        values=values,
        nexts=nexts,
        somes=somes,
        vals=vals,
        sizes=sizes,
    )


def getZipExtension(n):
    tparams = ", ".join(f"T{x}" for x in range(n))
    sequences = "\n".join(f"    s{x}: Sequence<T{x}>," for x in range(n))
    ss = ", ".join(f"s{x}" for x in range(n))
    return zipExtensions.format(
        n=n, tparams=tparams, sequences=sequences, ss=ss
    )


def main():
    print("// @generated")
    print("// Use tools/generate_sequence_zip.py to regenerate")
    print("module Sequence;")
    print()
    for n in range(TUPLE_MIN, TUPLE_MAX + 1):
        print((getZipClass(n)))
        print()
    print("extension mutable base class .Sequence {")
    for n in range(TUPLE_MIN, TUPLE_MAX + 1):
        print((getZipExtension(n)))
    print("}")
    print()
    print("module end;")


if __name__ == '__main__':
    main()
