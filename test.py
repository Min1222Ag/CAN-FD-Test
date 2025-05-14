#!/usr/bin/env python3
import pandas as pd
import time
import can
from multiprocessing import Process, Manager
import numpy as np


def send_can_proc(df, tag, shared_data):
    df = df.dropna(subset=['Timestamp', 'AID', 'Data'])
    df['Timestamp'] = pd.to_numeric(df['Timestamp'], errors='coerce')
    df = df.sort_values('Timestamp').reset_index(drop=True)

    latencies = []
    tx_count = 0
    rx_count = 0
    tx_start_ns = None
    tx_end_ns = None

    with can.Bus(channel='vcan0', interface='socketcan', receive_own_messages=True, fd=True) as bus:
        prev_timestamp = df.loc[0, 'Timestamp']
        for _, row in df.iterrows():
            try:
                curr_timestamp = float(row['Timestamp'])
                delta = curr_timestamp - prev_timestamp
                prev_timestamp = curr_timestamp
                if delta > 0:
                    time.sleep(delta)

                can_id = int(row['AID'], 16) if isinstance(row['AID'], str) else int(row['AID'])
                data_str_list = row['Data'].strip().split()
                cleaned = [b for b in data_str_list if len(b) == 2 and all(c in '0123456789abcdefABCDEF' for c in b)]
                dlc = len(cleaned)
                cleaned = cleaned[:dlc] + ['00'] * (dlc - len(cleaned))
                data_bytes = bytes([int(b, 16) for b in cleaned])

                msg = can.Message(
                    arbitration_id=can_id,
                    data=data_bytes,
                    is_extended_id=False,
                    is_fd=(dlc > 8),
                    bitrate_switch=(dlc > 8)
                )

                t0 = time.perf_counter_ns()
                if tx_start_ns is None:
                    tx_start_ns = t0

                bus.send(msg)
                tx_count += 1

                recv = bus.recv(timeout=1.0)
                t1 = time.perf_counter_ns()
                tx_end_ns = t1

                if recv is not None:
                    latencies.append(t1 - t0)
                    rx_count += 1

            except Exception as e:
                print(f"[{tag}] Error: {e}")

    shared_data[tag] = {
        "tx": tx_count,
        "rx": rx_count,
        "latency": latencies,
        "start_ns": tx_start_ns,
        "end_ns": tx_end_ns
    }


def run_four_process_test(fd_csv_path, can_csv1_path, can_csv2_path):
    df_fd = pd.read_csv(fd_csv_path).head(10)
    mid = len(df_fd) // 2
    df_fd_1 = df_fd.iloc[:mid].copy()
    df_fd_2 = df_fd.iloc[mid:].copy()

    df_can_1 = pd.read_csv(can_csv1_path).head(10)
    df_can_2 = pd.read_csv(can_csv2_path).head(10)

    manager = Manager()
    shared = manager.dict()

    procs = [
        Process(target=send_can_proc, args=(df_fd_1, 'proc_fd_1', shared)),
        Process(target=send_can_proc, args=(df_fd_2, 'proc_fd_2', shared)),
        Process(target=send_can_proc, args=(df_can_1, 'proc_can_1', shared)),
        Process(target=send_can_proc, args=(df_can_2, 'proc_can_2', shared))
    ]

    for p in procs:
        p.start()
    for p in procs:
        p.join()

 
    print("\n======== Summary ========")
    total_tx = 0
    total_rx = 0
    all_latencies = []

    for tag in shared.keys():
        result = shared[tag]
        tx = result.get('tx', 0)
        rx = result.get('rx', 0)
        lat = result.get('latency', [])
        t0 = result.get('start_ns', 0)
        t1 = result.get('end_ns', 0)

        total_tx += tx
        total_rx += rx
        all_latencies.extend(lat)

        print(f"\n[{tag}] TX: {tx}, RX: {rx}")
        if lat:
            print(f"{tag} Latency mean: {np.mean(lat):.0f} ns, median: {np.median(lat):.0f} ns")
        if t0 and t1 and t1 > t0:
            print(f"{tag} TX throughput: {tx / ((t1 - t0) / 1e9):.2f} msg/sec")

    if all_latencies:
        print(f"\n[Overall] Latency mean: {np.mean(all_latencies):.0f} ns")
        print(f"[Overall] Total TX: {total_tx}, RX: {total_rx}")

#main
run_four_process_test("timestamp_canfd_message.csv", "can1_message.csv", "can2_message.csv")
