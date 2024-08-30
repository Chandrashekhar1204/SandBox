#*****************************************************************************************************************************
#
#   Scons: tool directories for MinGW
#   Scons supports MinGW out of the box, but building UNICOS requires some advanced linker configuration,
#   so for flexbility this follows the same structure as the other customized compilers.
#
#*****************************************************************************************************************************
# pylint: disable=E0401, C0103, C0301

#-----------------------------------------------------------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------------------------------------------------------
import os.path

class Config:
    def __init__(self, path, target_architecture):
        
        accepted_architectures = ["i686", "x86_64"]
        architecture = target_architecture.split("-")[0]
        if architecture not in accepted_architectures:
            accepted_prefixes = " ".join([s +'-' for s in accepted_architectures])
            raise SystemExit(f"Unexpected GCC architecture: {target_architecture}. It should start with one of these: {accepted_prefixes}")
        # Installation directory:
        self.root = path
        self.bin = self.root + '/bin'
        self.mingw_path = self.root
        self.target_arch = target_architecture
        

        self.version_info = ''                             # Name of the tool that prints the compiler version
        self.name =    f'mingw-w64-{architecture}-gcc'     # Name of the tool (this must match with the folder name in turel\site_scons\cgt_sysfiles)
        self.ar_cfg  = f'mingw-w64-{architecture}-gcc_ar'  # Archiver tool name
        self.asm_cfg = f'mingw-w64-{architecture}-gcc_asm' # Asm compiler tool name
        self.c_cfg   = f'mingw-w64-{architecture}-gcc_c'   # C compiler tool name
        self.cpp_cfg = f'mingw-w64-{architecture}-gcc_c++' # C++ compiler tool name
        self.lnk_cfg = f'mingw-w64-{architecture}-gcc_lnk' # Linker tool name
        
        # These are set to make MinGW and MSVC interchangeable
        self.cs_cfg = None
        self.msvc_script = None

        # Check if the tool is installed
        if not os.path.isdir(self.root):
            raise SystemExit("GCC could not be found in: " + self.root)

        if not os.path.isdir(self.bin):
            raise SystemExit(f"{self.bin} could not be found!")
