#*****************************************************************************************************************************
#
#   Scons: C compiler settings for MinGW
#
#*****************************************************************************************************************************

import SCons.Tool

from TempFileMungeABB import TempFileMungeABB

def generate(env):
    """
    Setup Default 'cc'
    """
    SCons.Tool.Tool('cc').generate(env)

    #---------------------------------------------------------------------------------------------------------------------------
    # Options:
    #     -c = only compile, do not link (outputs object file)
    #     -o = output
    #
    #     This configuration creates object files with the Windows suffix '.obj' rather than Linux's '.o'.
    #---------------------------------------------------------------------------------------------------------------------------
    env.AppendENVPath('PATH', env['compiler_bin'], delete_existing=0)

    env['CC_TEMPFILE'] = TempFileMungeABB
    env['CC'] = 'gcc.exe'
    env['_CCCOM'] = '$($CC_WRAPPER$) $CC $CCFLAGS $CFLAGS $_CCCOMCOM -c ${SOURCE.abspath} -o ${TARGET.abspath}'
    env['CCCOM'] = "${CC_TEMPFILE('$_CCCOM','@')}"

    # this makes the choice between showing the full compiler command line or just filename
    # if not env.GetOption('verbose_option'):
    #     env['CCCOMSTR'] = "${SOURCE.abspath}"

    env['OBJSUFFIX'] = '.obj'
    env['CPPPATH'] = []
    env['CPPDEFINES'] = []
    env['INCPREFIX'] = '-I '
    env['INCSUFFIX'] = ''

def exists(env):
    return env.Detect('CC')
