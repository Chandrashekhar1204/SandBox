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
#ifndef SANDBOX_APPLICATION_API_VERSION_H_
#define SANDBOX_APPLICATION_API_VERSION_H_

#include <cstdint>

namespace sandbox_api
{
struct API_Version
{
    std::uint32_t major;
    std::uint32_t minor;

    bool operator==(API_Version const& rhs) const
    {
        return major == rhs.major && minor == rhs.minor;
    }

    bool operator!=(API_Version const& rhs) const
    {
        return !(*this == rhs);
    }
};

static constexpr API_Version version = {1, 0};

}


#endif /* #ifndef SANDBOX_APPLICATION_API_VERSION_H_ */
