#*****************************************************************************************************************************
#   Scons: Assembler settings for GCC ARM aarch64
#*****************************************************************************************************************************
import SCons.Tool
from TempFileMungeABB import TempFileMungeABB

def generate(env):
    """
    Setup Default 'as'
    """
    SCons.Tool.Tool('as').generate(env)

    """
    Change Variables for GCC ARM Embedded tools
    """
    env.AppendENVPath('PATH', env['compiler_bin'], delete_existing=0)

    env['AS_TEMPFILE'] = TempFileMungeABB
    env['AS'] = 'aarch64-none-elf-gcc.exe'
    env['_ASCOM'] = '$($AS_WRAPPER$) $AS $_CCCOMCOM $AFLAGS $_ASCOM ${SOURCE.abspath} -o ${TARGET.abspath}'

    # this makes the choice between showing the full compiler command line or just filename
    if not env.GetOption('verbose_option'):
        env['ASCOMSTR'] = "Compiling ${SOURCE}"

    env['ASCOM'] = "${AS_TEMPFILE('$_ASCOM','@')}"
    env['OBJSUFFIX'] = '.obj'
    env['CPPPATH'] = []
    env['CPPDEFINES'] = []
    env['INCPREFIX'] = '-I '
    env['INCSUFFIX'] = ''

def exists(env):
    return env.Detect('AS')
