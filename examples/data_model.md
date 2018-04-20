
## Data model
Python中，所有的东西都是对象，每个对象都有一个唯一识别的id，Python语言中有很多魔法函数，正式这些魔法函数，使得对象更加的Pythonic。

术语：
* magic: 魔法函数
* dunder: double under，也就是“__”

下面以《Fluent Python》中的两段代码来展示一下吧：

### __len__, __getitem__


```python
import collections

Card= collections.namedtuple('Card', ['rank', 'suit'])

class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()
    
    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]
    
    def __len__(self):
        return len(self._cards)
    
    def __getitem__(self, position):
        return self._cards[position]
```


```python
beer_card = Card('7', 'diamonds')
```


```python
beer_card
```




    Card(rank='7', suit='diamonds')




```python
deck = FrenchDeck()
```


```python
# Magic __len__ works 
len(deck)
```




    52




```python
# Magic __getitem__ works
deck[0]
```




    Card(rank='2', suit='spades')




```python
deck[-1]
```




    Card(rank='A', suit='hearts')




```python
from random import choice
```


```python
# Random item
choice(deck)
```




    Card(rank='Q', suit='diamonds')




```python
# Slice
deck[:3]
```




    [Card(rank='2', suit='spades'),
     Card(rank='3', suit='spades'),
     Card(rank='4', suit='spades')]




```python
deck[12::13]
```




    [Card(rank='A', suit='spades'),
     Card(rank='A', suit='diamonds'),
     Card(rank='A', suit='clubs'),
     Card(rank='A', suit='hearts')]




```python
# if __contain__ not exist, it will go through the sequence
Card('Q', 'hearts') in deck
```




    True




```python
Card('Q', 'beasts') in deck
```




    False




```python
# Sort
suit_values = dict(spades=3, hearts=2, diamonds=1, clubs=0)

def spades_high(card):
    rank_value = FrenchDeck.ranks.index(card.rank)
    return rank_value * len(suit_values) + suit_values[card.suit]

for card in sorted(deck, key=spades_high):
    print(card)
```

    Card(rank='2', suit='clubs')
    Card(rank='2', suit='diamonds')
    Card(rank='2', suit='hearts')
    Card(rank='2', suit='spades')
    Card(rank='3', suit='clubs')
    Card(rank='3', suit='diamonds')
    Card(rank='3', suit='hearts')
    Card(rank='3', suit='spades')
    Card(rank='4', suit='clubs')
    Card(rank='4', suit='diamonds')
    Card(rank='4', suit='hearts')
    Card(rank='4', suit='spades')
    Card(rank='5', suit='clubs')
    Card(rank='5', suit='diamonds')
    Card(rank='5', suit='hearts')
    Card(rank='5', suit='spades')
    Card(rank='6', suit='clubs')
    Card(rank='6', suit='diamonds')
    Card(rank='6', suit='hearts')
    Card(rank='6', suit='spades')
    Card(rank='7', suit='clubs')
    Card(rank='7', suit='diamonds')
    Card(rank='7', suit='hearts')
    Card(rank='7', suit='spades')
    Card(rank='8', suit='clubs')
    Card(rank='8', suit='diamonds')
    Card(rank='8', suit='hearts')
    Card(rank='8', suit='spades')
    Card(rank='9', suit='clubs')
    Card(rank='9', suit='diamonds')
    Card(rank='9', suit='hearts')
    Card(rank='9', suit='spades')
    Card(rank='10', suit='clubs')
    Card(rank='10', suit='diamonds')
    Card(rank='10', suit='hearts')
    Card(rank='10', suit='spades')
    Card(rank='J', suit='clubs')
    Card(rank='J', suit='diamonds')
    Card(rank='J', suit='hearts')
    Card(rank='J', suit='spades')
    Card(rank='Q', suit='clubs')
    Card(rank='Q', suit='diamonds')
    Card(rank='Q', suit='hearts')
    Card(rank='Q', suit='spades')
    Card(rank='K', suit='clubs')
    Card(rank='K', suit='diamonds')
    Card(rank='K', suit='hearts')
    Card(rank='K', suit='spades')
    Card(rank='A', suit='clubs')
    Card(rank='A', suit='diamonds')
    Card(rank='A', suit='hearts')
    Card(rank='A', suit='spades')


### __abs__, __add__ and __mul__


```python
from math import hypot

class Vector:
    
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        
    def __repr__(self):
        return 'Vector(%r, %r)' % (self.x, self.y)
    
    def __abs__(self):
        return hypot(self.x, self.y)

    def __bool__(self):
        return bool(self.x, self.y)
    
    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x, y)
        
    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)
```


```python
v1 = Vector(2, 4)
v2 = Vector(2, 1)
v1 + v2
```




    Vector(4, 5)




```python
v = Vector(3, 4)
```


```python
abs(v)
```




    5.0




```python
v * 3
```




    Vector(9, 12)




```python
abs(v * 3)
```




    15.0


