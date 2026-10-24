# doc TAG - LENGTH - VALUE (TLV), co long nhau

def doc_tlv(data, cap=0):
    i = 0
    while i < len(data):
        # bo qua byte padding
        if data[i] == 0x00 or data[i] == 0xFF:
            i += 1
            continue

        # doc tag (tag nhieu byte)
        dau = data[i]
        tag = [dau]
        i += 1
        if dau & 0x1F == 0x1F:
            while True:
                if i >= len(data):
                    raise ValueError("Tag khong day du")
                b = data[i]
                tag.append(b)
                i += 1
                if b & 0x80 == 0:
                    break

        # doc length
        if i >= len(data):
            raise ValueError("Thieu Length")
        length = data[i]
        i += 1
        if length & 0x80:
            n = length & 0x7F
            if n == 0 or i + n > len(data):
                raise ValueError("Length khong hop le")
            length = int.from_bytes(data[i:i + n], "big")
            i += n

        # doc value
        if i + length > len(data):
            raise ValueError("Value khong du so byte")
        value = data[i:i + length]
        i += length

        lui = "  " * cap
        tag_hex = bytes(tag).hex().upper()
        if dau & 0x20:
            print(f"{lui}{tag_hex} | {length} | (constructed)")
            doc_tlv(value, cap + 1)
        else:
            print(f"{lui}{tag_hex} | {length} | {value.hex(' ').upper()}")


try:
    chuoi = input("Nhap day HEX: ").upper().replace("0X", "")
    for c in " ,:-":
        chuoi = chuoi.replace(c, "")
    print("\nTAG | LENGTH | VALUE")
    doc_tlv(bytes.fromhex(chuoi))
except ValueError as e:
    print("Loi:", e)
