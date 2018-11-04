#!/usr/bin/python3.6
import collections
import os
import re
import pickle
from pprint import pprint
from matplotlib import pyplot
from matplotlib.font_manager import FontProperties

class NekoMecab(object):
    model = []

    def __init__(self):
       self.load_model()

    # 形態素解析結果の読み込みを行う。 無ければ作成
    def load_model(self):
        if os.path.exists("./files/neko.model.pickle"):
            with open("./files/neko.model.pickle", "rb") as f:
                self.model = pickle.load(f)
        else:
            self.save_model()

    # 形態素解析結果の作成
    def save_model(self):
        with open("./files/neko.txt.mecab", "r") as f:
            for line in f:
                # 終了文字EOSが現れたら終了
                if line == "EOS\n":
                    break
                vals = re.split(r"\t|,", line)
                self.model.append({
                    "surface": vals[0], "base": vals[7], "pos": vals[1], "pos1": vals[2]
                })
        with open("./files/neko.model.pickle", "wb") as f:
            pickle.dump(self.model, f)

    def filter(self, **kwargs):
        for key in kwargs:
            self.model = [i for i in self.model if kwargs[key] == i[key]]
        return self

    def get_arg(self, key):
        return [i[key] for i in self.model]

    # 2つの名詞が「の」で連結されている名詞句を取得
    def get_A_no_B(self):
        res = []
        for i in range(1, len(self.model) - 1):
            if self.model[i-1]["pos"] == self.model[i+1]["pos"] == "名詞" and self.model[i]["surface"] == "の":
                res.append(self.model[i-1]["surface"] + self.model[i]["surface"] + self.model[i+1]["surface"])
        return res

    # 連続した名詞句を取得
    def get_continuous_nouns(self):
        res = []
        nonus = []
        for line in self.model:
            if line["pos"] == "名詞":
                nonus.append(line["surface"])
            elif len(nonus) > 1:
                res.append("".join(nonus))
                nonus = []
        # 最後の連続した名詞が上記のforから漏れるからここで処理
        if len(nonus) > 1:
            res.append("".join(nonus))
        return res

    def get_word_frequency(self):
        res = []
        surfaces = self.get_arg("surface")
        return collections.Counter(surfaces)

    def output_frequency_rank_img(self, rank_num):
        word_frequency = self.get_word_frequency()
        top = word_frequency.most_common(rank_num)
        height = [i[1] for i in top]
        xtick = [i[0] for i in top]

        fp = FontProperties(fname='./IPAMTTC00303/ipam.ttc', size=14)
        pyplot.bar(range(rank_num), height)
        pyplot.xticks(range(rank_num), xtick, fontproperties=fp)
        pyplot.title("頻度上位10語", fontproperties=fp)
        pyplot.xlabel("単語", fontproperties=fp)
        pyplot.ylabel("出現回数", fontproperties=fp)
        pyplot.savefig(f"./files/img/frequency_rank_top{rank_num}.png")

    def output_frequency_histogram_img(self):
        word_frequency = self.get_word_frequency()
        top = word_frequency.most_common()
        datas = [i[1] for i in top]

        fp = FontProperties(fname='./IPAMTTC00303/ipam.ttc', size=14)
        # 出現頻度の差が大きいため、上限30で表示を打ち切る
        pyplot.hist(datas, bins=30, range=(1, 30))
        pyplot.title("単語の出現頻度ヒストグラム", fontproperties=fp)
        pyplot.xlabel("出現頻度", fontproperties=fp)
        pyplot.ylabel("単語の種類", fontproperties=fp)
        pyplot.savefig(f"./files/img/frequency_hist.png")

    def output_frequency_zipf_img(self):
        word_frequency = self.get_word_frequency()
        top = word_frequency.most_common()
        datas = [i[1] for i in top]

        fp = FontProperties(fname='./IPAMTTC00303/ipam.ttc', size=14)
        pyplot.scatter(range(len(datas)), datas)
        pyplot.xlim(1, len(datas) + 1)
        pyplot.title("zipf", fontproperties=fp)
        pyplot.xlabel("単語の出現頻度順", fontproperties=fp)
        pyplot.ylabel("出現頻度", fontproperties=fp)
        pyplot.xscale("log")
        pyplot.yscale("log")
        pyplot.savefig(f"./files/img/frequency_zipf.png")

if __name__ == "__main__":
    nm = NekoMecab()
    nm.output_frequency_zipf_img()
