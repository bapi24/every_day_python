
def open_file(filename):
    try:
        with open(filename) as f:
            content = f.read()
    except:
        print("file not found!!")
        hello()

def hello():
    print("Hello!!!")


open_file('testfile.txt')