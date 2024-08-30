#*****************************************************************************************************************************
#   Scons: Archiver settings for GCC ARM aarch64
#*****************************************************************************************************************************
import SCons.Tool
from TempFileMungeABB import TempFileMungeABB

def generate(env):
    """
    Setup Default 'ar'
    """
    SCons.Tool.Tool('ar').generate(env)

    """
    Change Variables for GCC ARM Embedded tools
    """
    env.AppendENVPath('PATH', env['compiler_bin'], delete_existing=0)

    env['AR_TEMPFILE'] = TempFileMungeABB
    env['AR'] = 'aarch64-none-elf-ar.exe'
    env['_ARCOM'] = '$($AR_WRAPPER$) $AR cr $ARFLAGS $TARGET $SOURCES'

    if not env.GetOption('verbose_option'):
        env['ARCOMSTR'] = "Archiving ${TARGET}"

    env['ARCOM'] = "${AR_TEMPFILE('$_ARCOM','@')}"
    env['ARFLAGS'] = []
    env['LIBPREFIX'] = ''
    env['LIBSUFFIX'] = '.lib'

    # SCons.Tool.Tool('ar').generate(env) may detect ranlib from
    # another compiler. If it does, remove ranlib
    if env.Detect('ranlib'):
        del env['RANLIB']
        del env['RANLIBFLAGS']
        del env['RANLIBCOM']

def exists(env):
    return env.Detect('AR')
