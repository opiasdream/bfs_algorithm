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

    



    
"""
Düğüm sayısındaki değişimin algoritma mesaj ve zaman ihtiyaçlarını nasıl etkilediği

Haberleşme menzilinin değişiminin mesaj ve zaman ihtiyaçlarını nasıl etkilediği


Ilk analiz i ̧cin haberle ̧sme menzili 75’te sabit tutulup, d ̈u ̆g ̈um sayılarını
49, 100, 144, 197, 256 olacak  ̧sekilde farklı topolojilerde test etmeniz gerekmektedir. Her bir d ̈u ̆g ̈um
sayısı i ̧cin testleri en az 30 farklı ba ̆glı topoloji  ̈uzerinde  ̧calı ̧smanız gerekmektedir. 

Aynı  ̧sekilde ikinci analiz i ̧cin de, d ̈u ̆g ̈um sayısını 256’da sabit tutup,
haberle ̧sme menzili 75, 100, 125 ve 150 olacak
 ̧sekilde farklı topolojiler ile testleri ger ̧cekle ̧stirmeniz gerekmektedir. Her haberle ̧sme menzili ii ̧cn ilk
analizde oldu ̆gu gibi, testleri en az 30 farklı ba ̆glı topoloji  ̈uzerinde  ̧calı ̧stırmanız gerekmektedir. 

Hertopoloji i ̧cin algoritmaların ne kadar s ̈ure ve mesaj kullandı ̆gını  ̈ol ̧cmeniz gerekmektedir. Raporlama
kısmında bu topolojilerin sonu ̧clarının ortalamalarını kullanmanız gerekmektedir. Testleri yaparken
mesajların iletim s ̈uresini rastgele olarak de ̆gi ̧stirmeniz gerekmektedir. Bunun i ̧cin source klas ̈or ̈unde
bulunan config.py dosyası i ̧cerisindeki SIM MESSAGGING DELAY TYPE de ̆gi ̧skenini random yap-
manız yeterlidir.
"""


# def create_simulators(titles: list[str], cell_count: int) -> list[DawnSimVis.Simulator] :
#     dx = cell_count * CELL_EDGE_LEN + PADDING
#     dy = cell_count * CELL_EDGE_LEN + PADDING
#     size = (dx, dy)
#     return [DawnSimVis.Simulator(DURATION, TIMESCALE, 0, size, VISUAL, title) for title in titles]


    

           
# def create_topology():

#     cell_count = 7
#     print(f"{cell_count*cell_count} düğümlük topoloji oluşturma")
#     count = 0


    
#     seedList = []

#     while True:

#         tempList = []
#         sim = DawnSimVis.Simulator(
#             duration=1,
#             timescale=1,
#             visual=True,
#             terrain_size=(650, 650),
#             title=f'{cell_count}x{cell_count} Sim',)

#         for x in range(cell_count):
#             for y in range(cell_count):
#                 px = PADDING + x * CELL_EDGE_LEN + random.uniform(-20, 20)
#                 py = PADDING + y * CELL_EDGE_LEN + random.uniform(-20, 20)
#                 sim.add_node(SyncBFSNode, pos=(px, py), tx_range = 75)
#                 tempList.append((px, py))

#         action = input("Enter 's' to save, 'c' to continue or 'q' to quit: ")
#         if action == 's':
#             seedList.append(tempList)
#             count += 1
#             print(f"Eklendi, Topoloji sayısı: {count}")
#             sim.add_node
#         elif action == 'c':
#             tempList.clear()
#             continue
#         elif action == 'q':
#             break
#         else:
#             print('invalid')
    
#     print(f"Kayıt ediliyor..")
    
#     with open ('seeds.txt', 'w') as f:
#         for seeds in seedList:
#             f.write(f"{seeds}\n")
#         f.close()