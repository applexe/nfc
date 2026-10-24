

pin_dung = "1234"
so_lan_max = 3

the = {"con": so_lan_max, "khoa": False, "xac_thuc": False}


def hex_str(b):
    return b.hex(" ").upper()


def lam_sach(s):
    s = s.upper().replace("0X", "")
    for c in " ,:-":
        s = s.replace(c, "")
    return bytes.fromhex(s)


def pin_ascii(pin):
    return bytes([0x00, 0x20, 0x00, 0x80, len(pin)]) + pin.encode("ascii")


def pin_block(pin):
    s = "2" + format(len(pin), "X") + pin
    return bytes.fromhex(s.ljust(16, "F"))


def doc_pin(data):
    # doc pin tu data cua lenh, la pin block hoac ascii
    if len(data) == 8 and data[0] >> 4 == 2:
        n = data[0] & 0x0F
        return data.hex().upper()[2:2 + n]
    s = data.decode("ascii", errors="ignore")
    if s.isdigit():
        return s
    return None


def xu_ly(apdu):
    if len(apdu) < 5:
        return 0x67, 0x00
    lc = apdu[4]
    if len(apdu) != 5 + lc:
        return 0x67, 0x00
    if apdu[1] != 0x20:
        return 0x6D, 0x00
    if the["khoa"]:
        return 0x69, 0x83
    if apdu[2] != 0x00 or apdu[3] not in (0x80, 0x01):
        return 0x6A, 0x86
    if lc != len(pin_dung) and lc != 8:
        return 0x67, 0x00

    data = apdu[5:]
    print("PIN trong lenh:", doc_pin(data))
    if data == pin_dung.encode("ascii") or data == pin_block(pin_dung):
        the["xac_thuc"] = True
        the["con"] = so_lan_max
        return 0x90, 0x00

    the["xac_thuc"] = False
    the["con"] -= 1
    if the["con"] <= 0:
        the["con"] = 0
        the["khoa"] = True
        return 0x69, 0x83
    return 0x63, 0xC0 | the["con"]


while not the["khoa"] and not the["xac_thuc"]:
    chuoi = input("Nhap PIN hoac APDU hex: ").strip()

    if chuoi.isdigit() and len(chuoi) <= 12:
        if len(chuoi) < 4:
            print("PIN phai co it nhat 4 chu so")
            continue
        apdu = pin_ascii(chuoi)
        print("APDU (ascii) :", hex_str(apdu))
        print("PIN block    :", hex_str(pin_block(chuoi)))
    else:
        try:
            apdu = lam_sach(chuoi)
        except ValueError:
            print("Loi: day hex khong hop le")
            continue

    sw1, sw2 = xu_ly(apdu)
    print(f"SW           : {sw1:02X} {sw2:02X}")
    print("con lai      :", the["con"], "| khoa:", the["khoa"], "| xac thuc:", the["xac_thuc"])
    print()
