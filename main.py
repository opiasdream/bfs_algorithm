import uuid, time, random, helper
from source import DawnSimVis
from bfs_nodes import SyncBFSNode, AsyncBFSNode

# Edge length of each cell.
CELL_EDGE_LEN = 60
# Total duration the simulator will operate.
DURATION = 450
# Seconds in real time for 1 second in simulation.
TIMESCALE = 1
# padding around the grid
PADDING = 50

def create_simulator(title:str, cell_count :int, visual:bool) -> DawnSimVis.Simulator:
    dx = cell_count * CELL_EDGE_LEN + PADDING
    dy = cell_count * CELL_EDGE_LEN + PADDING
    return DawnSimVis.Simulator(DURATION, TIMESCALE, 0, (dx, dy), visual, title)


def create_networks(sims: list[DawnSimVis.Simulator],
                    nodes: list[DawnSimVis.BaseNode], 
                    cell_count:int, tx_range:int):

    for x in range(cell_count):
        for y in range(cell_count):
            px = PADDING + x * CELL_EDGE_LEN + random.uniform(-20, 20)
            py = PADDING + y * CELL_EDGE_LEN + random.uniform(-20, 20)

            for idx, sim in enumerate(sims):
                sim.add_node(nodes[idx], pos=(px, py), tx_range = tx_range)

if __name__ == '__main__':

    id = str(uuid.uuid4()).split('-')[0]

    print(f"\n----------------- Iteration {id} -----------------\n")
      
    cell_count = 16

    tx_range = 75

    sync_sim_title = f'{cell_count}x{tx_range} {id} Synchronous BFS Simulator'
    async_sim_title = f'{cell_count}x{tx_range} {id} Asynchronous BFS Simulator'

    sync_sim = create_simulator(sync_sim_title, cell_count, True)
    async_sim = create_simulator(async_sim_title, cell_count, False)

    simsulators = [sync_sim, async_sim]
    
    create_networks(simsulators, [SyncBFSNode, AsyncBFSNode], cell_count, tx_range)

    for sim in simsulators:
        helper.running_sim = sim
        sim.run()