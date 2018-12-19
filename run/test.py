from makewordcloud import makeWordCloud
from asin2Masin import Asin2asin

if __name__ == '__main__':
    asin = 'B0755BYDD9'
    asin2asin = Asin2asin(asin)
    masin = asin2asin.getMasin()
    make = makeWordCloud()
    make.addStopWords('dress', 'beautiful')
    make.randomGetText(asin)
    make.getcloud(asin)
