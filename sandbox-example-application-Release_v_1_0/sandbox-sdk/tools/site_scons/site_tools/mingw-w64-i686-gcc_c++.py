#*****************************************************************************************************************************
#
#   Scons: C++ compiler settings for MinGW
#
#*****************************************************************************************************************************

import SCons.Tool

from TempFileMungeABB import TempFileMungeABB

def generate(env):
    """
    Setup Default "c++"
    """
    SCons.Tool.Tool('c++').generate(env)

    #---------------------------------------------------------------------------------------------------------------------------
    # Options:
    #     -c = only compile, do not link (outputs object file)
    #     -o = output
    #
    #     This configuration creates object files with the Windows suffix '.obj' rather than Linux's '.o'.
    #---------------------------------------------------------------------------------------------------------------------------
    env.AppendENVPath('PATH', env['compiler_bin'], delete_existing=0)

    env['CXX_TEMPFILE'] = TempFileMungeABB
    env['CXX'] = 'g++.exe'
    env['_CXXCOM'] = '$($CXX_WRAPPER$) $CXX $CCFLAGS $CXXFLAGS $_CCCOMCOM -c ${SOURCE.abspath} -o ${TARGET.abspath}'
    env['CXXCOM'] = "${CXX_TEMPFILE('$_CXXCOM','@')}"

    # this makes the choice between showing the full compiler command line or just filename
    # if not env.GetOption('verbose_option'):
    #     env['CXXCOMSTR'] = "${SOURCE.abspath}"

    env['OBJSUFFIX'] = '.obj'
    env['CPPPATH'] = []
    env['CPPDEFINES'] = []
    env['INCPREFIX'] = '-I '
    env['INCSUFFIX'] = ''

    # Create a resource builder, since we are targetting Windows
    # The MinGW linker does not accept .res files, so the resource suffix is set to .obj instead
    env['RC'] = 'windres.exe'
    env['RCCOM'] = '$RC $SOURCE $TARGET'
    env['RCCOMSTR'] = '$RCCOM'
    env['BUILDERS']['RES'] = SCons.Builder.Builder(action=SCons.Action.Action('$RCCOM', '$RCCOMSTR'),
                                                   src_suffix='.rc',
                                                   suffix='.obj')

def exists(env):
    return env.Detect('CXX')
