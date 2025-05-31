import netsquid as ns
from netsquid.nodes import Node, DirectConnection
from netsquid.components.models.qerrormodels import DepolarNoiseModel
from netsquid.components import QuantumChannel
from netsquid.nodes import DirectConnection
from netsquid.protocols import Protocol
from netsquid.qubits import create_qubits, assign_qstate, ketstates

import numpy as np

class Alice(Protocol):
    def __init__(self, node, num_bits, delay=1, decoy_prob=0.1):
        super().__init__()
        self.actual_key = np.random.choice([0, 1], size=num_bits)
        self.sent_sequence=[]
        self.num_bits=num_bits
        self.decoy_prob=decoy_prob
    def run(self):
        rand_val = np.random.rand()
        for i in range(self.num_bits):
            if rand_val < self.decoy_prob:
                # Send pulse at both early and late bins (decoy)
                pulse1, = create_qubits(1)
                pulse2, = create_qubits(1)
                pulse1.assign_qstate(ketstates.s1)
                pulse2.assign_qstate(ketstates.s1)

                self.node.ports["qout"].tx_output(pulse1)  # Early
                yield self.await_timer(self.delay)
                self.node.ports["qout"].tx_output(pulse2)  # Late

                self.sent_sequence.append("decoy")
            else:
                pulse, = create_qubits(1)
                pulse.assign_qstate(ketstates.s1)

                bit = self.actual_key[i]

                if bit == 1:
                    # Early pulse (bit 1)
                    self.node.ports["qout"].tx_output(pulse)
                    self.sent_sequence.append(1)
                else:
                    # Late pulse (bit 0)
                    yield self.await_timer(self.delay)
                    self.node.ports["qout"].tx_output(pulse)
                    self.sent_sequence.append(0)

                yield self.await_timer(self.delay)

            
class Bob(Protocol):
    def __init__(self, node, exp_pulses, dm2_thresh,f, delay=1):
        super().__init__()
        self.node=node
        self.exp_pulses=exp_pulses
        self.dm2_thresh=dm2_thresh 
        self.f=f
        self.delay=delay
        self.recv_bits=[]
        self.dm1_count=0
        self.dm_2_count=0
        self.total_received = 0
    def run(self):
        while self.total_received<self.exp_pulses:
            yield self.await_port_input(self.node.ports["qin"])
            pulse=self.node.ports["qin"].rx_input().items[0]
            arrival_time = pulse.time 
            
            if np.random.rand()<self.f: #go to the monitoring line with a probability of f(generally 10%)
                '''interfered=self.simulate_intereference(pul_0, pul_1)
                if interfered=="DM1":
                    self.dm1_count+=1
                else:
                    self.dm_2_count+=1'''
                pass
            else:
                #go to dataline
                time_bin_pos = arrival_time % (2 * self.delay) #here each time bin is self.delay time
                if time_bin_pos<self.delay:
                    self.recv_bits.append(0)
                else:
                    self.recv_bits.append(1)
                self.total_received += 1
            yield self.await_timer(self.delay)
                
                
                
            
        
    

def run_cow_protocol(num_pulses=10, delay=1, depolar_rate=0.01):
    alice = Node("Alice", port_names=["qout"])
    bob = Node("Bob", port_names=["qin"])

# Create a quantum channel with optional depolarizing noise
    noise_model = DepolarNoiseModel(depolar_rate, time_independent=True)
    cchannel = QuantumChannel("cChannel_Alice_Bob",
                          length=10, #in km
                          models={"quantum_noise_model": noise_model})
    connection = DirectConnection("conn[Alice->Bob]", channel_AtoB=cchannel)

    alice.connect_to(bob, connection=connection,
                 local_port_name="qout",
                 remote_port_name="qin")
    alice_entity = Alice(alice, num_pulses, delay)
    bob_protocol = Bob(bob, exp_pulses=num_pulses, dm2_thresh=3, f=0.1, delay=delay)

    
    alice_entity.start()
    bob_protocol.start()
 

    ns.sim_run()    
    print("Recv bits in main:", bob_protocol.recv_bits)
   
    count=0
    for i in range(len(bob_protocol.recv_bits)):
        if(bob_protocol.recv_bits[i]!=alice_entity.actual_key[i]):
                count+=1
    qber=count/len(bob_protocol.recv_bits)
    print("QBER", qber)
    return qber
run_cow_protocol()

        
    