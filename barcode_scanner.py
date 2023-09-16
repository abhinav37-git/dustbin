import usb

from usb.core import NoBackendError, USBError

byte_char_mapper = [
    [
        "",
        "",
        "",
        "",
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "0",
        "",
        "",
        "",
        "",
    ],
    [],
    [
        "",
        "",
        "",
        "",
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "L",
        "M",
        "N",
        "O",
        "P",
        "Q",
        "R",
        "S",
        "T",
        "U",
        "V",
        "W",
        "X",
        "Y",
        "Z",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
    ],
]


def byte_char_map(x, y):
    try:
        return byte_char_mapper[x][y]
    except:
        return ""


def read_scan(queue, vid, pid):
    while True:
        try:
            dev = usb.core.find(
                idVendor=int("0x" + vid, 16),
                idProduct=int("0x" + pid, 16),
            )
            dev.set_configuration()
            conf = dev.get_active_configuration()
            cfg = conf[(0, 0)]
            ep = cfg[0]
            r = []

            while True:
                code = ""
                try:
                    data = dev.read(ep.bEndpointAddress, ep.wMaxPacketSize)
                    r.append([data[0], data[2]])
                    if data[2] == 43:
                        for x in r:
                            code += str(byte_char_map(x[0], x[1]))
                        queue.put(code)
                        r = []
                except USBError as e:
                    val = str(e).split("[")[2].split("]")[0]
                    if val in ["claim_interface", "submit_async"]:
                        break
                    else:
                        queue.put("")
        except NoBackendError:
            queue.put("")
        except AttributeError:
            queue.put("")


def get_scan(queue):
    while True:
        data = queue.get()
        if data != "":
            print(data)
        else:
            print("Scanner not connected")
