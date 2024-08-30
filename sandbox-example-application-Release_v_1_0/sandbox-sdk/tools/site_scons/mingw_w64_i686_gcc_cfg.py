#*****************************************************************************************************************************
#
#   Scons: tool directories for MinGW
#   Scons supports MinGW out of the box, but building UNICOS requires some advanced linker configuration,
#   so for flexbility this follows the same structure as the other customized compilers.
#
#*****************************************************************************************************************************

#-----------------------------------------------------------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------------------------------------------------------
import os.path
import sys

class Config:
    def __init__(self, path = ''):
        self.root = path
        self.bin = self.root + '/bin'


        self.name = 'mingw-w64-i686-gcc'        # Name of the tool (this must match with the folder name in turel\site_scons\cgt_sysfiles)
        self.version_info = ''                  # Name of the tool that prints the compiler version
        self.ar_cfg = 'mingw-w64-i686-gcc_ar'   # Archiver tool name
        self.asm_cfg = 'mingw-w64-i686-gcc_asm' # Asm compiler tool name
        self.c_cfg = 'mingw-w64-i686-gcc_c'     # C compiler tool name
        self.cpp_cfg = 'mingw-w64-i686-gcc_c++' # C++ compiler tool name
        self.lnk_cfg = 'mingw-w64-i686-gcc_lnk' # Linker tool name
        
        # These are set to make MinGW and MSVC interchangeable
        self.cs_cfg = None
        self.msvc_script = None

        # Check if the tool is installed
        if not os.path.isdir(self.root):
            raise SystemExit("GCC could not be found in: " + self.root)

        if not os.path.isdir(self.bin):
            raise SystemExit(f"{self.bin} could not be found!")
