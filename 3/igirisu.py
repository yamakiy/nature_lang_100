#!/usr/bin/python3.6
import json
import re
import requests
from pprint import pprint

class JawikiCountry(object):
    jawiki = ""

    # 強調マークアップの除去
    __rm_markup = lambda self, x: re.sub(r'(\'{2,5})(.*?)\1', r'\2', x, flags=re.DOTALL)
    # 内部リンクマークアップの除去
    __rm_inlink = lambda self, x: re.sub(r'\[\[(?!Category:|File:|ファイル:)(.*?)\]\]', r'\1', x, flags=re.DOTALL)
    # 外部リンクマークアップの除去
    __rm_outlink = lambda self, x: re.sub(r'\[(.*?)\]', r'\1', x, flags=re.DOTALL)
    # リダイレクトマークアップの除去
    __rm_redirect = lambda self, x: re.sub(r'#REDIRECT \[\[(.*?)\]\]', r'\1', x, flags=re.DOTALL)
    # コメントアウトの除去
    __rm_commentout = lambda self, x: re.sub(r'<!--(.*?)-->', r'\1', x, flags=re.DOTALL)
    # 署名の除去
    __rm_signature = lambda self, x: x.replace('~~~~', '')

    def __init__(self, country):
        self.jawiki = self.get_jawiki(country)

    def get_jawiki(self, country):
        jawiki_country = {}
        with open("jawiki-country.json", "r") as f:
            for i in f:
                data = json.loads(i)
                jawiki_country[data["title"]] = data["text"]
        return jawiki_country[country]

    def get_category_line(self):
        return re.findall(r'^\[\[Category.*', self.jawiki, re.MULTILINE)

    def get_category(self):
        return re.findall(r'^\[\[Category:(.*?)(?:\|.*)?\]\]', self.jawiki, re.MULTILINE)

    def get_level(self):
        level = re.findall(r'^(==+)(.*?)==+', self.jawiki, re.MULTILINE)
        level = [[i[1], len(i[0])-1] for i in level]
        return level

    def get_mediafile(self):
        return re.findall(r'(?:File|ファイル):(.*?)\|', self.jawiki, re.DOTALL)

    def get_basic_info(self):
        basic_info = re.findall(r'^\{\{基礎情報.*?$\n(.*)^\}\}$', self.jawiki, re.MULTILINE + re.DOTALL)[0]
        basic_info = re.findall(r'^\|(.+?)\s*=\s*(.+?)(?=\n\|)', basic_info, re.MULTILINE + re.DOTALL)
        return basic_info

    # 強調マークアップの削除
    def get_basic_info_no_markup(self):
        basic_info = self.get_basic_info()
        return {i[0]: self.__rm_markup(i[1]) for i in basic_info}


    def get_basic_info_no_markup_no_inlink(self):
        basic_info = self.get_basic_info()
        res = {}
        for line in basic_info:
            val = self.__rm_markup(line[1])
            val = self.__rm_inlink(val)
            res[line[0]] = val
        return res

    # 可能な限りマークアップを除去
    def get_basic_info_no_markup_all(self):
        basic_info = self.get_basic_info()
        res = {}
        for line in basic_info:
            val = self.__rm_markup(line[1])
            val = self.__rm_inlink(val)
            val = self.__rm_outlink(val)
            val = self.__rm_redirect(val)
            val = self.__rm_commentout(val)
            val = self.__rm_signature(val)
            res[line[0]] = val
        return res

    def get_national_flag_url(self):
        national_flag = self.get_basic_info_no_markup_all()["国旗画像"]
        endpoint = "https://www.mediawiki.org/w/api.php"
        params = {
            'action': 'query',
            'titles': f'File: {national_flag}',
            'format': 'json',
            'iiprop': 'url',
            'prop': 'imageinfo'
        }
        res = requests.get(endpoint, params=params)
        if res.status_code == 200:
            data = json.loads(res.text)
            return data["query"]["pages"]["-1"]["imageinfo"][0]["url"]

        return ""

if __name__ == "__main__":
    jc = JawikiCountry("イギリス")
    pprint(jc.get_national_flag_url())
