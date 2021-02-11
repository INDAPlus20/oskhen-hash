#!/usr/bin/env python3

import HashTable
import os


def mainMenu():
    choice = ""

    while True:
        print("Available commands:")
        print("1. Create Database")
        print("2. Delete Database")
        print("3. Access Database")
        print("4. Exit")

        choice = input()

        if choice == "1":
            createDB()
        elif choice == "2":
            deleteDB()
        elif choice == "3":
            accessDB()
        elif choice == "4":
            exit()
    
def createDB():
    while True:
        filename = input("Input database name/path or Quit to quit: ")

        if filename.lower() == "quit":
            break

        if os.path.isfile(filename):
            print("File already exists!")
            continue

        table = HashTable.HashTable()

        saveDB(table, filename)

        print("Database created succesfully!\n")
        break

def deleteDB():
    while True:
        filename = input("Input database name/path or Quit to quit: ")

        if filename.lower() == "quit":
            break

        if not os.path.isfile(filename):
            print("File doesn't exist!")
            continue
        
        MB = open(filename, "rb").read(4)

        if MB != b"\xDE\xAD\xBE\xEF":
            print("Not a valid database file!")
            continue
        
        os.remove(filename)
        print("Database successfully deleted!\n")
        break

def accessDB():
    while True:
        filename = input("Input database name/path or Quit to quit: ")

        if filename.lower() == "quit":
            break

        if not os.path.isfile(filename):
            print("File doesn't exist!")
            continue
        
        MB = open(filename, "rb").read(4)

        if MB != b"\xDE\xAD\xBE\xEF":
            print("Not a valid database file!")
            continue

        database = loadDB(filename)
        
        print("Database opened")

        editDB(database, filename)
        break

def saveDB(hashtable, filename):

    f = open(filename, "wb")

    f.write(b"\xDE\xAD\xBE\xEF") # Database fingerprint/"Magic bytes" = 0xDEADBEEF

    f.close()

    f = open(filename, "a+")

    entries = hashtable.listAll()

    for entry in entries:
        f.write(f"{entry.key}|{entry.value}\n")
    
    f.close()
        
def loadDB(filename):

    entries = open(filename, "rb+").read()[4:].decode().split("\n") #skip 4 magic bytes

    table = HashTable.HashTable()

    for entry in entries:
        x = entry.split("|")
        if len(x) != 2:
            continue
        table.insert(x[0], x[1])
    
    return table

def editDB(table, filename):

    while True:

        print("What would you like to do?")
        print("1. Insert element")
        print("2. Delete element")
        print("3. List all elements")
        print("4. Print element")
        print("5. Save changes")
        print("6. Close database")

        try:
            choice = int(input())
        except:
            continue

        if choice > 6 or choice < 1:
            continue

        if choice == 1:
            key = input("Enter key: ")
            value = input("Enter value: ")
            table.insert(key, value)
            print("Insertion completed.")
        elif choice == 2:
            key = input("Enter key of element to be deleted: ")
            if table.delete(key):
                print("Deletion completed")
            else:
                print("Element not found")
        elif choice == 3:
            print(table.listAll())
        elif choice == 4:
            key = input("Enter key of element to be searched: ")
            entry = table.lookup(key)
            if entry:
                print(entry)
            else:
                print("Element not found")
        elif choice == 5:
            saveDB(table, filename)
            print("Database saved.")
        elif choice == 6:
            break

    





if __name__ == "__main__":
    mainMenu()