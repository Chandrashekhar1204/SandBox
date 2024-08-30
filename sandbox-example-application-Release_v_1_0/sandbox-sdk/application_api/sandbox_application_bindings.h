//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// (C) Copyright 2020 ABB. All rights reserved.
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Subsystem: Sandbox
// File: sandbox_application_bindings.h
// Description: Bindings which need to be implemented by a Sandbox application so that it can be used by UNICOS
//
// Related documents:
//
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#ifndef SANDBOX_APPLICATION_BINDINGS_H_
#define SANDBOX_APPLICATION_BINDINGS_H_

#include <cstdint>
#include "syscalls.h"
#include "sandbox_api_version.h"

namespace sandbox
{
namespace system_calls
{
struct System_Call_Implementation;
}
}  // namespace sandbox

namespace sandbox_api
{

struct UNICOS_To_Application
{
    sandbox::system_calls::System_Call_Implementation const* system_calls_table;
};

struct Host_To_Application
{
    API_Version api_version;
};

} /* namespace sandbox_api */

#if defined(_WIN32)
    /* You should define ADD_EXPORTS *only* when building the DLL. */
    #ifdef COPT_DYNAMIC_LOADING_EXPORT
        #define ADDAPI __declspec(dllexport)
    #else
        #define ADDAPI __declspec(dllimport)
    #endif

#else
    #define ADDAPI
#endif

/* Make sure functions are exported with C linkage under C++ compilers. */
#ifdef __cplusplus
extern "C"
{
#endif

    ADDAPI int API_FUNCTION application_init(sandbox_api::UNICOS_To_Application unicos_to_application);

/* Make sure functions are exported with C linkage under C++ compilers. */
#ifdef __cplusplus
}
#endif

#define REGISTER_APPLICATION volatile void* dummy_to_avoid_linker_removing_application_init = (void*)(&application_init);

#endif /* #ifndef SANDBOX_APPLICATION_BINDINGS_H_ */
