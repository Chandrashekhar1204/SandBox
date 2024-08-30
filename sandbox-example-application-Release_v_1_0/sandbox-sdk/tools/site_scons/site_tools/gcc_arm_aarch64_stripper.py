# SCons builder for stripping .elf file to remove symbols
import SCons.Builder


def generate(env):
    env['ELFSTRIPPER'] = env.File(f'{env["compiler_bin"]}/aarch64-none-elf-strip.exe')

    def stripelffile_gen(source, target, env, for_signature):

        actions = []
        actions.append(
            # pylint: disable=consider-using-f-string
            'pushd %s && ${ELFSTRIPPER.abspath} -s --strip-unneeded %s -o %s && popd' % (target[0].dir, source[0].abspath, target[0].name)
        )
        return actions

    stripelffile_bld = SCons.Builder.Builder(generator=stripelffile_gen)
    env.Append(BUILDERS={'StripElfFile' : stripelffile_bld})


def exists(env):
    return True
