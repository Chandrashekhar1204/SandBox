#*****************************************************************************************************************************
#   Scons: tool directories for GCC ARM aarch64 none
#*****************************************************************************************************************************
import os

class Config:
    def __init__(self, path = ''):
        self.root = path
        self.bin = self.root + '/bin'

        self.name = 'gcc_arm_none_aarch64'            # Name of the tool (this must match with the folder name in site_scons\cgt_sysfiles)
        self.version_info = ''                        # Name of the tool that prints the compiler version
        self.ar_cfg = 'gcc_arm_aarch64_none_ar'       # Name of the archiver settings file in site_scons\site_tools
        self.asm_cfg = 'gcc_arm_aarch64_none_asm'     # Name of the assembler settings file in site_scons\site_tools
        self.c_cfg = 'gcc_arm_aarch64_none_c'         # Name of the c compiler settings file in site_scons\site_tools
        self.cpp_cfg = 'gcc_arm_aarch64_none_c++'     # Name of the c++ compiler settings file in site_scons\site_tools
        self.lnk_cfg = 'gcc_arm_aarch64_none_lnk'     # Name of the linker settings file in site_scons\site_tools
        self.stripper = 'gcc_arm_aarch64_stripper'    # Name of the elf stripper file in site_scons\site_tools

        # Check if the tool is installed
        if not os.path.isdir(self.root):
            raise SystemExit(f"{self.root} is not installed!")

        if not os.path.isdir(self.bin):
            raise SystemExit(f"{self.bin} could not be found!")
