from qunetsim.components import Host, Network
from qunetsim.objects import Qubit
import matplotlib.pyplot as plt
import time

# For timeline visualization
timeline = []

def log_event(actor, action):
    timestamp = time.time()
    timeline.append((timestamp, actor, action))
    print(f"[{actor}] {action}")

# Alice's protocol
def example_protocol(sender, receiver_id):
    log_event(sender.host_id, "Creating a qubit")
    q = Qubit(sender)
    q.X()
    log_event(sender.host_id, "Applied X gate (qubit = |1⟩)")
    sender.send_qubit(receiver_id, q)
    log_event(sender.host_id, f"Sent qubit to {receiver_id}")

# Bob's protocol
def receive_protocol(receiver):
    log_event(receiver.host_id, "Waiting to receive a qubit...")
    
    q = None
    while q is None:
        q = receiver.get_data_qubit('Alice', wait=1)
        time.sleep(0.1)

    log_event(receiver.host_id, "Received a qubit")
    result = q.measure()
    log_event(receiver.host_id, f"Measured qubit result: {result}")

# Matplotlib plot function
def plot_timeline(timeline):
    import matplotlib.pyplot as plt
    from matplotlib import colormaps

    actors = sorted(set(actor for _, actor, _ in timeline))
    actor_indices = {actor: i for i, actor in enumerate(actors)}
    base_time = min(t for t, _, _ in timeline)

    plt.figure(figsize=(12, 5))
    cmap = colormaps["tab10"]

    for i, (t, actor, action) in enumerate(timeline):
        relative_time = t - base_time
        y = actor_indices[actor]

        # Color by actor
        color = cmap(y % 10)

        # Dot
        plt.plot(relative_time, y, 'o', color=color, markersize=10)

        # Staggered text placement
        offset = 0.25 if i % 2 == 0 else -0.35

        # Annotation
        plt.text(relative_time, y + offset, action,
                 fontsize=9, ha='left', rotation=30, color='black')

    plt.yticks(range(len(actors)), actors)
    plt.xlabel("Time (s)")
    plt.title("Quantum Communication Timeline")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()



# Main function
def main():
    network = Network.get_instance()
    network.start()

    # Create and connect hosts
    alice = Host('Alice')
    bob = Host('Bob')
    alice.add_connection('Bob')
    bob.add_connection('Alice')

    network.add_host(alice)
    network.add_host(bob)

    # Start hosts
    alice.start()
    bob.start()

    # Run protocols
    bob.run_protocol(receive_protocol)
    alice.run_protocol(example_protocol, ('Bob',))

    time.sleep(5)
    network.stop()

    # Plot the visualization
    plot_timeline(timeline)

if __name__ == '__main__':
    main()
