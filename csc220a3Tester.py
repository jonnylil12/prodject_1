###############################################################
# Auto-Grader (See "A Generic Python Auto-Grader")            #
# File: Tester.py                                             #
# Author: Albert Chan                                         #
# Affiliation: Fayetteville State University                  #
#              Department of Mathematics and Computer Science #
# Copyright (c) 2019                                          #
# License: GPL 2.0                                            #
# Exception: Tester.pyc and the generated TestData.pyc can be #
#            distributed to students without source or        #
#            showing the license                              #
###############################################################

module = 'csc220a3'
function = 'evaluate'
maxScore = 20
testData = 'csc220a3TestData'

def loadFunction (module, path, function):
    import sys
    sys.path.insert (0, path)
    try:
        return getattr (__import__ (module), function)
    finally:
        sys.path.pop (0)

def printMessage (msg):
    print (msg)

def message (record, msg, verbose):
    if verbose:
        record (msg)

def convertToTuple (value):
    return (value if type (value) in (list, tuple) else (value,))

def checkExceptions (tc, resultingException, verbose, record):
    tcID = tc [0]
    expectedException = None
    if len (tc) > 3:
        expectedException = tc [3]

    if expectedException is None:
        if resultingException is None:
            return True
        else:
            message (record, 'TC %d failed - exception %s caught' % (tcID, type (resultingException).__name__), verbose)
            return False

    if resultingException is None:
        message (record, 'TC %d failed - expecting an exception, none raised' % tcID, verbose)
        return False

    if isinstance (resultingException, expectedException):
        return True
    message (record, 'TC %d failed - unexpected exception %s caught' % (tcID, type (resultingException).__name__), verbose)
    return False

def checkReturnValue (tc, actualResult, verbose, record):
    tcID = tc [0]
    expectedResult = tc [2]
    if expectedResult is None:
        if not actualResult is None:
            message (record, 'TC %d failed - not expecting a return value, got %s instead' % (tcID, repr (actualResult)), verbose)
            return False
        else:
            return True

    if actualResult is None:
        message (record, 'TC %d failed - expecting %s, got nothing' % (tcID, repr (expectedResult)), verbose)
        return False

    actualResult = convertToTuple (actualResult)
    expectedResult = convertToTuple (expectedResult)
    if len (actualResult) == len (expectedResult) == 1:
        if actualResult [0] == expectedResult [0]:
            return True
        else:
            message (record, 'TC %d failed - expecting %s, got %s instead' % (tcID, repr (expectedResult [0]), repr (actualResult [0])), verbose)
            return False;

    if len (actualResult) == len (expectedResult):
        n = len (actualResult)
        for i in range (n):
            if not actualResult [i] == expectedResult [i]:
                message (record, 'TC %d failed - expecting %s at position %d, got %s instead' % (tcID, repr (expectedResult [i]), i, repr (actualResult [i])), verbose)
                return False
        return True
    else:
        message (record, 'TC %d failed - expecting a list of %d values, got a list of %d instead' % (tcID, len (expectedResult), len (actualResult)), verbose)
        return False


def runSingleTest (function, testcase, verbose = False, record = printMessage):
    testInput = convertToTuple (testcase [1])
    result = None
    resultingException = None

    try:
        result = function (*testInput)
    except Exception as err:
        resultingException = err

    if checkExceptions (testcase, resultingException, verbose, record):
        if checkReturnValue (testcase, result, verbose, record):
            message (record, 'TC %d passed' % testcase [0], verbose)
            return True
        else:
            return False
    else:
        return False

def runAllTests (testSuite, module = module, path = '.', record = printMessage):
    try:
        fun = loadFunction (module, path, function)
    except:
        record ('File loading error - testing not executed.')
        return 0
    passed = []
    failed = []
    n = len (testSuite)
    for tc in testSuite:
        success = runSingleTest (fun, tc, False, record)
        if success:
            passed.append (tc [0])
        else:
            failed.append (tc [0])

    score = len (passed)
    testScore = float (maxScore) * score / n
    record ('Passed: %s - total %d.' % (passed, len (passed)))
    record ('Failed: %s - total %d.' % (failed, len (failed)))
    record ('\n%d of %d test cases passed. Score = %.2f of %.2f\n' % (score, n, testScore, maxScore))
    return testScore

def runTestCase (i, module = module, path = '.', record = printMessage):
    try:
        fun = loadFunction (module, path, function)
    except:
        record ('File loading error - testing not executed.')
        return 0
    for tc in tests:
        if tc [0] == i:
            runSingleTest (fun, tc, True, printMessage)

if __name__ == '__main__':
    tests = loadFunction (testData, '.', 'tests')
    runAllTests (tests)
