import pyshark
import os
import csv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data/raw/captures")
OUT_FILE = os.path.join(BASE_DIR, "data/processed/features1.csv")

def extract_features_from_pcap(filepath):
    cap = pyshark.FileCapture(filepath, use_json=True, include_raw=True)
    
    total_packets = 0
    total_bytes = 0
    packet_sizes = []
    timestamps = []
    
    for pkt in cap:
        try:
            size = int(pkt.length)
            time = float(pkt.sniff_timestamp)

            packet_sizes.append(size)
            timestamps.append(time)
            total_bytes += size
            total_packets += 1
        except Exception:
            continue

    cap.close()

    duration = max(timestamps) - min(timestamps) if timestamps else 0
    avg_pkt_size = sum(packet_sizes) / len(packet_sizes) if packet_sizes else 0
    return {
        "total_packets": total_packets,
        "total_bytes": total_bytes,
        "avg_packet_size": avg_pkt_size,
        "duration": duration
    }

def extract_all(directory, output_csv):
    with open(output_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["filename", "total_packets", "total_bytes", "avg_packet_size", "duration", "label"])
        writer.writeheader()
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".pcap"):
                    full_path = os.path.join(root, file)
                    label = os.path.basename(root) 
                    print(f"Processing {file} ({label})...")
                    stats = extract_features_from_pcap(full_path)
                    stats["filename"] = file
                    stats["label"] = label
                    writer.writerow(stats)

if __name__ == "__main__":
    extract_all(RAW_DIR, OUT_FILE)
