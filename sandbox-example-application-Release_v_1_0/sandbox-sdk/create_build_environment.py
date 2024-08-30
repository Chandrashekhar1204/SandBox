
Import('compiler_dir sdk_dir architecture')
compiler_root_dir = compiler_dir
import sys
import os
import shutil

def rename_long_path_to_short_path(long_path, short_path, num_tries):
    # if short path already exists, remove it
    if os.path.exists(short_path):
        print(f"removing the existing folder at {short_path}")
        shutil.rmtree(short_path)

    # try multiple times because it could fail due to windows file locks e.g. triggered by antivirus
    for i in range(num_tries):
        try:
            os.rename(long_path, short_path)
            break
        except Exception as e:
            if i == num_tries - 1:
                print(f"An error occurred while renaming the compiler path: {e}", file=sys.stderr)
                print(f"please rename manually from {long_path} to {short_path} and try again.", file=sys.stderr)
                sys.exit(-1)
            else:
                print("An error occurred while renaming the compiler path, trying again...")
                continue

def download_extract_zip_file(zip_url, download_path, tool_name_from_archive, destination_folder, tool_name_in_destination, tar_file = False):

    os.makedirs(destination_folder, exist_ok=True)

    if not os.path.exists(download_path):
        print(f'Downloading compiler from {zip_url}')
        import urllib.request
        proxies = urllib.request.getproxies()
        proxy_handler = urllib.request.ProxyHandler(proxies)
        opener = urllib.request.build_opener(proxy_handler)
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(zip_url, download_path)

    # get a temporary folder location to extract the zip file to
    import tempfile
    temp_dir = tempfile.gettempdir()

    print(f'Extracting to a temporary location ({temp_dir})')
    if tar_file:
        import tarfile
        with tarfile.open(download_path, 'r') as file:
            file.extractall(temp_dir)
    else:
        import zipfile
        with zipfile.ZipFile(download_path, 'r') as file:
            file.extractall(temp_dir)

    num_tries = 3

    print(f"renaming the extracted folder from {temp_dir}/{tool_name_from_archive} to {temp_dir}/{tool_name_in_destination}")
    rename_long_path_to_short_path(f"{temp_dir}/{tool_name_from_archive}", f"{temp_dir}/{tool_name_in_destination}", num_tries=num_tries)

    # move the extracted folder to the desired location
    print(f"moving the extracted folder from {temp_dir}/{tool_name_in_destination} to {destination_folder}")
    # try multiple times because it could fail due to windows file locks e.g. triggered by antivirus
    for i in range(num_tries):
        try:
            shutil.move(f"{temp_dir}/{tool_name_in_destination}", destination_folder)
            break
        except Exception as e:
            if i == num_tries - 1:
                print(f"An error occurred while moving the compiler folder: {e}", file=sys.stderr)
                print(f"please move manually from {temp_dir}/{tool_name_in_destination} to {destination_folder} and try again.", file=sys.stderr)
                sys.exit(-1)
            else:
                print("An error occurred while moving the compiler folder, trying again...")
                continue

def check_compiler_and_install_if_needed(
        compiler_path_short,
        compiler_path_old, 
        auto_install, 
        zip_url, 
        zip_path, 
        tool_name_in_archive, 
        compiler_root_dir, 
        tool_name_destination,
        compiler_binary_relative_path):
    if not os.path.exists(f"{compiler_path_short}/{compiler_binary_relative_path}"):
        # check if long path exists and rename it to short path
        if os.path.exists(compiler_path_old):
            rename_long_path_to_short_path(compiler_path_old, compiler_path_short, num_tries=3)
        else:
            install_question = f"compiler could not be found in {compiler_path_short}, do you want to install it now? [y/n] "
            if auto_install or input(install_question).strip().lower() == 'y':
                download_extract_zip_file(zip_url, zip_path, tool_name_in_archive, compiler_root_dir, tool_name_destination, tar_file=False)
            else:
                sys.exit(-1)


import SCons.Script as SC    # for AddOption and Help
auto_install = SC.GetOption('auto_install')
if architecture == 'x86':

    zip_url = "https://github.com/brechtsanders/winlibs_mingw/releases/download/12.2.0-16.0.0-10.0.0-msvcrt-r5/winlibs-i686-posix-dwarf-gcc-12.2.0-mingw-w64msvcrt-10.0.0-r5.zip"
    zip_path = f"{compiler_root_dir}/winlibs-i686-posix-dwarf-gcc-12.2.0-mingw-w64msvcrt-10.0.0-r5.zip"
    tool_name_in_archive = "mingw32"
    tool_name_destination = "mingw-i686-12.2.0"
    compiler_path_old = f"{compiler_root_dir}/winlibs-i686-posix-dwarf-gcc-12.2.0-mingw-w64msvcrt-10.0.0-r5/{tool_name_in_archive}"   # from previous SDK versions
    compiler_path_short = f"{compiler_root_dir}/{tool_name_destination}"
    
    check_compiler_and_install_if_needed(
        compiler_path_short = compiler_path_short,
        compiler_path_old = compiler_path_old,
        auto_install = auto_install,
        zip_url = zip_url,
        zip_path = zip_path,
        tool_name_in_archive = tool_name_in_archive,
        compiler_root_dir = compiler_root_dir,
        tool_name_destination = tool_name_destination,
        compiler_binary_relative_path = 'bin/g++.exe',
        )
    
    print(f"using MinGW from: {compiler_path_short}")
    
    import mingw_w64_i686_gcc_cfg
    mingw_w64_i686 = mingw_w64_i686_gcc_cfg.Config(path=compiler_path_short)
    compilers = \
    [
        mingw_w64_i686.c_cfg,
        mingw_w64_i686.cpp_cfg,
        mingw_w64_i686.asm_cfg,
        mingw_w64_i686.ar_cfg,
        mingw_w64_i686.lnk_cfg,
        mingw_w64_i686.version_info
    ]
    compiler_bin=mingw_w64_i686.bin
    ccflags = []
    linkflags = []

elif architecture == 'x86_64':

    zip_url = "https://github.com/brechtsanders/winlibs_mingw/releases/download/11.3.0-14.0.3-10.0.0-msvcrt-r3/winlibs-x86_64-posix-seh-gcc-11.3.0-mingw-w64msvcrt-10.0.0-r3.zip"
    zip_path = f"{compiler_root_dir}/winlibs-x86_64-posix-seh-gcc-11.3.0-mingw-w64msvcrt-10.0.0-r3.zip"
    tool_name_in_archive = "mingw64"
    tool_name_destination = "mingw-x86_64-12.2.0"
    compiler_path_old = f"{compiler_root_dir}/winlibs-x86_64-posix-seh-gcc-11.3.0-mingw-w64msvcrt-10.0.0-r3/{tool_name_in_archive}"   # from previous SDK versions
    compiler_path_short = f"{compiler_root_dir}/{tool_name_destination}"
    
    check_compiler_and_install_if_needed(
        compiler_path_short = compiler_path_short,
        compiler_path_old = compiler_path_old,
        auto_install = auto_install,
        zip_url = zip_url,
        zip_path = zip_path,
        tool_name_in_archive = tool_name_in_archive,
        compiler_root_dir = compiler_root_dir,
        tool_name_destination = tool_name_destination,
        compiler_binary_relative_path = 'bin/g++.exe',
        )
    
    print(f"using MinGW from: {compiler_path_short}")
    
    import mingw_w64_gcc_cfg
    mingw_w64_x86_64 = mingw_w64_gcc_cfg.Config(target_architecture='x86_64', path=compiler_path_short)
    compilers = \
    [
        mingw_w64_x86_64.c_cfg,
        mingw_w64_x86_64.cpp_cfg,
        mingw_w64_x86_64.asm_cfg,
        mingw_w64_x86_64.ar_cfg,
        mingw_w64_x86_64.lnk_cfg,
        mingw_w64_x86_64.version_info
    ]
    compiler_bin=mingw_w64_x86_64.bin
    ccflags = []
    linkflags = []

elif architecture == 'aarch64':
    
    tool_name_in_archive = "arm-gnu-toolchain-12.2.rel1-mingw-w64-i686-aarch64-none-elf"
    zip_url = f"https://developer.arm.com/-/media/Files/downloads/gnu/12.2.rel1/binrel/{tool_name_in_archive}.zip?rev=554fdb28819040f983ab13363612752a&hash=6A43A615E4AC06EA8F8A82E648038C4B50AF684C"
    zip_path = f"{compiler_root_dir}/{tool_name_in_archive}.zip"
    tool_name_destination = "mingw-aarch64-12.2.rel1"
    compiler_path_old = f"{compiler_root_dir}/{tool_name_in_archive}"   # from previous SDK versions
    compiler_path_short = f"{compiler_root_dir}/{tool_name_destination}"
    
    check_compiler_and_install_if_needed(
        compiler_path_short = compiler_path_short,
        compiler_path_old = compiler_path_old,
        auto_install = auto_install,
        zip_url = zip_url,
        zip_path = zip_path,
        tool_name_in_archive = tool_name_in_archive,
        compiler_root_dir = compiler_root_dir,
        tool_name_destination = tool_name_destination,
        compiler_binary_relative_path = 'bin/aarch64-none-elf-gcc.exe',
        )

    print(f"using GCC-arm from: {compiler_path_short}")
    
    import gcc_arm_aarch64_cfg as gcc_arm64_cfg
    gcc_arm64 = gcc_arm64_cfg.Config(path=compiler_path_short)
    compilers = \
    [
        gcc_arm64.c_cfg,
        gcc_arm64.cpp_cfg,
        gcc_arm64.asm_cfg,
        gcc_arm64.ar_cfg,
        gcc_arm64.lnk_cfg,
        gcc_arm64.version_info
    ]
    compiler_bin=gcc_arm64.bin
    ccflags = [
        '-march=armv8-a+crypto',
        '-mtune=cortex-a53',
        '-pipe',                          # Use pipes instead of temporary files while compiling
        '-c',                             # Compile only
        '-fno-builtin',                   # Do not use GCC's builtin C standrd library functions (i.e use libc's)
        '-fno-exceptions',                # Don't generate the extra code needed to propagate exceptions
    ]
    linkflags = [
        '-nostartfiles',
        '-march=armv8-a+crypto',
        '-mcpu=cortex-a53',
        '-Xlinker', '--no-warn-rwx-segments',
    ]

else:
    print(f'error: architecture {architecture} not supported')
    sys.exit(-1)

# check if absolute path of parent directory (application reporitory root) is less than 99 characters and print a warning if not
import platform
if platform.system() == 'Windows':
    if len(Dir('.').abspath) > 110:
        print(f"!!!!! Warning: the SDK directory is located in a path which is longer than 110 characters. Due to a windows limitation (of MAX_PATH) this might cause problems resulting in failing build.")

env = Environment(
    cgt = 'gcc_arm_none_aarch64',
    compiler_bin=compiler_bin,
    tools = compilers,
    TARGET_ARCH = architecture,
    CPPPATH=[],
    CPPDEFINES=[],
    CCFLAGS=[
        '-g',
        '-ggdb',
        '-Og',
        # '-fno-builtin',
        '-fno-use-cxa-atexit', # needed to avoid undefined reference to __dso_handle errors
        ccflags,
    ],
    CXXFLAGS=[
        '-std=c++17',
    ],
    LINKFLAGS=[
        '-static-libgcc',
        '-static-libstdc++',
        '-static',
        # '-Bsymbolic-functions',
        linkflags,
    ],
)

include_dirs = \
[
    'application_api',
    f'application_api/{architecture}',
]
env.Append(CPPPATH=include_dirs)

Return('env')