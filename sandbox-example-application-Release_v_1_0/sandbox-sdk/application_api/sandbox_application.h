//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// (C) Copyright 2021 ABB. All rights reserved.
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Subsystem: Sandbox application lib
// File: main.cpp
// Description: Main function for Sandbox application
//
// Related documents:
//
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#ifndef SANDBOX_APPLICATION_API_SANDBOX_APPLICATION_H_
#define SANDBOX_APPLICATION_API_SANDBOX_APPLICATION_H_

#include <cstdint>

#define SANDBOX_APPLICATON_NAME_LENGTH 5
#define SANDBOX_APPLICATON_VERSION_TEXT_LENGTH 255

extern "C"
{
    void application_init_user();
    extern uint8_t application_version_major;
    extern uint8_t application_version_minor;
    extern uint8_t application_version_patch;
    extern uint8_t application_version_build;
    extern char const application_name[SANDBOX_APPLICATON_NAME_LENGTH];
    extern char const * application_version_text;
}

#endif /* SANDBOX_APPLICATION_API_SANDBOX_APPLICATION_H_ */
