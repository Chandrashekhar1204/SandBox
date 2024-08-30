
# API versioning
The sandbox application API is versioned using ```major.minor``` version numbers:
- Changes in ```minor``` version number indicate that new features were added, but backwards compatibility is retained
- Changes in ```major``` version number indicate backwards compatibility breakig changes

## Compability table
| Major version         | Minor version         | Compatible    | Comments                                                              |
| -                     | -                     | -             | -                                                                     |
| Engine == Application | Engine >= Application | yes           |                                                                       |
| Engine == Application | Engine < Application  | no            | Engine might be missing some features required by the application     |
| Engine != Application | *                     | no            | breaking changes in the API between Engine and Application            |

Terms:
- *Engine* API version
  - API version supported by the engine shipped with the product FW.
- *Application* API version
  - API version used when developing the application.

# Changelog
Below sections list changes & fixes to the SDK and application API.

## 1.0
### Changes
- SDK
  - Change in repository structure: There's a separate repository for the example application code now located [here](https://codebits.abb.com/drives-sw-common/sandbox-example-application)
    - The SDK repository only contains the tools, build scripts & API files for building applcations
    - This makes it easier to create own application repositories using the SDK repository as a submoudule
  - Updated compilers for UCON and PC (both based on GCC 12). The compilers don't have to be installed manually anymore, but can be installed automatically during building.
  - Documentation improvements on C++ API, see [here](application_api/API_cpp.md)
  - Documentation improvements on usage with Matlab Simulink, see [here](doc/README_Simulink.md)
  - Simplified example C++ and Matlab Simulink application
- Application API
  - Sandbox applications are now located in a different memory region. This is a preparation for supporting multiple sandbox applications and breaks backwards compatibility with API version 0.x

## 0.3
### Changes
- Application API
  - Application ID, Version (major.minor.build.patch) and description can now be registered and will be shown in parameters in group 7.
  - Fixed problems with dynamic memory allocation & deallocation not being thread-safe. NOTE: allocating dynamic memory on fast cyclic tasks can lead to CPU overload trips due to high time consumption depending on the amount and structure of memory to be allocated and other aspects.

## 0.2
### Changes
- Application API
  - When loading applications, the API version of the engine is compared with the application lib version used for building the application. If those versions are incompatible, the application will not be loaded.
  - Added support for reading pointer parameters, see [here](application_api/API_cpp.md#read_pointer_parameter_unconverted)

## 0.1
### Changes
- Application API
  - register_cyclic_task: register function as cyclic task (to be called cyclically)
  - register_background_task: register function as background task (to be called aperiodically)
  - read_parameter_float: read parameter as floating point value
  - read_parameter_int32: read parameter as int32 value
  - write_parameter_float: write parameter as floating point value 
  - write_parameter_int32: write parameter as int32 value 
- Example applications
  - C++ example application
  - Simulink example application
- Target & compiler support
  - aarch64: used for UCU control platform
  - x86: used for PC platform (v)
- IDE support
  - VS Code
  - Eclipse
