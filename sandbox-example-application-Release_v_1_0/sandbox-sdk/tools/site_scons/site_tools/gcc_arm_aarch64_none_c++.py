#**************************************************************************************************************************
#   Scons: C++ compiler settings for GCC ARM aarch64
#**************************************************************************************************************************
import SCons.Tool
from TempFileMungeABB import TempFileMungeABB

def generate(env):
    """
    Setup Default "c++"
    """
    SCons.Tool.Tool('c++').generate(env)

    """
    Change Variables for GCC ARM Embedded tools
    """
    env.AppendENVPath('PATH', env['compiler_bin'], delete_existing=0)

    env['CXX_TEMPFILE'] = TempFileMungeABB
    env['CXX'] = 'aarch64-none-elf-gcc.exe'
    env['_CXXCOM'] = ('$($CXX_WRAPPER$) $CXX $CCFLAGS $CXXFLAGS $($DEBUG_CCFLAGS $DEBUG_CXXFLAGS$) ' +
                      '$_CCCOMCOM ${SOURCE.abspath} -o ${TARGET.abspath}')

    # this makes the choice between showing the full compiler command line or just filename
    if not env.GetOption('verbose_option'):
        env['CXXCOMSTR'] = "Compiling $SOURCE"

    env['CXXCOM'] = "${CXX_TEMPFILE('$_CXXCOM','@')}"
    env['OBJSUFFIX'] = '.obj'
    env['CPPPATH'] = []
    env['CPPDEFINES'] = []
    env['INCPREFIX'] = '-I '
    env['INCSUFFIX'] = ''

def exists(env):
    return env.Detect('CXX')
