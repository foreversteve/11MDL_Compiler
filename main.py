from script import run
import sys

if len(sys.argv) == 2:
    run(sys.argv[1])
elif len(sys.argv) == 1:
    run(input("please enter the filename of an mdl script file: \n"))
else:
    print ("Too many arguments.")
'''
B,C
C,E(B),C
A,A,A,D
D,E,A,B,C
B,C,E,C,B
'''
