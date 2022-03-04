import sys
args = sys.argv[1:]
if len(args) == 0:
    print("Please pass args!")
elif len(args) == 1:
    dPath = args[0]
    print(dPath)
else:
    print("Hello")
