# Readme: Sandbox SDK
This repository is meant to provide a light-weight SDK which can be used to easily create & develop own Sandbox applications.

The Sandbox is available in some UNICOS based products, currently ACS880, ACS6080 & TUREL for pilot purposes.

**NOTE:** Example application source code is located in a separate [repository](https://codebits.abb.com/drives-sw-common/sandbox-example-application).

## Table of contents
- [Changelog](#changelog)
- [Installation / Requirements](#installation--requirements)
- [How to develop applications](#how-to-develop-applications)
- [Build sandbox_application](#build-sandbox_application)
- [Execute Sandbox application](#execute-sandbox-application)
- [Debugging](#debugging)
- [Workflow for developing a Matlab Simulink application](#workflow-for-developing-a-matlab-simulink-application)

## Changelog
See [CHANGELOG.md](CHANGELOG.md)

## Installation / Requirements
### Python
Python 3 with pip support should be installed and available from PATH.
Required Python packages will automatically be fetched and installed using pip.

### PC and UCON compilers
Before building the build scripts will automatically check if the required compilers are available.
If not the user will be asked if installation should be done automatically.

### Proxy settings
In case a proxy is needed for the SDK to download the required tools, please configure it by settings the environment variables ```HTTP_PROXY``` and ```HTTPS_PROXY``` to the proxy url, e.g.:
- ```HTTP_PROXY=http://proxy.my-organization.com:8080```
- ```HTTPS_PROXY=http://proxy.my-organization.com:8080```

***NOTE:*** make sure to replace ```http://proxy.my-organization.com:8080``` with your orginations' proxy address. 

### Optional: Matlab
if you want to build the simulink application:
- Install Matlab, e.g. 2019b
- set **MATLAB_HOME** environment variable to your MATLAB installation folder (e.g. ```C:\Programs\MATLAB\R2020b```)

### Sandbox enabled drive FW
The sandbox engine is currently available on
| Product     | UCU target    | PC target                           | PC target architecture          |
| ---         | ---           | ---                                 | ---                             |
| ACS880 INU  | YINLX         | YINVB                               | 32bit/x86                       |
| ACS880 LSU  | YISLX         | YISVB                               | 32bit/x86                       |
| AC6080      | LAAAB         | Jungfrau_Fast_Simulator_2           | 64bit/x86_64                    |
| TUREL       | TUREL_UCON_22 | TUREL_UCON_22_VD                    | both 32bit and 64bit available  |

## How to develop applications
### C++ application
#### [C++ API reference](application_api/API_cpp.md)
- Open [src/c++/sandbox_application.cpp](src/c++/sandbox_application.cpp)
- By default 5 application tasks are registered (see application_init_user())
  - T1 .. T4: cyclic tasks running at 250us, 500us, 2ms, 10ms intervals
    - These tasks are real-time and have strict requirements in terms of execution time. They are not allowed to take longer than their cycle time to finish (including interruptions).
  - Background: acyclic task running with low priority
    - This task is meant for longer calculations which can take up to 1s of execution time.
- The default application tasks can be extended with additional functionality
- The application can interface with the drive FW using API functions
  - For details, please see [application_api/API_cpp.md](application_api/API_cpp.md)
- After modifying the application, proceed with [build application](#build-sandbox_application)

### Matlab Simulink (ML/SL)
- Open [src/simulink/sandbox_application.slx](src/simulink/sandbox_application.slx) and modify the model
- The default application contains 4 Tasks which are implemented as subsystems with different cycle times
  - The task cycles are 250us, 500us, 2ms, 10ms
  - The subsystems can be extended with additional functionality
  - NOTE: these tasks are real-time and have strict requirements in terms of execution time. They are not allowed to take longer than their cycle time to finish (including interruptions).
- Generate code from Simulink model using Simulink Coder
  - For details, please see [doc/README_Simulink.md](doc/README_Simulink.md#quick-start)
  - The Simulink application can interface with the drive FW using Simulink library blocks
    - For details, please see [doc/API_simulink.md](doc/API_simulink.md)
- Build the Simulink application as described [here](#build-sandbox_application)

For more information on how to modify, generate code from Simulink and integrate Simulink code into the Sandbox, please see [doc/README_Simulink.md](doc/README_Simulink.md).
### Mixed C++ and ML/SL
It is also possible to develop a mixed application with code both in C++ and Simulink.
For this purpose the Simulink example application can be extended with C++ code by modifying [src/simulink/sandbox_application.cpp](src/simulink/sandbox_application.cpp).
That way both the functionality from the Simulink model and the C++ code will be included in the Simulink application.

## Build sandbox_application
There's different build examples and build configurations which can be selected.
Certain tools (MINGW, UCU arm compiler, MATLAB) are automatically detected using environment variables.

### Build from console
Use build.bat from the SDK root folder:
- ```build.bat [--architecture={x86, x86_64, aarch64}] [application]```
- architecture:
  - x86: 32bit PC target using Virtual Drive (e.g. ACS880, TUREL_VDWIN)
  - x86_64: 64bit PC target, e.g. ACS6080 Fast Simulator
  - aarch64: UCU aarch64 target
  - [not specified]: build for x86 by default
- application (optional): select which example application to build
  - **c++**: build c++ example application from src/c++ folder
  - **simulink**: build simulink code generated example application from src/simulink folder
  - [empty]: build all supported example applications

### Build only C++ or Simulink example application
- Execute ```build.bat c++``` to build only the C++ example application
- Execute ```build.bat simulink``` to build only the simulink example application

### Build artifacts
#### x86 and x86_64 PC target
- if everything works as expected, the application should be generated in the build folders
  - ```build/c++/x86/sandbox_application.dll``` (or x86_64 instead of x86)
  - ```build/simulink/x86/sandbox_application.dll``` (or x86_64 instead of x86)
- those dll files can be used together with a PC simulator (ACS880 Virtual Drive, ACS6080 Jungfrau Fast Simulator2, ...) as sandbox applications

#### aarch64 UCU target
- if everything works as expected, the application should be generated in the build folders
  - ```build/c++/aarch64/sandbox_application.lp```
  - ```build/simulink/aarch64/sandbox_application.lp```
- builds loading package (.lp) files which can be used (e.g. by DriveLoader) to load the application to the UCU

## Execute Sandbox application
### PC target
Running the application is possible with any PC build of a UNICOS based product which has the Sandbox runtime enabled. The following steps describe how start a PC simulator with an application loaded:
- Build the application using the SDK for the correct PC architecture. See the table [here](#sandbox-enabled-drive-fw) for details about which PC simulators are built for what architecture.
- Copy the generated sandbox_application.dll to the same folder as where the PC simulator executable (e.g. TUREL_VDWIN_01.exe) is located
- Start the simulator e.g. using
  - ```TUREL_VDWIN_01.exe /wcf /flash flash.vd```
- Connect using Drive Composer
  - change parameter "96.90 Enable Sandbox applications" to "Enable"
  - check that the sandbox_application output signals (e.g. 47.01) are showing changing values

### UCU target
In order to run Sandbox applications on the UCU target, a FW (e.g. ACS880INU YINLX) with Sandbox support enabled is needed.
- Load ```sandbox_application.lp``` from ```build/..application_name../aarch64/``` using Drive firmware loader (integrated to Drive Composer under Tools)
- Enable execution of Sandbox application by setting parameter **96.90 Enable Sandbox application** to **Enable**
  - ***NOTE:*** in some products, this parameter might be protected by a pilot access level passcode
- for **reloading** a newly loaded application, first set the parameter to _Disable_ and then _Enable_

## Debugging
### Application exit reason
If the application crashes or exits unexpectedly, an event "**0xB68C: Sandbox application diagnostics**" will be created in the event log. The AUX code encodes the reason for the exit:
|AUX code|Description|Core dump created|
|--------|-----------|--------------------|
|0|Application status OK. |No|
|1|Application has ended/aborted. |No|
|2|Application is incompatible with Sandbox API version. NOTE: application API major version and sandbox engine API major version must be equal and application API minor version must be smaller or equal to sandbox engine API minor version. |No|
|3|Application has triggered a synchronous exception and has been stopped. |Yes|
|4|During exception of application an asynchronous (SError/vSError) exception has occured. Application has been stopped. |Yes|
|5|Application has issued an invalid supervisor call and has been stopped. |Yes|
|6|Application has initiated an invalid system call. |Yes|
|7|Application took too long to execute and was aborted. |No|

In case a core dump is created, it can be found on the SD card under ```/sandbox/YYYYMMDD/hhmmss.txt``` (YYYY: year, MM: month, DD: day, hh: hour, mm: minute, ss: second). It can be analyzed to identify reason and location of an exception. 

## Workflow for developing a Matlab Simulink application
See [here](doc/README_Simulink.md)