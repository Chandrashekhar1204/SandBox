#**************************************************************************************************************************
#   Scons: C compiler settings for GCC ARM aarch64
#**************************************************************************************************************************
import SCons.Tool
from TempFileMungeABB import TempFileMungeABB

def generate(env):
    """
    Setup Default 'cc'
    """
    SCons.Tool.Tool('cc').generate(env)

    """
    Change Variables for GCC ARM Embedded tools
    """
    env.AppendENVPath('PATH', env['compiler_bin'], delete_existing=0)

    env['CC_TEMPFILE'] = TempFileMungeABB
    env['CC'] = 'aarch64-none-elf-gcc.exe'
    env['_CCCOM'] = ('$($CC_WRAPPER$) $CC $CCFLAGS $CFLAGS $($DEBUG_CCFLAGS $DEBUG_CFLAGS$) ' +
                     '$_CCCOMCOM ${SOURCE.abspath} -o ${TARGET.abspath}')

    # this makes the choice between showing the full compiler command line or just filename
    if not env.GetOption('verbose_option'):
        env['CCCOMSTR'] = "Compiling $SOURCE"

    env['CCCOM'] = "${CC_TEMPFILE('$_CCCOM','@')}"
    env['OBJSUFFIX'] = '.obj'
    env['CPPPATH'] = []
    env['CPPDEFINES'] = []
    env['INCPREFIX'] = '-I '
    env['INCSUFFIX'] = ''

def exists(env):
    return env.Detect('CC')
