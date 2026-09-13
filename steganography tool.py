from PIL import Image

def ttb(txt):
    bts = []
    for b in txt.encode('utf-8'):
        bts.extend([int(x) for x in bin(b)[2:].zfill(8)])
    return bts

def btt(bts):
    bytlst = []
    for i in range(0, len(bts), 8):
        byt = bts[i:i+8]
        bytlst.append(int("".join(str(x) for x in byt), 2))
    return bytes(bytlst).decode('utf-8', errors='replace')

def encimg(inpath, outpath, secmsg):
    img = Image.open(inpath).convert("RGB")
    rawdat = bytearray(img.tobytes())
    msgbts = ttb(secmsg)
    numbts = len(msgbts)
    lenbts = [int(b) for b in bin(numbts)[2:].zfill(32)]
    payload = lenbts + msgbts
    totpix = len(rawdat) // 3
   
    if len(payload) > totpix:
        raise ValueError("Message to big for the image")
    
    for i, bit in enumerate(payload):
        byteidx = i * 3
        rawdat[byteidx] = (rawdat[byteidx] & ~1) | bit

    encimg = Image.frombytes(img.mode, img.size, bytes(rawdat))
    encimg.save(outpath, "PNG")
    print(f"Message hidden in: {outpath}")

def decimg(imgpath):
    img = Image.open(imgpath).convert("RGB")
    rawdat = img.tobytes()
    totpix = len(rawdat) // 3
    lenbts = [rawdat[i * 3] & 1 for i in range(32)]
    msgbitcnt = int("".join(str(b) for b in lenbts), 2)  

    if msgbitcnt <= 0 or (32 + msgbitcnt) > totpix:
        print("No valid hidden message detected.")
        return None

    msgbts = [rawdat[i * 3] & 1 for i in range(32, 32 + msgbitcnt)]  
    sec = btt(msgbts)
    print(f" Extracted Message: {sec}")
    return sec


if __name__ == "__main__":
    print("===Steganography Tool===")
    choice = input("Do you want to (E)ncode or (D)ecode? ").strip().upper()

    if choice == "E":
        src = input("Source image path: ").strip()
        out = input("Output image name (e.g. output.png): ").strip()
        msg = input("Secret message: ").strip()
        encimg(src, out, msg)
    elif choice == "D":
        src = input("Image to decode: ").strip()
        decimg(src)
    else:
        print("Invalid choice. Enter E or D.")
