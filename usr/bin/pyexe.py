#!/usr/bin/env python
import io,os,platform,sys,time;
import contextlib as ctx;
from dis import dis;
import subprocess as sub;
import threading as task;
import tkinter as tk;
exe_mark='pe';

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
                self.pe_signature = data[0:4];                                      # PE magic number (usually b'MZ')
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
        the_header_length=the_header.head_len;
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

def processFiles(files:list[str]):
    for i in range(len(files)):
        fn=files[i-1];
        try:
            exe_file_reader=file_reader(fn,'elf');
            print(exe_file_reader.read_header());
        except Exception as e:
            print(e);
        ##endtry
    ##end
##end

def main(argc:int,argv:list[str]):
    if (argc<2):
        print('No input file(s) specified!');
    else:
        args=argv[1:];
        processFiles(args);
    ##endif
##end
main(len(sys.argv),sys.argv);
