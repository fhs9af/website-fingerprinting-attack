import pyshark

cap = pyshark.FileCapture('data/raw/cnn/cnn_1.pcap')

for i, pkt in enumerate(cap):
    if i >= 5:
        break
    print(pkt.highest_layer, pkt.length, pkt.sniff_time)
