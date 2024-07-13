import json
import time
from source.DawnSimVis import Simulator

# currently running simulation
running_sim: Simulator = None

# last time to send or receive a message | runnig time
last_time = None

# total message count in topology
msg_count = 0



def stop_sync_sim():
    """
    Stops the running synchronous simulation and prints the result.

    This function stops the currently running synchronous simulation by calling the
    `print_result` function to print the result of the simulation, resetting the
    `msg_count` variable to 0, and deleting the `running_sim` object.
    """
    print_result()
    
    # Reset the message count to 0
    msg_count = 0
    
    # Delete the running simulation object
    running_sim.__del__()

def print_result():
    """
    Prints the result of the simulation to the console.

    The result includes the simulation ID, the simulator name, the last time the simulation ran,
    and the total number of messages sent.
    """
    # Print the simulation ID
    print("------------------------------------------------")
    
    # Print the simulator name
    print(f"Simulator Name: {running_sim.title}")
    
    # Print the last time the simulation ran
    print(f"Last Time: {last_time}")
    
    # Print the total number of messages sent
    print(f"Total Messages: {msg_count}")
    
    # Print a separator
    print("------------------------------------------------")
    
    # Write the result to a file
    write_result()

def write_result():
    """
    Writes the result of the simulation to a file.

    The result includes the simulation title, the last time the simulation ran,
    and the total number of messages sent.

    The file is located at '/Users/opias/Desktop/a_sencron_bfs_algorithm/result.txt'.
    """
    while True:
        try:
            # Open the file in append mode
            with open('output.txt', 'a+') as f:
                # Write the result to the file
                f.write(f"{running_sim.title}, {last_time}, {msg_count}\n")
                # Close the file
                f.close()
                # Exit the loop
                break
        except:
            # If an exception occurs, wait for 3 seconds and try again
            time.sleep(3)
            continue
    