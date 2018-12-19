from makewordcloud import makeWordCloud
from asin2Masin import Asin2asin
from word import WordFre
import sys

if __name__ == '__main__':
    if sys.argv[1] == 'cloud':
        asin = 'B0755BYDD9'
        asin2asin = Asin2asin(asin)
        masin = asin2asin.getMasin()
        make = makeWordCloud()
        make.addStopWords('dress', 'beautiful')
        make.getcloud(asin)
    else:
        asin = 'B0755BYDD9'
        asin2asin = Asin2asin(asin)
        masin = asin2asin.getMasin()
        make = makeWordCloud()
        text, searchState = make.randomGetText(asin)
        print(text)
        wordfre = WordFre(text)
        dict = wordfre.differentiate()
        print(dict)
