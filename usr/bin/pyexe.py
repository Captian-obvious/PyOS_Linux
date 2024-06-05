#!/usr/bin/env python
import sys;
def main(argc:int,argv:list[str]):
    if argc<2:
        print("ERROR: No input file specified");
    ##endif
##end
main(len(sys.argv),sys.argv);
