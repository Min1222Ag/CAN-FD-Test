# Description
This repository is for evaluation of CAN messages using python-can.
There are test codes and dataset.

## Dataset
- There are two types of dataset
1. CAN messages
2. CAN FD messages
   - timestamp_canfd_message
## loopback_can_fd_test.py
It is just for loopback test using vcan with socketCAN.
- Result
```Sent and received. Latency: 31.7 μs
 Sent and received. Latency: 23.2 μs
Sent and received. Latency: 32.3 μs
Sent and received. Latency: 24.0 μs
Sent and received. Latency: 31.0 μs
Sent and received. Latency: 23.2 μs
Sent and received. Latency: 32.1 μs
Sent and received. Latency: 32.6 μs
Sent and received. Latency: 32.2 μs
Sent and received. Latency: 31.1 μs
Sent and received. Latency: 24.1 μs
Sent and received. Latency: 34.2 μs
```

- Because there is no CAN controller for loopback test, latency is low.
