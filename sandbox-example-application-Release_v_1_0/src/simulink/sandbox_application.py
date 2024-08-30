
# folder where Matlab Simulink generated code is located
# NOTE: this folder will be added to the include path (CPPPATH) and
# all .cpp files (except rtw_main.cpp) in this folder will be added to the build
#simulink_code_folder = 'sandbox_application_grt_rtw'
simulink_code_folder = 'sandbox_application_grt_rtw'


Import('env')

import os
if os.environ.get("C:\Program Files\MATLAB\R2020b"):
    matlab_root = os.environ.get("C:\Program Files\MATLAB\R2020b")
else:
    matlab_root = "C:\Program Files\MATLAB\R2020b"

source_nodes = []
import os
if os.path.exists(matlab_root):
    
    print(f"using MATLAB from: {matlab_root}")

    # add directories to include path for compiler to find header files (.h)
    include_dirs = \
    [
        env.Dir(simulink_code_folder).abspath, # TODO: fix
        matlab_root + '/extern/include',
        matlab_root + '/simulink/include',
    ]
    env.Append(CPPPATH=include_dirs)
    
    sources = Glob('*.cpp') + Glob('**/*.cpp')

    for source in sources:
        # exclude rtw_main.cpp, since it's not needed
        if not 'rtw_main.cpp' in source.abspath:
            source_nodes.append(env.File(source).abspath)
else:
    print(f"MATLAB_HOME environment variable not set and Matlab not found in {matlab_root}, skipping build of simulink application")

Return('source_nodes')