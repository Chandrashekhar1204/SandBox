#*****************************************************************************************************************************
#
#   Scons: Linker settings for MinGW
#
#*****************************************************************************************************************************

import SCons.Tool

from TempFileMungeABB import TempFileMungeABB

def generate(env):
    """
    Setup Default 'link'
    """
    SCons.Tool.Tool('link').generate(env)

    #---------------------------------------------------------------------------------------------------------------------------
    # Options:
    #     -Xlinker = Pass parameter to ld not g++
    #     -lstdc++ = Link against stdc++ library that GCC system supplies.
    #     -( = opens group of objects to be linked so that order doesn't matter. Same as --start-group
    #     -) = closes group of objects to be linked where order doesn't matter. Same as --end-group
    #
    #		Within _LINKCOM the linker is instructed to generate a map file in the build directory. It is
    #     also given a custom script (custom.lnk) which positions the event system sections correctly in
    #     memory.
    #
    #     custom.lnk is a copy of the internal MinGW linker script with a single line added to include events.lnk.
    #     events.lnk is where the event system section layout is actually specified. More customizations can be made
    #     by modifying this file or adding more files and including them in custom.lnk.
    #---------------------------------------------------------------------------------------------------------------------------
    env.AppendENVPath('PATH', env['compiler_bin'], delete_existing=0)

    env['LINK_TEMPFILE'] = TempFileMungeABB
    env['LINK'] = 'g++.exe'
    env['_LINKCOM'] = '$($LINK_KWRAPPER$) $LINK -o ${TARGETS[0].abspath} $LINKFLAGS -Wl,-T,custom_x64.lnk $_LIBDIRFLAGS -Lcommon_scripts/site_scons/cgt_sysfiles/mingw32 -Xlinker -Map=${TARGETS[1].abspath} -Xlinker -( $_LIBFLAGS $LINKED_LIBS -lstdc++ ${SOURCES.abspath} -Xlinker -)'
    env['LINKCOM'] = "${LINK_TEMPFILE('$_LINKCOM','@')}"

    # use built-in SHLINKCOM, but wrap using TEMPFILE if needed
    env['_SHLINKCOM'] = env['SHLINKCOM']
    env['SHLINKCOM'] = "${LINK_TEMPFILE('$_SHLINKCOM','@')}"

    if not env.GetOption('verbose_option'):
        env['LINKCOMSTR'] = "${TARGET.abspath}"

    env['LINKFLAGS'] = ''
    env['LIBS'] = []
    env['LIBLINKPREFIX'] = '-l'
    env['LIBLINKSUFFIX'] = ''

    env['LIBPATH'] = []
    env['LIBDIRPREFIX'] = '-L'
    env['LIBDIRSUFFIX'] = ''
    env['PROGSUFFIX'] = '.exe'

def exists(env):
    return env.Detect('SHLINK')
