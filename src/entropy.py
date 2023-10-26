from collections import Counter
import math

def calculate_entropy(ports):
    total_ports = len(ports)
    port_counts = Counter(ports)
    entropy = 0.0
    
    for count in port_counts.values():
        probability = count / total_ports
        entropy -= probability * math.log2(probability)
    
    return entropy
