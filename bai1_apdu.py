# phan tich APDU

def lam_sach(s):
    s = s.upper().replace("0X", "")
    for c in " ,:-":
        s = s.replace(c, "")
    return bytes.fromhex(s)


def hex_str(b):
    return b.hex(" ").upper()


def doc_command(apdu):
    if len(apdu) < 4:
        raise ValueError("APDU phai co it nhat 4 byte")
    cla, ins, p1, p2 = apdu[0], apdu[1], apdu[2], apdu[3]
    body = apdu[4:]
    lc = None
    le = None
    data = b""

    if len(body) == 0:
        case = "1"
    elif len(body) == 1:
        case = "2"
        le = body[0] or 256
    elif body[0] != 0:
        # dang short
        lc = body[0]
        if len(body) == lc + 1:
            case = "3"
        elif len(body) == lc + 2:
            case = "4"
            le = body[-1] or 256
        else:
            raise ValueError("Lc khong khop voi du lieu")
        data = body[1:lc + 1]
    else:
        # dang extended
        if len(body) == 3:
            case = "2 (extended)"
            le = int.from_bytes(body[1:3], "big") or 65536
        elif len(body) > 3:
            lc = int.from_bytes(body[1:3], "big")
            if len(body) == lc + 3:
                case = "3 (extended)"
            elif len(body) == lc + 5:
                case = "4 (extended)"
                le = int.from_bytes(body[-2:], "big") or 65536
            else:
                raise ValueError("Lc khong khop voi du lieu")
            data = body[3:lc + 3]
        else:
            raise ValueError("APDU khong hop le")

    print(f"Case : {case}")
    print(f"CLA  : {cla:02X}")
    print(f"INS  : {ins:02X}")
    print(f"P1   : {p1:02X}")
    print(f"P2   : {p2:02X}")
    if lc is not None:
        print(f"Lc   : {lc} ({lc:02X})")
        print(f"Data : {hex_str(data)}")
    if le is not None:
        print(f"Le   : {le}")


def doc_response(resp):
    if len(resp) < 2:
        raise ValueError("Response phai co it nhat 2 byte")
    data = resp[:-2]
    if data:
        print(f"Data : {hex_str(data)} ({len(data)} byte)")
    else:
        print("Data : <rong>")
    print(f"SW1  : {resp[-2]:02X}")
    print(f"SW2  : {resp[-1]:02X}")


try:
    loai = input("1 - command, 2 - response: ").strip()
    chuoi = input("Nhap day HEX: ")
    data = lam_sach(chuoi)
    print()
    if loai == "2":
        doc_response(data)
    else:
        doc_command(data)
except ValueError as e:
    print("Loi:", e)
