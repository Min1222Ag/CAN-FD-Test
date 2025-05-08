#!/usr/bin/env python3
import pandas as pd
import can
import time

df = pd.read_csv('timestamp_canfd_message.csv')
df = df.dropna(subset=['timestamp', 'AID', 'Data'])
df['timestamp'] = pd.to_numeric(df['timestamp'], errors='coerce')
df = df.sort_values('timestamp').reset_index(drop=True)

start_time = df.loc[0, 'timestamp']

with can.Bus(channel='vcan0', interface='socketcan', receive_own_messages=True, fd=True) as bus:
    prev_timestamp = start_time

    for i, row in df.iterrows():
        try:
            curr_timestamp = float(row['timestamp'])
            delta = curr_timestamp - prev_timestamp
            prev_timestamp = curr_timestamp

            # time starts from 0
            if delta > 0:
                time.sleep(delta)

            # preprocess data
            can_id = int(row['AID'], 16) if isinstance(row['AID'], str) else int(row['AID'])
            data_str_list = row['Data'].strip().split()
            cleaned = [b for b in data_str_list if len(b) == 2 and all(c in '0123456789abcdefABCDEF' for c in b)]
            dlc = len(cleaned)
            cleaned = cleaned[:dlc] + ['00'] * (dlc - len(cleaned))

            data_bytes = bytes([int(b, 16) & 0xFF for b in cleaned])

            msg = can.Message(
                arbitration_id=can_id,
                data=data_bytes,
                is_extended_id=False,
                is_fd=True,
                bitrate_switch=True
            )

            # start timer
            t0 = time.perf_counter_ns()
            bus.send(msg)

            # Waiting for RX(loopback)
            recv = bus.recv(timeout=1.0)
            t1 = time.perf_counter_ns()

            if recv is not None:
                latency_us = (t1 - t0) / 1000  # microseconds
                print(f"Sent and received. Latency: {latency_us:.1f} μs")
            else:
                print("Timed out waiting for loopback")

        except Exception as e:
            print(f" Error: {e}")