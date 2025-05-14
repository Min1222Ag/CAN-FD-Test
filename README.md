# Description
This repository is for evaluation of CAN messages using python-can.
There are test codes and dataset.

## Dataset
- There are two types of dataset
1. CAN messages
  - can1_message.csv
  - can2_message.csv
2. CAN FD messages
   - timestamp_canfd_message.csv
   - You need to change column 'timestamp' to 'Timestamp'
   - 
## Expected Result
```
======== Summary ========

[proc_fd_1] TX: 5, RX: 5
proc_fd_1 Latency mean: 54368 ns, median: 43201 ns
proc_fd_1 TX throughput: 900.69 msg/sec

[proc_fd_2] TX: 5, RX: 5
proc_fd_2 Latency mean: 44222 ns, median: 29916 ns
proc_fd_2 TX throughput: 1264.33 msg/sec

[proc_can_1] TX: 10, RX: 10
proc_can_1 Latency mean: 35238 ns, median: 31775 ns
proc_can_1 TX throughput: 2204.40 msg/sec

[proc_can_2] TX: 10, RX: 10
proc_can_2 Latency mean: 31981 ns, median: 23170 ns
proc_can_2 TX throughput: 3069.62 msg/sec

[Overall] Latency mean: 38838 ns
[Overall] Total TX: 30, RX: 30
```
