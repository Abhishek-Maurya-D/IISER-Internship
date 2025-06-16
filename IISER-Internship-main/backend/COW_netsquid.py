# Importing required libraries and modules
import netsquid as ns
from netsquid.nodes import Node, DirectConnection
from netsquid.components.models.qerrormodels import DepolarNoiseModel
from netsquid.components import QuantumChannel
from netsquid.protocols import Protocol
from netsquid.qubits import create_qubits, assign_qstate, ketstates
import numpy as np

# Alice's protocol for sending quantum bits
class Alice(Protocol):
    def __init__(self, node, num_bits, delay=1, decoy_prob=0.1):
        super().__init__()
        self.actual_key = np.random.choice([0, 1], size=num_bits)  # Generate random bit string
        self.sent_sequence = []  # To record what was sent (bit or decoy)
        self.num_bits = num_bits
        self.decoy_prob = decoy_prob  # Probability of sending a decoy pulse
        self.delay = delay  # Time gap between pulses

    def run(self):
        rand_val = np.random.rand()  # Random value to decide decoy insertion
        for i in range(self.num_bits):
            if rand_val < self.decoy_prob:
                # Send a decoy: two pulses (early and late)
                pulse1, = create_qubits(1)
                pulse2, = create_qubits(1)
                pulse1.assign_qstate(ketstates.s1)
                pulse2.assign_qstate(ketstates.s1)

                self.node.ports["qout"].tx_output(pulse1)  # Early pulse
                yield self.await_timer(self.delay)
                self.node.ports["qout"].tx_output(pulse2)  # Late pulse

                self.sent_sequence.append("decoy")
            else:
                # Send data pulse based on actual key bit
                pulse, = create_qubits(1)
                pulse.assign_qstate(ketstates.s1)
                bit = self.actual_key[i]

                if bit == 1:
                    # Send early pulse for bit 1
                    self.node.ports["qout"].tx_output(pulse)
                    self.sent_sequence.append(1)
                else:
                    # Send late pulse for bit 0
                    yield self.await_timer(self.delay)
                    self.node.ports["qout"].tx_output(pulse)
                    self.sent_sequence.append(0)

                yield self.await_timer(self.delay)  # Wait before sending the next pulse

# Bob's protocol for receiving and processing pulses
class Bob(Protocol):
    def __init__(self, node, exp_pulses, dm2_thresh, f, delay=1):
        super().__init__()
        self.node = node
        self.exp_pulses = exp_pulses  # Expected number of pulses to receive
        self.dm2_thresh = dm2_thresh  # Monitoring parameter (unused here)
        self.f = f  # Fraction of pulses sent to monitoring line
        self.delay = delay
        self.recv_bits = []  # Bits decoded from pulses
        self.dm1_count = 0  # Placeholder for monitoring count
        self.dm_2_count = 0  # Placeholder for monitoring count
        self.total_received = 0

    def run(self):
        while self.total_received < self.exp_pulses:
            # Wait for pulse at input port
            yield self.await_port_input(self.node.ports["qin"])
            pulse = self.node.ports["qin"].rx_input().items[0]
            arrival_time = pulse.time  # Timestamp when pulse arrived
            
            if np.random.rand() < self.f:
                # Monitoring path (e.g., interferometer) - not implemented
                pass
            else:
                # Data line decoding: determine time-bin based on pulse arrival
                time_bin_pos = arrival_time % (2 * self.delay)
                if time_bin_pos < self.delay:
                    self.recv_bits.append(0)  # Late pulse ⇒ bit 0
                else:
                    self.recv_bits.append(1)  # Early pulse ⇒ bit 1
                self.total_received += 1
            
            yield self.await_timer(self.delay)  # Wait before receiving next pulse

# Function to simulate the COW protocol
def run_cow_protocol(num_pulses=10, delay=1, depolar_rate=0.01):
    # Create two nodes for Alice and Bob
    alice = Node("Alice", port_names=["qout"])
    bob = Node("Bob", port_names=["qin"])

    # Create a quantum channel with depolarizing noise model
    noise_model = DepolarNoiseModel(depolar_rate, time_independent=True)
    cchannel = QuantumChannel("cChannel_Alice_Bob",
                              length=10,  # Length of fiber (in km)
                              models={"quantum_noise_model": noise_model})

    # Establish direct quantum connection between Alice and Bob
    connection = DirectConnection("conn[Alice->Bob]", channel_AtoB=cchannel)
    alice.connect_to(bob, connection=connection,
                     local_port_name="qout", remote_port_name="qin")

    # Instantiate protocol objects for Alice and Bob
    alice_entity = Alice(alice, num_pulses, delay)
    bob_protocol = Bob(bob, exp_pulses=num_pulses, dm2_thresh=3, f=0.1, delay=delay)

    # Start both protocols
    alice_entity.start()
    bob_protocol.start()

    # Run the simulation
    ns.sim_run()

    # Output the received bits and calculate QBER (Quantum Bit Error Rate)
    print("Recv bits in main:", bob_protocol.recv_bits)
    count = 0
    for i in range(len(bob_protocol.recv_bits)):
        if bob_protocol.recv_bits[i] != alice_entity.actual_key[i]:
            count += 1
    qber = count / len(bob_protocol.recv_bits)
    print("QBER", qber)

    return qber

# Run the full protocol
run_cow_protocol()