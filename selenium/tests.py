from b1 import main as b1_main
from b2 import main as b2_main
from b3 import main as b3_main
from k1 import main as k1_main
from z1 import main as z1_main

def main():
    port = "8503"
    try:
        b1_main(port)
        b2_main(port)
        b3_main(port)
        k1_main(port)
        z1_main(port)
    except Exception as e:
        print(e)
        exit(1)
    print("All tests passed!")

if __name__ == "__main__":
    main()