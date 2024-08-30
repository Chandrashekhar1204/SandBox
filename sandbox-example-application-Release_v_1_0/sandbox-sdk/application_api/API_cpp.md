# Application API for C++ applications

## API Index
- [read_parameter_float](#read_parameter_float)
- [read_parameter_int32](#read_parameter_float)
- [write_parameter_float](#write_parameter_float)
- [write_parameter_int32](#read_parameter_float)
- [read_pointer_parameter_unconverted](#read_pointer_parameter_unconverted)
- [read_pointer_parameter_as_float](#read_pointer_parameter_as_float)
- [application_init_user](#application_init_user)
- [register_cyclic_task](#register_cyclic_task)
- [register_background_task](#register_background_task)
- [get_timer_counter_value](#get_timer_counter_value)
- [get_timer_counter_frequency](#get_timer_counter_frequency)

## Topics
- [Drive Parameter Interface for data exchange](#drive-parameter-interface-for-data-exchange)
- [Application tasks / entry points](#application-tasks--entry-points)
- [Application name and application version information](#application-name-and-application-version-information)
- [Stack and heap size](#stack-and-heap-size)
- [Memory usage restrictions](#Maximum-memory-usage-restrictions)
- [File system](#file-system)
- [Maximum files opened simultaneously](#maximum-files-opened-simultaneously)
- [Logging support](#logging-support)

## Drive Parameter Interface for data exchange

### ```read_parameter_float```
```cpp
float read_parameter_float(uint32_t group, uint32_t index)
```
Reads parameter ```group```.```index``` and returns the value as a ```float```.
#### Parameters
- ```group```: parameter group
- ```index```: parameter index

#### Return value
Returns the value of parameter, in case parameter exists and reading as float is supported, 0.0 otherwise.

**_NOTE:_** not every parameter can be accessed in every data type. See [Parameter data types](#parameter-data-types) for details.

### ```read_parameter_int32```
```cpp
int32_t read_parameter_int32(uint32_t group, uint32_t index)
```
Reads parameter ```group```.```index``` and returns the value as ```int32_t```.
#### Parameters
- ```group```: parameter group
- ```index```: parameter index

#### Return value
Returns the value of parameter, in case parameter exists and reading as int32 is supported, 0 otherwise.

**_NOTE:_** not every parameter can be accessed in every data type. See [Parameter data types](#parameter-data-types) for details.

### ```write_parameter_float```
```cpp
bool write_parameter_float(uint32_t group, uint32_t index, float value)
```
Writes to parameter ```group```.```index``` using ```float``` data type.
#### Parameters
- ```group```: parameter group
- ```index```: parameter index
- ```value```: value to be written

#### Return value
```true``` in case of success, ```false``` otherwise.

**_NOTE:_** not every parameter can be accessed in every data type. See [Parameter data types](#parameter-data-types) for details.

### ```write_parameter_int32```
```cpp
bool write_parameter_int32(uint32_t group, uint32_t index, int32_t value)
```
Writes to parameter ```group```.```index``` using ```int32_t``` data type.
#### Parameters
- ```group```: parameter group
- ```index```: parameter index
- ```value```: value to be written

#### Return value
```true``` in case of success, ```false``` otherwise.

**_NOTE:_** not every parameter can be accessed in every data type. See [Parameter data types](#parameter-data-types) for details.

### ```read_pointer_parameter_unconverted```
```cpp
uint32_t read_pointer_parameter_unconverted(uint32_t group, uint32_t index)
```
Reads the value of the parameter 1 to which parameter 2 at ```group```.```index``` is pointing to without converting it's value.
#### Parameters
- ```group```: parameter group
- ```index```: parameter index

#### Return value
Returns the **unconverted** value of the parameter 1.

**_NOTE:_** A reinterpret_cast might be needed to convert the raw (unconverted) value to the correct type. If the type of the parameter being pointed to is float, then the value needs to be reinterpret_cast to a float:
```cpp
uint32_t value_raw = read_pointer_parameter_as_float(1, 6);
float value_float = *reinterpret_cast<float*>(&value_raw);
```

### ```read_pointer_parameter_as_float```
```cpp
float read_pointer_parameter_as_float(uint32_t group, uint32_t index)
```
Reads the value of the parameter 1 to which parameter 2 at ```group```.```index``` is pointing to and **converts** the value to ```float```.

#### Parameters
- ```group```: parameter group
- ```index```: parameter index

#### Return value
Returns the value of parameter 1 **converted** to ```float```.

### Parameter data types
Each parameter is implemented using an underlying data type. Options can be:
- real32
    - 32 bit floating point type
    - can be accesssed using ```{read,write}_parameter_float``` functions
- (u)int32
    - 32 bit integer data type
    - can be accesssed using ```{read,write}_parameter_int32``` functions
- (u)int16
    - 16 bit integer data type
    - can be accesssed using ```{read,write}_parameter_int32``` functions

Information about which data types are used for each parameter can be found in the product user manuals in the **Type** column of the parameter description.

## Application tasks / entry points

### ```application_init_user```
This function is executed upon loading of the application.
It's main purpose is to initialize global state and register application tasks.
The example application registers
- 4 cyclic tasks with specific cycle times using [register_cyclic_task](#register_cyclic_task)
- 1 background task using [register_background_task](#register_background_task)
### ```register_cyclic_task```
```cpp
float register_cyclic_task(void (API_FUNCTION *task)(void), float max_period, size_t stack_size = 1000)
```
Registers a cyclic task (function) that will be executed periodically.
#### Parameters
- ```task```: The function pointer to the task.
    - see [task functions](#task-functions) for requirements and details on how to implement ```task```
- ```max_period```: The maximum allowed period of the task in seconds.
    - **_NOTE:_** only discrete task cycle times are supported by each product, see [task_cycle_times.md](task_cycle_times.md) for more details.
- ```stack_size```: The size of the stack for the task in bytes (default: 1000).

#### Return value
Returns the actual time [s] by which ```task``` will be called periodically.

**_NOTE:_** each application can only register one function with the same task cycle. In case another function was already registered at the same task cycle, the previous function will be unregistered and only the new function will be registered.

### ```register_background_task```
```cpp
bool register_background_task(void (API_FUNCTION *task)(void), size_t stack_size = 1000)
```
Registers a task that will be executed in the background.
#### Parameters
- ```task```: The function pointer to the task.
    - see [task functions](#task-functions) for requirements and details on how to implement ```task```
- ```stack_size```: The size of the stack for the task in bytes (default: 1000).

#### Return value
```true``` if the task was successfully registered, ```false``` otherwise.

**_NOTE:_** each application can only register one background function. In case another function was already registered, the previous function will be unregistered and only the new function will be registered.

### task functions
Task functions need to adhere to certain requirements so that they can be used as cyclic or background task functions. The following prototype must be used to implement task functions.
```cpp
void API_FUNCTION application_task(void);
```
- ```application_task``` needs to adhere to specific calling conventions. This can be achieved by using ```API_FUNCTION``` when declaring the function

## Application name and application version information
Each application must instantiate the following global variables in order to register the application name and version information:
- ```application_name```: 5 letter application name
    - used to identify an application
    - should be unique between different applications
- ```application_version_{major, minor, patch, build}```
    - used to indicate the application version in format of major.minor.patch.build
- ```application_version_text```
    - Free text which can be used to specify further application details, including e.g. build date or commit SHA

## Stack and heap size
### Stack
Each registered application task has it's own stack. The size of this stack can be selected when registering the task e.g. using [register_cyclic_task](#register_cyclic_task).

The total amount of memory which is available for stacks of all application tasks is 1MB by default. This can be adjusted by changing ```_STACK_SIZE``` in [src/lscript.ld](../src/lscript.ld).

### Heap
By default the maximum heap size available is 1MB.
This can be changed by adjusting ```_HEAP_SIZE``` in [src/lscript.ld](../src/lscript.ld).

### Memory usage restrictions
>**_NOTE:_** the total memory size which can be used by an application is
>currently limited to 6MB. This means that code, data, stack and heap all need to fit within this space.


## Timer counter functions
### ```get_timer_counter_value```
```cpp
uint64_t get_timer_counter_value()
```
Get the current value of the system timer counter.

#### Return value
The current value of the system timer counter. 1 equals to the timer period which is 1/frequency [s].

### ```get_timer_counter_frequency```
```cpp
uint64_t get_timer_counter_frequency()
```
Get the system timer counter frequency.

#### Return value
The frequency of the system timer counter [hz].


## File system

Sandbox applications can use file handling functionality from standard C & C++ library (fopen/fread/fwrite/cout/...), every application
root filesystem is located at `<FS root>/SANDBOX/<application name>/` (i.e. /SD_card_root/SANDBOX/APP/file.txt).
Sandbox `<application name>` is registered through [application_name](#application-name-and-application-version-information) variable.

> Note: File IO is possible only in background task.
> The reason is that this operation takes a significant amount of time and is not deterministic.

Example:
```cpp
#include <cstdio>
// ...

// Open file in read/write mode
FILE* fd = fopen("path/to/file.txt", "r+");

// Wirte or read to file
fwrite(write_buffer, sizeof(write_buffer[0]), strlen(write_buffer), fd);

// ...

// Close file if it is no longer needed
fclose(fd);
```

Sandbox manages all opened file descriptors, but user has access to them only through standard functions, so closing previously opened files is the user's responsibility.
Moreover, user can't keep files opened after application restart, all opened files are automatically closed on application stop.

### Maximum files opened simultaneously

There are restrictions, in terms of maximum files opened simultaneously by application (currently the limit is **15**). Amount of files created in application
directory is limited only by disk space.

### Logging support

Sandbox supports logging during application execution. Logs are created through standard functions which write to stdout/stderr streams.
User can call printf-like functions or write to `std::cout`/`std::cerr` as well as write to std streams like to regular files.

All logging is saved to log files (`stdout.log` and `stderr.log`) in application [directory](#file-system).

Log files are kept between application reloads, so there is no need to worry about data loss.
Every time application is loaded log files are opened and old logging sesion is separated with date and time of new application start.
Currently log file rotation is not supported.

Example:
```cpp
#include <cstdio>
// ...

printf("You can use printf to write to stdout.log\n");

fprintf(stderr, "Logging to stderr is also supported\n");

// other file
#include <iostream>

// ...

std::cout << "C++ objects are also supported" << std::endl;
```
