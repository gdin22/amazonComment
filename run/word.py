from collections import defaultdict


# 词频的编写
# stopwords 是屏蔽词 可以添加
# stopwordlist 把屏蔽词文本转换为list
# differentiate 把内容区分成词频 以字典的格式返回
class WordFre(object):
    def __init__(self, text):
        self.text = text.split(' ')

    def stopwordlist(self):
        stopwordlist = []
        with open('stopwords') as f:
            for word in f.readlines():
                stopwordlist.append(word.strip())
        return stopwordlist

    def differentiate(self):
        stopwordlist = self.stopwordlist()
        wordDict = defaultdict(int)
        for word in self.text:
            if word.lower() not in stopwordlist:
                wordDict[word] += 1
        wordDict = dict(wordDict)
        return wordDict
