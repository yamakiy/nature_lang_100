#!/usr/bin/python3.6
import re
from pprint import pprint

class Morph(object):
    surface = ""
    base = ""
    pos = ""
    pos1 = ""

    def __init__(self, line):
        self.__set_vals(line)

    def __str__(self):
        return f"{self.surface}\t{self.base}\t{self.pos}\t{self.pos1}"

    def __set_vals(self, line):
        vals = re.split(r"\t|,", line)

        self.surface = vals[0]
        self.base = vals[7]
        self.pos = vals[1]
        self.pos1 = vals[2]

class Chunk(object):
    morphs = []
    srcs = []
    dst = -1

    def __init__(self, **kwargs):
        self.morphs = kwargs["morphs"] if "morphs" in kwargs else []
        self.dst = kwargs["dst"] if "dst" in kwargs else ""
        self.srcs = kwargs["srcs"] if "srcs" in kwargs else []

    def __str__(self):
        ret_str = f"srcs:{self.srcs}\tdst:{self.dst}\n"
        for morph in self.morphs:
            ret_str += f"{morph.surface}\t{morph.base}\t{morph.pos}\t{morph.pos1}\n"
        return ret_str

class NekoCabocha(object):

    def phrase_morphs(self):
        with open("./files/neko.txt.cabocha", "r") as f:
            morphs = []
            for line in f:
                if line == "EOS\n": # 終了文字判定
                    yield morphs
                    morphs = []
                elif line[0] != "*": # * は解析開始文字
                    morphs.append(Morph(line))

    def phrase_chunks(self):
        with open("./files/neko.txt.cabocha", "r") as f:
            chunks = {}
            for line in f:
                if line == "EOS\n": # 終了文字判定
                    yield chunks
                    chunks = {}
                elif line[0] == "*": # * は解析開始文字
                    cols = line.split(' ')
                    idx = int(cols[1])
                    dst = int(re.search(r'(.*?)D', cols[2]).group(1))
                    chunks[idx] = chunks[idx] if idx in chunks else Chunk()
                    chunks[idx].dst = dst
                    if dst != -1:
                        if dst not in chunks:
                            chunks[dst] = Chunk()
                        chunks[dst].srcs.append(idx)
                else:
                    chunks[idx].morphs.append(Morph(line))

# 42. 係り元と係り先の文節の表示
def print_42():
    nc = NekoCabocha()
    for i, chunks in enumerate(nc.phrase_chunks()):
        for k in chunks:
            dst_idx = chunks[k].dst
            if dst_idx != -1:
                src = "".join([i.surface for i in chunks[k].morphs if i.pos != "記号"])
                dst = "".join([i.surface for i in chunks[dst_idx].morphs if i.pos != "記号"])
                print(f"{src}\t{dst}")

# 43. 名詞を含む文節が動詞を含む文節に係るものを抽出
def print_43():
    nc = NekoCabocha()
    for i, chunks in enumerate(nc.phrase_chunks()):
        for k in chunks:
            dst_idx = chunks[k].dst
            if dst_idx != -1:
                if "名詞" in [i.pos for i in chunks[k].morphs] and "動詞" in [i.pos for i in chunks[dst_idx].morphs]:
                    src = "".join([i.surface for i in chunks[k].morphs if i.pos != "記号"])
                    dst = "".join([i.surface for i in chunks[dst_idx].morphs if i.pos != "記号"])
                    print(f"{src}\t{dst}")

if __name__ == "__main__":
    print_43()
