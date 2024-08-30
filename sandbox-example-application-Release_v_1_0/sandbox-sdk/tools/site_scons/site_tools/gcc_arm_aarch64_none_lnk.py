#*****************************************************************************************************************************
#   Scons: Linker settings for GCC ARM aarch64
#*****************************************************************************************************************************
import SCons.Tool
from TempFileMungeABB import TempFileMungeABB

def generate(env):
    """
    Setup Default 'link'
    """
    SCons.Tool.Tool('link').generate(env)

    """
    Change Variables for GCC ARM Embedded tools
    """
    # Options:
    #     -Xlinker = Pass parameter to ld not g++
    #     -lstdc++ = Link against stdc++ library that GCC system supplies.
    #     -lc = Link against c library that GCC system supplies.
    #     -( = opens group of objects to be linked so that order doesn't matter. Same as --start-group
    #     -) = closes group of objects to be linked where order doesn't matter. Same as --end-group
    #
    #		Within _LINKCOM objcopy is also called to generate flat raw bin file out of elf file.
    env.AppendENVPath('PATH', env['compiler_bin'], delete_existing=0)

    env['LINK_TEMPFILE'] = TempFileMungeABB
    env['LINK'] = 'aarch64-none-elf-g++.exe'

    ## ToDo: move these somewhere
    env['ELFSIZE'] = 'aarch64-none-elf-size.exe'
    env['ELFSIZEFLAGS'] = '-B '

    env['BINDUMP'] = 'aarch64-none-elf-objcopy.exe'
    env['BINDUMPFLAGS'] = '-O binary -I elf32-little  '
    ##

    env['_LINKCOM'] = '$($LINK_WRAPPER$) $LINK $LINKFLAGS $_LIBDIRFLAGS $_LIBFLAGS -Xlinker -( -Xlinker ${SOURCES.abspath} -Xlinker -lgcc -Xlinker -lm -Xlinker -lstdc++ -Xlinker -lc -Xlinker -) -o ${TARGETS[0].abspath} -Xlinker -Map=${TARGETS[1].abspath}'

    if env.GetOption('verbose_option'):
        env.Append(_LINKCOM=' -Xlinker --print-memory-usage')
    else:
        env['LINKCOMSTR'] = "Linking ${TARGET}"

    env['LINKCOM'] = "${LINK_TEMPFILE('$_LINKCOM','@')}"
    env['LINKFLAGS'] = ''
    env['LIBS'] = []
    env['LIBLINKPREFIX'] = ''
    env['LIBLINKSUFFIX'] = '.lib'
    env['LIBPATH'] = []
    env['LIBDIRPREFIX'] = '-L'
    env['LIBDIRSUFFIX'] = ''
    env['PROGSUFFIX'] = '.axf'

def exists(env):
    return True
