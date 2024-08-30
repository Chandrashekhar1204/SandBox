#*****************************************************************************************************************************
#
#   Scons: Archiver settings for MinGW
#
#*****************************************************************************************************************************

import SCons.Tool

from TempFileMungeABB import TempFileMungeABB

def generate(env):
    """
    Setup Default 'ar'
    """
    SCons.Tool.Tool('ar').generate(env)

    # Options:
    #     -cr = Create archive
    #     Even though this is a GCC toolchain, the archiver creates libraries according
    #     to the Windows naming convention (libraryName.lib) rather than Linux (libLibraryName.a).
    #     This is on purpose to simplify the SCons build scripts (there are some hardcoded library names).
    env.AppendENVPath('PATH', env['compiler_bin'], delete_existing=0)

    env['AR_TEMPFILE'] = TempFileMungeABB
    env['AR'] = 'ar.exe'
    env['_ARCOM'] = '$($AR_WRAPPER$) $AR cr $ARFLAGS $TARGET $SOURCES'
    env['ARCOM'] = "${AR_TEMPFILE('$_ARCOM','@')}"

    # if not env.GetOption('verbose_option'):
    #     env['ARCOMSTR'] = "${TARGET.abspath}"

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
