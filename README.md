# CPP14 CFG Extractor
A practical and educational implementation of CPP14 source code
CFG extractor, implemented using Python3 and Antlr4.

A Control Flow Graph (CFG) is the graphical representation of control flow
or computation during the execution of programs or applications.
Control flow graphs are mostly used in static analysis as well as compiler
applications, as they can accurately represent the flow inside a program unit.
The control flow graph was originally developed by Frances E. Allen.

## Getting started
The program have been implemented and tested using python3.8, though, it would be ok
with other minor python3 versions (3.x).

Install Antlr4 how it described in the following link. 

[Antlr4 Installation Guide](https://github.com/antlr/antlr4/blob/master/doc/python-target.md)

## How to extract CFG from source code
By running the `src/cfg_from_stdin.py` a prompt will be shown
in terminal asking for the source code path. 
```bash
python3 src/cfg_from_stdin.py
```