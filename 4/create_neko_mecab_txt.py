#!/usr/bin/python3.6
import MeCab

if __name__ == "__main__":
    m = MeCab.Tagger()
    with open("./files/neko.txt", "r") as f:
        with open("./files/neko.txt.mecab", "w") as f2:
            f2.write(m.parse(f.read()))
