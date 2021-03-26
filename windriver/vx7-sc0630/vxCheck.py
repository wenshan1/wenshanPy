#!/usr/bin/env python
"""
This file checks the comments sections of a .c or .h file for conformance
with the VxWorks coding standard
"""

import argparse
import os
import re
import six
import sys

""" first line of file """
LINE_ONE_STD = r"^/\* %s - .*\*/$"
LINE_ONE_DOX = r"^/\*\* \\file \\brief %s - .*\*/$"
LINE_ONE = LINE_ONE_STD

""" module header strings """
DESCRIPTION_STD = "DESCRIPTION"
DESCRIPTION_DOX = "* ### Description"
DESCRIPTION = DESCRIPTION_STD

INCLUDE_FILES_STD = "INCLUDE FILES:"
INCLUDE_FILES_DOX = "### Include Files:"
INCLUDE_FILES = INCLUDE_FILES_STD

""" Function header strings """
SEE_ALSO_STD = "SEE ALSO:"
SEE_ALSO_DOX = "### See Also:"
SEE_ALSO = SEE_ALSO_STD


""" Copyright strings """
COPYRIGHT_LINE = \
    re.compile(r"^ \* Copyright \(c\) [0-9, \-]* Wind River Systems, Inc\.$")
COPYRIGHT_FIRST_SENTENCE = \
    " * The right to copy, distribute, modify or otherwise make use"
COPYRIGHT_SECOND_SENTENCE = \
    " * of this software may be licensed only pursuant to the terms"
COPYRIGHT_THIRD_SENTENCE = \
    " * of an applicable Wind River license agreement."

""" Mod history strings """
MOD_HISTORY_TITLE  = "modification history"
MOD_HISTORY_DASHES = "--------------------"

""" Possible function header """
FUNCTION_LINE = re.compile(r"/\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\**")

lineCount = 0
copyrightString = ""
years = []
fileName = ""
isCFile = True
foundTab = False
foundCr = False
foundModHistory = False

def readNextLine():
    """ read next line and cleanup """

    global lineCount, foundTab, foundCr, foundModHistory

    line = inputFile.readline()
    if not line:
        if not foundModHistory:
            print("Mod History title '{}' not found".format(MOD_HISTORY_TITLE))
        sys.exit(0)
        
    lineCount += 1

    try:
        line = line.decode('ascii')
    except UnicodeDecodeError:
        print("line %d contains UNICODE characters" % lineCount)
        itIs(line)
    
    if not foundTab and line.find('\t'):
        foundTab = True
        print("file contains TAB characters")
        
    if not foundCr and line.find('\r'):
        foundCr = True
        print("file contains CR (possible DOS EOL)")
        
    line = line.strip("\n")
    if (len(line) > 80):
        print("line %d is longer than 80 characters" % lineCount)
    return line.rstrip()


def itIs(line):
    """ itIs - print message about original line that is in error """

    print("It is '{}'".format(line)) 
        
        
def processFileTitle(line):
    """ processFileTitle - validate first 2 lines of file """ 

    fileBase = os.path.basename(fileName)
    print("Processing %s" % fileName)

    lineOne = re.compile(LINE_ONE % fileBase)
    if not lineOne.match(line):
        print("First line is not correct")
        print("it should match "+LINE_ONE % fileBase)
        itIs(line)
        sys.exit(1)
    line = readNextLine()

    if line:
        print("Second line is not correct")
        print("It should be a completely blank line")
        itIs(line)
    else:
        line = readNextLine()
    return line

    
def processCopyrightYears(line):
    """ processCopyright - validate the copyrightyears header

    to do this we need to parse the date in the copyright header
    the date format is nnnn,nnnn-nnnn,nnnnn  with possible white space

    the entire copyright format can be seen at the begining of this file.
    """ 

    global years

    """
    We split the copyright line up in order to process the years
    index 0 is "/*"
    index 1 is "Copyright"
    index 2 is "(c)"
    index 3 is the start of the first year.                    
    """                         
    dateIndex = 3

    # Convert commas to spaces for separating dates and date ranges
    sline = line.replace(',', ' ').split()
    if len(sline) <= 3:
        return
    
    CopyrightDate = sline[dateIndex]
    if not CopyrightDate[0].isdigit():
        print("Incorrect copyright year %s" % CopyrightDate[0])
        print("only years such as 2017 should be after the (c)")
        return

    while CopyrightDate[0:1].isdigit():
        CopyrightDate = CopyrightDate.rstrip(",")
        sdate = CopyrightDate.split("-")
        if len(sdate) > 1:
            if not sdate[0].isdigit() or not sdate[1].isdigit():
                print("line {} incorrect date format {}".format(
                    lineCount, CopyrightDate))
                return
            
            start = int(sdate[0])
            end = int(sdate[1])
            if start > end:
                print("Line {} the copyright line may not be correct".format
                       (lineCount))
                return
            while start <= end:
                years.append(str(start))
                start += 1
        else:
            years.append(CopyrightDate)
        dateIndex += 1
        if dateIndex < len(sline)-1 and sline[dateIndex] == ",":
            dateIndex += 1
        if dateIndex == len(sline):
            break
        CopyrightDate = sline[dateIndex]
#    print(years)


def copyrightLineIncorrect():
    """ copyrightLineIncorrect - print an error message """

    print("line {} of the copyright is incorrect".format(lineCount))

    
def processCopyright(line):
    """ processCopyright - validate the copyright notice """

    global copyrightString

    #print("Check copyright")
    #print(line)
    if myArgs.doxygen:
        if line != "/**":
            copyrightLineIncorrect()
            print("It should read '/**' only")
            itIs(line)
        line = readNextLine()
        if line != "* \internal \copyright":
            copyrightLineIncorrect()
            print("It should read '* \internal \copyright' only")
            itIs(line)
        line = readNextLine()
        if line != "*":
            copyrightLineIncorrect()
            print("It should read '*' only")
            itIs(line)
    else:        
        if line != "/*":
            copyrightLineIncorrect()
            print("It should read /* only")
            itIs(line)

    line = readNextLine()

    copyrightString = line
    if not re.match(COPYRIGHT_LINE, line):
        print("Copyright line may not be correct")
        itIs(line)
    
    processCopyrightYears(line)
    line = readNextLine()

    if line == " * Wind River Systems, Inc.":
        line = readNextLine()
    elif line != " *":
        copyrightLineIncorrect()
        print('It should read " *" only')
        itIs(line)
    line = readNextLine()

    if line != COPYRIGHT_FIRST_SENTENCE:
        copyrightLineIncorrect()
        print('It should read [{}]'.format(COPYRIGHT_FIRST_SENTENCE))
        itIs(line)
    line = readNextLine()

    if line != COPYRIGHT_SECOND_SENTENCE:
        copyrightLineIncorrect()
        print('It should read [{}]'.format(COPYRIGHT_SECOND_SENTENCE))
        itIs(line)
    line = readNextLine()

    if line != COPYRIGHT_THIRD_SENTENCE:
        copyrightLineIncorrect()
        print('It should read [{}]'.format(COPYRIGHT_THIRD_SENTENCE))
        itIs(line)
    line = readNextLine()

    if line != " */":
        copyrightLineIncorrect()
        print("expecting closing comment */")
        itIs(line)
    line = readNextLine()

    if line != "":
        copyrightLineIncorrect()
        print("Expecting blank line")
        itIs(line)
    line = readNextLine()

    if not line:
        line = readNextLine()
    return line


def functionHeaderIncorrect():
    """ functionHeaderIncorrect - print an error message """

    print("line {} of a Function Header is incorrect".format(lineCount))


def modHistoryLineIncorrect():
    """ modHistoryLineIncorrect - print an error message """

    print("line {} of the modification history is incorrect".format(lineCount))


def processModHistory(line):
    """ processModHistory - validate modification history and copyright dates

    the format of the mod history is nnl,nnMONYR,lll or nnMONYR,lll
    """ 

    global foundModHistory
    
    if myArgs.doxygen:
        if line != "/**":
            modHistoryLineIncorrect()
            print("expecting '/**'")
            itIs(line)
        line = readNextLine()
        if line != "*":
            modHistoryLineIncorrect()
            print("expecting '*'")
            itIs(line)
        line = readNextLine()
        if line != "\internal":
            modHistoryLineIncorrect()
            print("expecting '\internal'")
            itIs(line)
    else:
        if line != "/*":
            modHistoryLineIncorrect()
            print("expecting '/*'")
            itIs(line)

    line = readNextLine()

    print("Searching for '{}'".format(MOD_HISTORY_TITLE))

    while line != MOD_HISTORY_TITLE:
        line = readNextLine()
        
    foundModHistory = True
    
#    if line != MOD_HISTORY_TITLE:
#        modHistoryLineIncorrect()
#        print("expecting [%s]" % MOD_HISTORY_TITLE)
#        itIs(line)
#        return
    
    line = readNextLine()
    if line != MOD_HISTORY_DASHES:
        modHistoryLineIncorrect()
        print("expecting [%s]" % MOD_HISTORY_DASHES)
        itIs(line)
        return

    line = readNextLine()
    while (line.lstrip() != "*/"):
        if len(line.split()) == 0:
            line = readNextLine()
            continue
        ModHistoryDate = line.split()[0]

        theDate = ModHistoryDate.split(",")
        if ModHistoryDate.count(',') == 1:
            theDate = ModHistoryDate.split(",")[0]
        elif ModHistoryDate.count(',') == 0:
            line = readNextLine()
            continue
        else:
            theDate = ModHistoryDate.split(",")[1]

        if not re.match(r"^[0-9]+", theDate):
            line = readNextLine()
            continue

        if not theDate[-2:].isdigit():
            print("Invalid mod history line %d" % lineCount)
            itIs(theDate[-2:])
            line = readNextLine()
            continue
            
        if int(theDate[-2:]) > 50:
            ModHistoryYear = "19" + theDate[-2:]
        else:
            ModHistoryYear = "20" + theDate[-2:]
        

#        print(ModHistoryYear)

        if ModHistoryYear not in years:
            print("Modification History year " + 
                   ModHistoryYear + " is not in copyright year list:")
            print(copyrightString)
#            print(years)
            itIs(line)

        line = readNextLine()

    line = readNextLine()
    if line.lstrip() != "":
        print("line {} after mod history must be blank".format(lineCount))
        itIs(line)
    line = readNextLine()

    return line


def processDescription(line):
    """ processDescription - validate the description comment 
        then look for key word INCLUDES:
    """

    if not isCFile:
        return line

    foundIncludes = 0

    if myArgs.doxygen:
        if line != "/**":
            print("first line {} of description is incorrect".format(lineCount))
            print("Expecting '/**'")
            itIs(line)
    else:
        if line != "/*":
            print("first line {} of description is incorrect".format(lineCount))
            print("Expecting '/*'")
            itIs(line)

    line = readNextLine()
    if line != DESCRIPTION:
        print("second line {} of description is incorrect".format(lineCount))
        print("Expecting '{}'".format(DESCRIPTION))
        itIs(line)

    line = readNextLine()

    while (line.lstrip() != "*/"):
        if line.find(INCLUDE_FILES) >= 0:
            foundIncludes = 1
        line = readNextLine()

    if foundIncludes == 0:
        print("Description is incorrect")
        print("Missing '{}'".format(INCLUDE_FILES))

    return line


def processFunction(line):
    """ processFunction - validate the function comment header

    look for key word RETURNS:  then ERRNO:
    look for function parameter list format as follows
    after function header
    ie int foo
           (
           para bar,  /* comment */
           para bar2  /* comment */
           )
    """

    if not isCFile:
        return line

    foundReturns = 0
    foundErrno = 0
    
    FunctionCommentString = line
    if FunctionCommentString.count('*') != 79:
        functionHeaderIncorrect()
        print("Function header initial comment line is not 80 characters")
        print('Is has {} stars'.format(FunctionCommentString.count('*')))
        return line

    line = readNextLine()
    if line != "*":
        functionHeaderIncorrect()
        print("expecting '*'")
        itIs(line)
        return line

    line = readNextLine()
    foo = line.split()
    """
    Function Header String should be at least 4 elements when split:
        * FunctionName - whatitdoes                             
    """
    if len(foo) <= 3:
        functionHeaderIncorrect()
        print("Expecting: '* FunctionName - whatitdoes'")
        print("Incorrect function header one line description")
        itIs(line)
        return line
        
    if (foo[0] != "*") or (foo[2] != "-"):
        functionHeaderIncorrect()
        print("Expecting: '* FunctionName - whatitdoes'")
        print("Incorrect function header one line description")
        itIs(line)
        return line

    if myArgs.doxygen:
        if (foo[1][0:2] != "**") or (foo[1][-2:] != "**"):
            functionHeaderIncorrect()
            print("Function name must have two stars before and after")
            itIs(foo[1])
            return line

    line = readNextLine()
    if line != "*":
        functionHeaderIncorrect()
        print("Title line must contain only a single-line description")
        print("expecting [*]")
        itIs(line)
        return line

    line = readNextLine()
    while (line.lstrip() != "*/"):
        if line.find("RETURNS:") >= 0:
            foundReturns = 1
        elif line.find("ERRNO:") >= 0:
            foundErrno = 1
        line = readNextLine()

    if foundReturns == 0:
        functionHeaderIncorrect()
        print("Missing RETURNS:")
        return line

    line = readNextLine()
    if line != "":
        functionHeaderIncorrect()
        print("Line after function header comment must be blank")
        itIs(line)
        return line

    line = readNextLine()
    if line.find(r"(void)") >= 0:
        return line

    line = readNextLine()
    if line.lstrip() != "(":
        functionHeaderIncorrect()
        print("The line following the function name must contain only [(]")
        itIs(line)
        return line
        
    line = readNextLine()
    while (line.lstrip() != ")"):
        if not re.search(".*/\*.*\*/", line):
            functionHeaderIncorrect()
            print("Each function parameter must have a comment")
            itIs(line)
            return line
            
        line = readNextLine()

    return line
        

def processLine(line):
    """ processLine - validate the current line in the file """ 

    line = processFileTitle(line)
    line = processCopyright(line)
    line = processModHistory(line)
    line = processDescription(line)

    while True:
        if isCFile and line and re.match(FUNCTION_LINE, line):
            processFunction(line)
        line = readNextLine()

def processArgs(help=False):
    """ processArgs - process the arguments to this script """

    parser = argparse.ArgumentParser(
        description="Check VxWorks Coding Convention comments")
    parser.add_argument('fileName', help='.c or .h file name')
    parser.add_argument("-d", "--doxygen", help="check doxygen markup",
                        action="store_true")

    if help:
        parser.print_help()

    return parser.parse_args()


###############################################################################
if __name__ == '__main__':
    """ main code """

    myArgs = processArgs()
    fileName = myArgs.fileName
    if fileName.endswith('.c'):
        isCFile = True
    elif fileName.endswith('.h'):
        isCFile = False
    else:
        print("Input file is not a .c or .h file")
        sys.exit(1)

    if myArgs.doxygen:
        LINE_ONE = LINE_ONE_DOX
        DESCRIPTION = DESCRIPTION_DOX
        INCLUDE_FILES = INCLUDE_FILES_DOX
        SEE_ALSO = SEE_ALSO_DOX
        
    with open(fileName, 'r') as inputFile:
        line = readNextLine()
        processLine(line)
        
# EOF