#!/usr/bin/python3.6
import CaboCha

if __name__ == "__main__":
    c = CaboCha.Parser()
    with open("./files/neko.txt", "r") as f:
        with open("./files/neko.txt.cabocha", "w") as f2:
            for line in f:
                f2.write(c.parse(line).toString(CaboCha.FORMAT_LATTICE))
