function [] = build(target)

build_root = '../../';
disp('Starting simulink code generation');

slbuild('sandbox_application');
%slbuild('test');

disp(['Starting build for target: ' target]);
% Run build.bat for UCON
current_dir = pwd;
try
    cd(build_root);

    if target == "all"
        target_arch = "all";
    elseif target == "UCU"
        target_arch = "aarch64";
    elseif target == "PC_32bit"
        target_arch = "x86";
    elseif target == "PC 64bit"
        target_arch = "x86_64";
    else
        disp(['Target ' target ' is not supported'])
    end

catch
    disp('Error');
end

system(strcat('build --architecture=', target_arch));
disp('Done');

cd(current_dir);

return

