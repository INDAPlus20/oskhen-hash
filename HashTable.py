#!/usr/bin/env python3

from math import sqrt, ceil
from itertools import count
from collections import namedtuple
import copy

DEFAULT_SIZE = 100

def is_prime(n):
    if n == 2:
        return True
    if n % 2 == 0 or n == 1:
        return False
    for i in range(3, int(sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

def next_prime(n):
    return next(filter(is_prime, count(n)))

def nth(iterator, n): # Yields nth element from iterator 
    return next((x for i,x in enumerate(iterator) if i==n), None) # https://stackoverflow.com/questions/2300756/get-the-nth-item-of-a-generator-in-python

class Entry(namedtuple('Entry', ['key', 'value'])): # Akin to rust/c++ structs
    def __repr__(self):
        return f"{self.key}:{self.value}"

class HashTable:

    def __init__(self, size=DEFAULT_SIZE):
        self.size = next_prime(size) # # We want tablesize and hash constant k to be coprime (to avoid regular collisions), all k's are coprime with primenumbers.
        self.hashTable = self.createTable()
        self.initMAD()
        self.usedsize = 0

    def createTable(self): # Buckets can contain ONE item.
        return [None] * self.size

    def hash(self, key): # String-only

        ## Hashcode (str -> int) conversion to integer - Polynomial hashcode

        a = 41 ## 42 but prime 

        k = len(key) + 1

        h = 0
        for c in key:
            h += ord(c)*a**k
            k-=1
        
        ## Compression (int -> hash) size adjustment for table - MAD compression
        # ay+b mod p mod N, constants generated at table creation/resize
        # h = y, self.size = N
        
        self.madA * h 

        return ((self.madA * h + self.madB) % self.madP) % self.size

    def initMAD(self):
        self.madP = nth(filter(is_prime, count(self.size)), 42) # 42nd prime after tablesize, constraint: P > self.size
        self.madA = self.madP - (self.madP // 3) - 26 # Constraint: A in range [1, p-1]
        self.madB = self.madP - ceil(self.madP * 0.1337) # Constraint: B in range [0, p-1]
    
    def findPos(self, key): ## Quadratic probing - https://stackoverflow.com/questions/22437416/best-way-to-resize-a-hash-table

        currentPos = self.hash(key)
        collisionNum = 0

        while self.hashTable[currentPos] != None and self.hashTable[currentPos].key != key:
            collisionNum += 1
            currentPos += 2 * (collisionNum) - 1
            currentPos % self.size
        
        return currentPos

    def upsizeTable(self): ## Doubles size to nearest prime, rehashes
        
        self.size = next_prime(self.size*2)
        oldTable = copy.deepcopy(self.hashTable) ## Rework this, deepcopy extremely memory-inefficient!
        self.hashTable = self.createTable()

        for entry in oldTable:
            if entry:
                self.insert(entry.key, entry.value)
        
        self.initMAD()
        

    def insert(self, key, value):

        entry = Entry(key, value)
        pos = self.findPos(key)

        if not self.hashTable[pos]:
            self.usedsize += 1

        self.hashTable[pos] = entry

        if self.usedsize > self.size // 2:
            self.upsizeTable()
    
    def lookup(self, key):
        pos = self.findPos(key)
        entry = self.hashTable[pos]
        if entry:
            return entry.value
        return None

    def listAll(self):
        return [entry for entry in self.hashTable if entry != None]

    def delete(self, key):

        pos = self.findPos(key)
        
        if self.hashTable[pos]:
            self.usedsize -= 1

        if self.hashTable[pos]:
            self.hashTable[pos] = None
            return True
        else:
            return False



if __name__ == "__main__":
    table = HashTable()

    table.insert("a", "hello")
    table.insert("b", "world")

    for i in range(65, 100):
        table.insert(chr(i), "asdf")
    

    print(table.lookup("a"))
    print(table.listAll())

    table.delete("a")

    print(table.lookup("a"))
    print(table.listAll())

