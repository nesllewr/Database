import random

def createRandomCode(length):
    string = ""
    
    code = [
        ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
        ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    ]
    
    for i in range(length):
        string += code[random.randint(0, 1)][random.randint(0,9)]
    
    return string