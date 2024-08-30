#include "syscalls.h"
#include "sandbox_application.h"
#include <cmath>
#include "sandbox_application_bindings.h"

REGISTER_APPLICATION

// application version, major.minor.patch.build
uint8_t application_version_major = 0;
uint8_t application_version_minor = 2;
uint8_t application_version_patch = 0;
uint8_t application_version_build = 0;

// 5 letter application name, NOTE: use only ASCII characters 47 (/) to 110 (n)
char const application_name[SANDBOX_APPLICATON_NAME_LENGTH] = {'S','D','K','C','P'};
// application description text
char const * application_version_text = "c++ application 2022-12-15 10:28 commit x";

float sin_angle = 0.0;
float cycle_t1 = 0;
float cycle_t2 = 0;
float cycle_t3 = 0;
float cycle_t4 = 0;

unsigned int t1_counter = 0;
unsigned int t2_counter = 0;
unsigned int t3_counter = 0;
unsigned int t4_counter = 0;
unsigned int bgnd_counter = 0;


void API_FUNCTION application_t1();
void API_FUNCTION application_t1()
{
    write_parameter_int32(47, 11, ++t1_counter);

    float output = std::sin(sin_angle);

    static float const pi2 = (float)(2 * std::acos(-1.0));
    float const sin_period = 20e-3f;
    float const interval = cycle_t1;
    float const angle_increment = (float)(pi2 * interval / sin_period);
    sin_angle += angle_increment;

    if (sin_angle >= pi2)
    {
        sin_angle = std::fmod(sin_angle, pi2);
    }

    bool success = write_parameter_float(47, 1, output);
}

void API_FUNCTION application_t2();
void API_FUNCTION application_t2()
{
    write_parameter_int32(47, 12, ++t2_counter);
}

void API_FUNCTION application_t3();
void API_FUNCTION application_t3()
{
    write_parameter_int32(47, 13, ++t3_counter);
}

void API_FUNCTION application_t4();
void API_FUNCTION application_t4()
{
    write_parameter_int32(47, 14, ++t4_counter);

    // echo value of 47.16 to 47.17
    int value = read_parameter_int32(47, 16);
    write_parameter_int32(47, 17, value);
}

void API_FUNCTION application_background();
void API_FUNCTION application_background()
{
    write_parameter_int32(47, 15, ++bgnd_counter);
}

void application_init_user();
void application_init_user()
{
    cycle_t1 = register_cyclic_task(&application_t1, 250e-6, 10000);    // register application_t1 at 250us cycle time with 10k stack size
    cycle_t2 = register_cyclic_task(&application_t2, 500e-6, 10000);    // register application_t2 at 500us cycle time with 10k stack size
    cycle_t3 = register_cyclic_task(&application_t3, 2e-3, 10000);      // register application_t3 at 2ms cycle time with 10k stack size
    cycle_t4 = register_cyclic_task(&application_t4, 10e-3, 10000);     // register application_t4 at 10ms cycle time with 10k stack size
    register_background_task(&application_background, 10000);           // register application_background as background task with 10k stack size
}

