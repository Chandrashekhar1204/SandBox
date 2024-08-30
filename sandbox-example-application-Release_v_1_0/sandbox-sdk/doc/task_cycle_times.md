# Task cycle times for periodic application tasks
Periodic task functions can only be registered to be called at discrete cycle times.
The following table gives an overview on which cycle times (T1..T4) are possible for each product:
| Task  | ACS880    | ACS6080, ACS8080, ACS5000 Gen 3   | TUREL     |
|-------|-----------|-----------------------------------|-----------|
| T1    | 250 us    | 125 us                            | 250 us    |
| T2    | 500 us    | 500 us                            | 500 us    |
| T3    | 2 ms      | 2 ms                              | 2 ms      |
| T4    | 10 ms     | 10 ms                             | 10 ms     |

**_NOTE:_** each application can only register one task function to be called for each available cycle time.