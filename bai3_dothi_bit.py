import matplotlib.pyplot as plt

chuoi = input("Nhap day bit: ").strip()
if chuoi.lower().startswith("0x"):
    so = chuoi[2:].replace(" ", "")
    bit = [int(c) for c in "".join(format(b, "08b") for b in bytes.fromhex(so))]
else:
    bit = [int(c) for c in chuoi if c in "01"]

if len(bit) == 0:
    print("Khong co bit nao")
else:
    n = len(bit)
    plt.step(range(n + 1), bit + bit[-1:], where="post", lw=2)
    for i, b in enumerate(bit):
        plt.text(i + .5, 1.1, b, ha="center")
    plt.xlim(0, n), plt.ylim(-0.3, 1.4)
    plt.title("do thi bit"), plt.xlabel("bit"), plt.ylabel("muc logic")
    plt.xticks(range(n + 1)); plt.yticks([0, 1]); plt.grid(ls=":")
    plt.show()
#-m pip install matplotlib