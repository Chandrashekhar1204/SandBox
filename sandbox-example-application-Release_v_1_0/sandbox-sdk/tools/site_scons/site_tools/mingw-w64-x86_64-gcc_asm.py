#*****************************************************************************************************************************
#
#   Scons: Assembler settings for MinGW
#
#*****************************************************************************************************************************

import SCons.Tool

from TempFileMungeABB import TempFileMungeABB

def generate(env):
    """
    Setup Default 'as'
    """
    SCons.Tool.Tool('as').generate(env)

    #---------------------------------------------------------------------------------------------------------------------------
    # Options:
    #     $_CCCOMCOM = Use same includes and defines like C compiler does since we don't call -as implicitly.
    #     -o = output object file
    #
    #     This configuration creates object files with the Windows suffix '.obj' rather than Linux's '.o'.
    #---------------------------------------------------------------------------------------------------------------------------
    env.AppendENVPath('PATH', env['compiler_bin'], delete_existing=0)

    env['AS_TEMPFILE'] = TempFileMungeABB
    env['AS'] = 'gcc.exe'
    env['_ASCOM'] = '$($AS_WRAPPER$) $AS $_CCCOMCOM $AFLAGS $_ASCOM ${SOURCE.abspath} -o ${TARGET.abspath}'
    env['ASCOM'] = "${AS_TEMPFILE('$_ASCOM','@')}"

    # this makes the choice between showing the full compiler command line or just filename
    if not env.GetOption('verbose_option'):
        env['ASCOMSTR'] = "${SOURCE.abspath}"

    env['OBJSUFFIX'] = '.obj'
    env['CPPPATH'] = []
    env['CPPDEFINES'] = []
    env['INCPREFIX'] = '-I '
    env['INCSUFFIX'] = ''

def exists(env):
    return env.Detect('AS')
