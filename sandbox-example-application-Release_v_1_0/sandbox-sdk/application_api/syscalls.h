//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// (C) Copyright 2020 ABB. All rights reserved.
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Subsystem: Sandbox
// File: syscalls.h
// Description: Common system calls interface
//
// Related documents:
//
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#ifndef SANDBOX_SYSCALLS_H_
#define SANDBOX_SYSCALLS_H_

#include <stdint.h>
#include <stddef.h>
#include <sys/types.h>

#if defined(_WIN32)
    #define API_FUNCTION __cdecl
#else
    #define API_FUNCTION
#endif

#ifdef __cplusplus
extern "C"
{
#endif

/**
 * @brief Registers a cyclic task (function) that will be executed periodically.
 * 
 * See [API_cpp.md](API_cpp.md) for more information.
 */
float API_FUNCTION register_cyclic_task(void (API_FUNCTION *task)(void), float max_period, size_t stack_size = 1000);

/**
 * @brief Registers a task that will be executed in the background.
 *
 * See [API_cpp.md](API_cpp.md) for more information.
 */
bool API_FUNCTION register_background_task(void (API_FUNCTION *task)(void), size_t stack_size = 1000);

/**
 * @brief Reads a parameter and returns the value as a float.
 *
 * See [API_cpp.md](API_cpp.md) for more information.
 */
float API_FUNCTION read_parameter_float(uint32_t group, uint32_t index);

/**
 * @brief Reads a parameter and returns the value as int32.
 *
 * See [API_cpp.md](API_cpp.md) for more information.
 */
int32_t API_FUNCTION read_parameter_int32(uint32_t group, uint32_t index);

/**
 * @brief Reads a pointer parameter destination value without converting it.
 *
 * See [API_cpp.md](API_cpp.md) for more information.
 */
uint32_t API_FUNCTION read_pointer_parameter_unconverted(uint32_t group, uint32_t index);

/**
 * @brief Reads a pointer parameter destination value while converting it to float.
 *
 * See [API_cpp.md](API_cpp.md) for more information.
 */
float API_FUNCTION read_pointer_parameter_as_float(uint32_t group, uint32_t index);

/**
 * @brief Writes a float value to a parameter.
 *
 * See [API_cpp.md](API_cpp.md) for more information.
 */
bool API_FUNCTION write_parameter_float(uint32_t group, uint32_t index, float value);

/**
 * @brief Writes an int32 value to a parameter.
 *
 * See [API_cpp.md](API_cpp.md) for more information.
 */
bool API_FUNCTION write_parameter_int32(uint32_t group, uint32_t index, int32_t value);

#ifdef __cplusplus
}
#endif

#endif // SANDBOX_SYSCALLS_H_
