def append_to_file(path, text):
    f = open(path, "a")
    f.write(text)
    f.close()


def read_file(path):
    try:
        f = open(path, "r")
        text = f.read()
        f.close()
        return text

    except Exception as e:
        f = open(path, "w+")
        f.close()
        return ""


def write_to_file(path, text):
    f = open(path, "w")
    f.write(text)
    f.close()
