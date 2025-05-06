import pyshark
import os
import csv
import statistics

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data/raw")
OUT_FILE = os.path.join(BASE_DIR, "data/processed/features2.csv")

def extract_features_from_pcap(filepath, max_packets=1000):
    print(f"[DEBUG] Opening: {filepath}")
    
    try:
        cap = pyshark.FileCapture(
            filepath,
            use_json=True,
            include_raw=True,
            keep_packets=False
        )
    except Exception as e:
        print(f"[!] Failed to load {filepath}: {e}")
        return None

    total_packets = 0
    total_bytes = 0
    packet_sizes = []
    timestamps = []

    try:
        for i, pkt in enumerate(cap):
            if i >= max_packets:
                break
            try:
                size = int(pkt.length)
                time = float(pkt.sniff_timestamp)
                packet_sizes.append(size)
                timestamps.append(time)
                total_bytes += size
                total_packets += 1
            except Exception:
                continue
    except Exception as e:
        print(f"[!] Error while parsing {filepath}: {e}")
        return None
    finally:
        cap.close()

    duration = max(timestamps) - min(timestamps) if timestamps else 0
    avg_pkt_size = sum(packet_sizes) / len(packet_sizes) if packet_sizes else 0
    max_pkt_size = max(packet_sizes) if packet_sizes else 0
    std_pkt_size = statistics.stdev(packet_sizes) if len(packet_sizes) > 1 else 0

    interarrival_times = [j - i for i, j in zip(timestamps[:-1], timestamps[1:])]
    mean_iat = sum(interarrival_times) / len(interarrival_times) if interarrival_times else 0
    std_iat = statistics.stdev(interarrival_times) if len(interarrival_times) > 1 else 0

    first_timestamp = timestamps[0] if timestamps else 0
    first_5s_packet_count = sum(1 for t in timestamps if t - first_timestamp <= 5)

    return {
        "total_packets": total_packets,
        "total_bytes": total_bytes,
        "avg_packet_size": avg_pkt_size,
        "duration": duration,
        "max_packet_size": max_pkt_size,
        "std_packet_size": std_pkt_size,
        "mean_interarrival_time": mean_iat,
        "std_interarrival_time": std_iat,
        "first_5s_packet_count": first_5s_packet_count
    }


def extract_all(directory, output_csv):
    with open(output_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames = [
        "filename", "total_packets", "total_bytes", "avg_packet_size", "duration",
        "max_packet_size", "std_packet_size", "mean_interarrival_time",
        "std_interarrival_time", "first_5s_packet_count", "label"
    ])
        writer.writeheader()

        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".pcap"):
                    full_path = os.path.join(root, file)
                    label = os.path.basename(root)
                    print(f"Processing {file} ({label})...")
                    stats = extract_features_from_pcap(full_path)
                    if stats:
                        stats["filename"] = file
                        stats["label"] = label
                        writer.writerow(stats)
                    else:
                        print(f"[!] Skipped {file} due to error")

if __name__ == "__main__":
    extract_all(RAW_DIR, OUT_FILE)
