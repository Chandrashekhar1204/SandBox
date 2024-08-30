
Import('env lp_name build_dir tools_dir program')

lp_update_exe = f'{tools_dir}/UnicosLoader/LPUpdate.exe'

sandbox_out_stripped = f'{build_dir}/sandbox_application_stripped.elf'
empty_lp = f'{tools_dir}/ucon/empty.lp'
sandbox_lp = f'{build_dir}/{lp_name}'
    


def add_builders(env):
    def update_lp_file(target, source, env, for_signature):
        lpc_data = f"""\
LpOpen(@"{target[0].name}");
LpUpdateFile(@"{source[1].name}",@"\sandbox\sandbox_application.elf", 2);
LpClose();
"""
    
        tmpdir = str(target[0].dir.abspath)
        actions = []
        lpc_file = target[0].dir.abspath + '/temp.lpc'

        # generate tmpdir if it doesn't exist
        import os
        if not os.path.exists(tmpdir):
            os.makedirs(tmpdir)
        
        # write LPC file 
        import sys
        try:
            with open(lpc_file, 'w', encoding='utf-8') as file:
                file.write(lpc_data)
        except Exception as error_info:
            print(f'Error: {error_info}', file = sys.stderr)
            sys.exit(1)

        lp_update_abspath = env.File(lp_update_exe).abspath
        actions = []
        actions.append(f'copy /Y \"{source[0].abspath}\" \"{target[0].abspath}\"')

        action_str = f'pushd {tmpdir} && \"{lp_update_abspath}\" -d -f \"{lpc_file}\" && popd'
        actions.append(action_str)
        return actions

    lp_update = Builder(
        generator = update_lp_file,
    )
    env.Append(BUILDERS={'LP_Update': lp_update})

add_builders(env)


# strip debug symbols to keep LP size small
env.Command(target=sandbox_out_stripped, source=program, 
    action=f'aarch64-none-elf-strip.exe -s $SOURCES -o $TARGET')

application_lp = env.LP_Update(target=sandbox_lp, source=[empty_lp, sandbox_out_stripped])

Return('application_lp')