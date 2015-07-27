# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re

'''
TODO:
    full match -- offset begin, offset end
'''

class Clangchecker(object):
    lineList = ''
    text = ''
    errorCount = 0

    def __init__(self, filePath):
        f = open(filePath)
        self.lineList = f.readlines()
        f.seek(0)
        self.text = f.read()
        self.errCheck()
        #self.errPrint(int(offset))
        #print self.text
        
    def errCheck(self):
        reg = [
            ['tabCheck',['\\t']],
            ['commentCheck',['/\*[\w]']],
            ['bracketsCheck',['\}[\w]', '\( ', ' \)']],
            ['grammerCheck',['\?[\w]', '[^}] else', ',[\w&*]', '[ ](for|while|if|switch)\([\w\d!]']],
            ['macroCheck',['#[ ]*(include|define|if|ifdef|ifndef|elif|else|undef|line|pragma)[^ ]']]
        ]
        regLen = len(reg)
        for i in range(regLen):
            print(reg[i][0] + ':')
            #print('----------------')
            for expression in reg[i][1]:
                offset = 0
                pattern = re.compile(expression)
                match = pattern.search(self.text[offset:])
                if match:
                    print('error: \'' + expression + '\'')
                while match:
                    offset += match.start()+1
                    self.errPrint(offset)
                    match = pattern.search(self.text[offset:])
            print('--- complete ---')
            
    def getLine(self, lineCount, offset):
        for i in range(lineCount):
            offset -= len(self.lineList[i])
            if offset < 0:
                return i, offset + len(self.lineList[i])
                
    def errPrint(self, offset):
        lineCount = len(self.lineList)
        lineNo, offset = self.getLine(lineCount, offset)
        print('line ' + str(lineNo + 1) + ':')
        print(self.lineList[lineNo], end = '')
        space = ''
        for i in range(offset-1):
            space += ' '
        print(space + '^', end = '\n')

filePath = raw_input("filePath:")
check = Clangchecker(filePath)
