from collections import Counter, OrderedDict
from typing import Union

def normalizeCounter(counter: Counter) -> Counter:

    propCounts = counter.copy()
    totalCounts = sum(counter.values())
    
    for key in counter:
        propCounts[key] /= totalCounts
        
    return propCounts

def prettyNumber(number: Union[int, str]) -> str:
    
    if type(number) != 'str':
        number = str(number)
    
    reversedNumber                 = reversed(number)
    insertSpaceAfter3CharsReversed = [char if i % 3 != 0 or i == 0 else f'{char} ' for i, char in enumerate(reversedNumber)]
    insertSpaceAfter3Chars         = list(reversed(insertSpaceAfter3CharsReversed))
    
    return ''.join(insertSpaceAfter3Chars)

def uniqueList(lst: list) -> list:
    return list(OrderedDict.fromkeys(lst))