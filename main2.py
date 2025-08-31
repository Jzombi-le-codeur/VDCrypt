import struct, os
vd = r"F:\vdisk.vdcr"   # adapte si besoin

with open(vd, "rb") as f:
    data = f.read()

print("file_size =", len(data))
if len(data) < 14:
    print("fichier trop petit")
else:
    header = data[:14]
    fmt, vsize = struct.unpack(">6sQ", header)
    fmt = fmt.split(b"\x00")[0].decode("utf-8")
    table_offset = 14 + vsize
    print("format:", repr(fmt))
    print("virtual_files_size (header):", vsize)
    print("table_offset (14 + vsize):", table_offset)

    # afficher 20 bytes avant et 100 après la frontière
    start_slice = max(0, table_offset - 20)
    end_slice = min(len(data), table_offset + 200)
    context = data[start_slice:end_slice]
    print("\ncontext bytes (hex):", context.hex())
    print("\ncontext repr (ascii-ish):")
    print(repr(context))

    # Chercher premier caractère JSON dans la zone après le header
    after14 = data[14:]
    idx_bracket = after14.find(b'[')
    idx_brace = after14.find(b'{')
    print("\nfirst '[' after header at:", idx_bracket if idx_bracket>=0 else None)
    print("first '{' after header at:", idx_brace if idx_brace>=0 else None)