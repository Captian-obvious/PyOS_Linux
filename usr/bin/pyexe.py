#!/usr/bin/env python
import argparse,io,os,platform,sys,time;
import contextlib as ctx;
from dis import dis;
import subprocess as sub;
import threading as task;
#import tkinter as tk;
import traceback;
exe_mark='pe';
ver="3.45.3";
if (platform.system()=='Linux'):
    exe_mark='elf';
##endif
class file_reader:
    class exe_headers:
        def __init__(self):
            pass;
        ##end
        class elf:
            def __init__(self,data):
                # Parse the ELF header data (e.g., read from a file)
                self.magic_number=data[0:4];# ELF magic number (usually b'\x7fELF')
                if self.magic_number!=b"\x7fELF":
                    return "invalid";
                ##endif
                self.file_class=data[4];# 32-bit (1) or 64-bit (2)
                self.endianness=data[5];# Little-endian (1) or big-endian (2)
                self.version=data[6];# ELF version (usually 1)
                self.os_abi=data[7];# OS/ABI identification
                self.e_type=data[16];# Object file type
                if self.e_type==2 or self.e_type==3:#if the file is a shared library or an executable
                    self.machine_architecture=b''+data[18:20];# Machine architecture (e.g., x86, ARM, etc.)
                    self.entry_point_address=int.from_bytes(data[24:32],byteorder='little');# Entry point address
                    self.program_header_offset=int.from_bytes(data[32:40],byteorder='little');# Program header offset
                    self.section_header_offset=int.from_bytes(data[40:48],byteorder='little');# Section header offset
                    if (self.file_class==1):
                        self.num_program_headers=int.from_bytes(data[54:56],byteorder='little');# Number of program header entries
                        self.num_section_headers=int.from_bytes(data[56:58],byteorder='little');# Number of section header entries
                        self.size_program_header_entry=int.from_bytes(data[58:60],byteorder='little');# Size of program header entry
                        self.size_section_header_entry=int.from_bytes(data[60:62],byteorder='little');# Size of section header entry
                        self.head_len=62;
                    elif (self.file_class==2):
                        self.num_segments=int.from_bytes(data[62:64],byteorder='little');
                        self.head_len=64;
                    else:
                        print("Invalid ELF File!");
                    ##endif
                ##endif
            ##end
            def __str__(self):
                return f"ELF Header:\n" \
               f"  Magic: {self.magic_number}\n" \
               f"  Class: {self.file_class}\n" \
               f"  Endianness: {self.endianness}\n" \
               f"  ELF Version: {self.version}\n" \
               f"  OS/ABI: {self.os_abi}\n" \
               f"  Object File Type: {self.e_type}\n" \
               f"  Machine Architecture: {self.machine_architecture}\n" \
               f"  Entry Point Address: 0x{self.entry_point_address:08X}\n" \
               f"  Program Header Offset: 0x{self.program_header_offset:08X}\n" \
               f"  Section Header Offset: 0x{self.section_header_offset:08X}\n" \
            ##end
        ##end
        class pe:
            def __init__(self,data):
                #self.magic=b"PE\x00\x00";
                # Parse the PE header data (e.g., read from a file)
                self.pe_signature = data[0:4];# PE magic number (usually b'MZ')
                if self.pe_signature!=b"MZ":
                    return "invalid";
                ##endif
                self.machine_type = int.from_bytes(data[4:6],byteorder='little');
                self.num_sections = int.from_bytes(data[6:8],byteorder='little');
                self.head_len=20;
                # Add more fields as needed
            ##end
            def __str__(self):
                return f"PE Header:\n" \
                       f"  Signature: {self.pe_signature}\n" \
                       f"  Machine Type: {self.machine_type}\n" \
                       f"  Number of Sections: {self.num_sections}\n";
                # Include other fields in the string representation
            ##end
        ##end
        class mo:
            def __init__(self,data):
                self.magic32=b"\xfe\xed\xfa\xce";
                self.magic64=b"\xfe\xed\xfa\xcf";
            ##end
        ##end
    ##end
    class ExecutableFormatError(Exception):
        def __init__(self,exe="unknown"):
            super().__init__(self,f"Invalid Executable Format! Expected ELF,PE or MO. Got {exe}.");
        ##end
    ##end
    def __init__(self,file:str,exe_type:str):
        self.exe_type=exe_type;
        self.file=open(file,'rb');
        self.headers=self.exe_headers();
        if (self.exe_type=="elf"):
            self.fheader=self.headers.elf;
        elif (self.exe_type=="mo"):
            self.fheader=self.headers.mo;
        elif (self.exe_type=="pe"):
            self.fheader=self.headers.pe;
        else:
            raise self.ExecutableFormatError(self.exe_type);
        ##endif
    ##end
    def read_header(self):
        the_header=self.fheader(self.read());
        if the_header!="invalid":
            the_header_length=the_header.head_len;
        ##endif
        return the_header;
    ##end
    def read(self,*args):
        return self.file.read(*args);
    ##end
    def close(self):
        self.file.close();
    ##end
##end
class JIT_Compiler:
    def __init__(self,bytecode:bytes|None=None):
        self.loaded=bytecode;
        self.code="";
    ##end
    def start(self):
        pass;
    ##end
    def __decompile__(self):
        pass;
    ##end
    def __run__(self):
        pass;
    ##end
##end
class Interpreter:
    def __init__(self):
        self.code="";
        self.finished=False;
    ##end
    def init(self,codetorun=""):
        self.finished=False;
        if codetorun!="":
            self.code=codetorun;
        ##endif
    ##end
    def run(self):
        loaded=self.code;
        output=exec(loaded);
        self.finished=True;
    ##end
##end
class Interactive:
    def __init__(self):
        pass;
    ##end
    def start(self):
        arch=platform.machine();
        print(f'PyEXE v{ver} ({arch}) on {platform.system()}');
        print(f'Type "help", "copyright", "credits", or "license" for more information.');
        while True:
            cmd=input('>>>');
            if cmd==None:
                cmd="";
            ##endif
            if cmd.startswith('if '):
                if cmd.endswith(":"):
                    cmd=self.__define__(cmd,1);
                ##endif
            elif cmd.startswith('def '):
                if cmd.endswith(":"):
                    cmd=self.__define__(cmd,1);
                ##endif
            elif cmd.startswith('for '):
                if cmd.endswith(":"):
                    cmd=self.__define__(cmd,1);
                ##endif
            elif cmd.startswith('while '):
                if cmd.endswith(":"):
                    cmd=self.__define__(cmd,1);
                ##endif
            elif cmd.startswith('class '):
                if cmd.endswith(":"):
                    cmd=self.__define__(cmd,1);
                ##endif
            elif cmd.startswith('try'):
                if cmd.endswith(":"):
                    cmd=self.__define_try__(cmd,1);
                ##endif
            ##endif
            try:
                exec(cmd);
            except Exception as e:
                print(traceback.format_exc());
            ##endtry
        ##end
    ##end
    def __define__(self,cmd,layer):
        function_typing=True;
        def_content=cmd+"\n";
        indent=4;
        while function_typing:
            cmd2=input('...'+" "*(indent*layer));
            if cmd2==None:
                cmd2="";
            ##endif
            if cmd2.startswith('if '):
                if cmd2.endswith(":"):
                    cmd2=self.__define__(cmd2,layer+1);
                else:
                    def_content=cmd2;
                    break;
                ##endif
            elif cmd2.startswith('def '):
                if cmd2.endswith(":"):
                    cmd2=self.__define__(cmd2,layer+1);
                else:
                    def_content=cmd2;
                    break;
                ##endif
            elif cmd2.startswith('for '):
                if cmd2.endswith(":"):
                    cmd2=self.__define__(cmd2,layer+1);
                else:
                    def_content=cmd2;
                    break;
                ##endif
            elif cmd2.startswith('while '):
                if cmd2.endswith(":"):
                    cmd2=self.__define__(cmd2,layer+1);
                else:
                    def_content=cmd2;
                    break;
                ##endif
            elif cmd2.startswith('class '):
                if cmd.endswith(":"):
                    cmd2=self.__define__(cmd2,layer+1);
                else:
                    def_content=cmd2;
                    break;
                ##endif
            elif cmd2.startswith('try'):
                if cmd2.endswith(":"):
                    cmd2=self.__define_try__(cmd2,layer+1);
                else:
                    def_content=cmd2;
                    break;
                ##endif
            ##endif
            if cmd2=="":
                break;
            else:
                def_content+=(" "*(indent*layer))+cmd2+"\n";
            ##endif
        ##end
        return def_content
    ##end
    def __define_try__(self,cmd,layer):
        function_typing=True;
        def_content=cmd+"\n";
        indent=4;
        try_indent=" "*(indent*(layer-1));
        while function_typing:
            cmd2=input('...'+try_indent);
            if cmd2==None:
                cmd2="";
            ##endif
            if cmd2.startswith(" "*(indent*layer)+'if '):
                if cmd2.endswith(":"):
                    cmd2=self.__define__(cmd2,layer+1);
                else:
                    def_content=cmd2;
                    break;
                ##endif
            elif cmd2.startswith(" "*(indent*layer)+'def '):
                if cmd2.endswith(":"):
                    cmd2=self.__define__(cmd2,layer+1);
                else:
                    def_content=cmd2;
                    break;
                ##endif
            elif cmd2.startswith(" "*(indent*layer)+'for '):
                if cmd2.endswith(":"):
                    cmd2=self.__define__(cmd2,layer+1);
                else:
                    def_content=cmd2;
                    break;
                ##endif
            elif cmd2.startswith(" "*(indent*layer)+'while '):
                if cmd2.endswith(":"):
                    cmd2=self.__define__(cmd2,layer+1);
                else:
                    def_content=cmd2;
                    break;
                ##endif
            elif cmd2.startswith(" "*(indent*layer)+'class '):
                if cmd.endswith(":"):
                    cmd2=self.__define__(cmd2,layer+1);
                else:
                    def_content=cmd2;
                    break;
                ##endif
            elif cmd2.startswith(" "*(indent*layer)+'try'):
                if cmd2.endswith(":"):
                    cmd2=self.__define_try__(cmd2,layer+1);
                else:
                    def_content=cmd2;
                    break;
                ##endif
            ##endif
            if cmd2=="":
                break;
            else:
                def_content+=try_indent+cmd2+"\n";
            ##endif
        ##end
        return def_content;
    ##end
##end
def processArgs(args):
    parser=argparse.ArgumentParser(description='PyEXE (built-in)');
    parser.add_argument('--build',action='store_true',help='Create a PyEXE binary from a python script');
    parser.add_argument('--interactive','-i',action='store_true',help='Load interactive interpreter.');
    parser.add_argument('files', nargs='*',help='Input file path(s)');
    parser.add_argument('--output','--out','--outfile','-o', help='Output file path');
    parser.add_argument('-c',help='code to be ran');
    args=parser.parse_args(args);
    if args.build:
        print('running build');
        build(args);
    elif args.interactive:
        inter=Interactive();
        inter.start();
    elif args.c:
        thecode=args.c;
        compiler=Interpreter();
        compiler.init(thecode);
        compiler.run();
    else:
        processFiles(args.files);
    ##endif
##end
def build(args):
    print(args.files);
##end
def processFiles(files:list[str]):
    for i in range(len(files)):
        fn=files[i-1];
        try:
            if (fn.endswith('.py') or fn.endswith('.pyw')):
                thefile=open(fn,mode="r");
                theexecute=Interpreter();
                theexecute.init(thefile.read());
                theexecute.run();
            else:
                #check if its an ascii executable (it might be for linux)
                thefile=open(fn,mode="r");
                if e:
                    theexecute=Interpreter();
                    theexecute.init(thefile.read());
                    theexecute.run();
                else:
                    exe_file_reader=file_reader(fn,'elf');
                    print(exe_file_reader.read_header());
                ##endif
            ##endif
        except Exception as e:
            print(e);
        ##endtry
    ##end
##end
def main(argc:int,argv:list[str]):
    if (argc<2):
        print('No input file(s) specified!');
        inter=Interactive();
        inter.start();
    else:
        args=argv[1:];
        processArgs(args);
    ##endif
##end
main(len(sys.argv),sys.argv);
