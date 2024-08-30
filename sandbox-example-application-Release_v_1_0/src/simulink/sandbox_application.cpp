#include "syscalls.h"
#include "sandbox_application.h"
#include "sandbox_application_bindings.h"
#include "sandbox_application_grt_rtw/sandbox_application.h"
#include <cmath>

REGISTER_APPLICATION

// application version, major.minor.patch.build
uint8_t application_version_major = 0;
uint8_t application_version_minor = 1;
uint8_t application_version_patch = 0;
uint8_t application_version_build = 0;

// 5 letter application name, NOTE: use only ASCII characters 47 (/) to 110 (n)
char const application_name[SANDBOX_APPLICATON_NAME_LENGTH] = {'S','D','K','S','L'};
// application description text
char const * application_version_text = "simulink application 2023-04-12 09:20";


float cycle_t0 = 0;
float cycle_t1 = 0;
float cycle_t2 = 0;
float cycle_t3 = 0;


void API_FUNCTION application_t0();
void API_FUNCTION application_t0()
{
    // call simulink generated code
   sandbox_application_step(0);
}

void API_FUNCTION application_t1();
void API_FUNCTION application_t1()
{
    // call simulink generated code
   sandbox_application_step(1);
}

void API_FUNCTION application_t2();
void API_FUNCTION application_t2()
{
    sandbox_application_step(2);
}

void API_FUNCTION application_t3();
void API_FUNCTION application_t3()
{
    sandbox_application_step(3);
}

void API_FUNCTION application_background();
void API_FUNCTION application_background()
{
}

void application_init_user();
void application_init_user()
{
    cycle_t0 = register_cyclic_task(&application_t0, 250e-6, 10000);    // register application_t0 at 250us cycle time with 10k stack size
    cycle_t1 = register_cyclic_task(&application_t1, 500e-6, 10000);    // register application_t1 at 500us cycle time with 10k stack size
    cycle_t2 = register_cyclic_task(&application_t2, 2e-3, 10000);      // register application_t2 at 2ms cycle time with 10k stack size
    cycle_t3 = register_cyclic_task(&application_t3, 10e-3, 10000);     // register application_t3 at 10ms cycle time with 10k stack size
    register_background_task(&application_background, 10000);           // register application_background as background task with 10k stack size

    sandbox_application_initialize();
}

