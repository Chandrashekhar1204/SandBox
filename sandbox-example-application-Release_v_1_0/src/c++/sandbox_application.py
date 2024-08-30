Import('env')

# add directories to include path for compiler to find header files (.h)
include_dirs = \
[
]
env.Append(CPPPATH=include_dirs)

# automatically build all .cpp files in this folder
source_nodes = []
for source in Glob('**.cpp'):
    source_nodes.append(env.File(source).abspath)

Return('source_nodes')