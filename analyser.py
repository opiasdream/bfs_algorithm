import json

data = {}

with open('output.txt', 'r') as f:
    for line in f:
        ls = line.split(",")
        title = ls[0].split(' ')
        test_id = title[0] # cell count and tx range
        sim_id = title[1] # unique simulator id
        bfs_type = title[2] # Synchronous or Asynchronous
        sim_res = { bfs_type : {'test_id' : test_id, 'bfs_type' : bfs_type,
                            'time': ls[1], 'msg_count':ls[2].replace('\n', '')} }
        if list(data.keys()).count(sim_id) == 0:
            data[sim_id] = sim_res
        else:
            data[sim_id][bfs_type] = list(sim_res.values())[0]
                  
length = len(data.keys())
sync_total_time = 0.0
sync_total_msg = 0
async_total_time = 0.0
async_total_msg = 0

test_id_ls:list = list(list(data.values())[0].values())[0]['test_id'].split('x')
cell_count = test_id_ls[0]
tx_range = test_id_ls[1]


for i in data.values():
    for j in i.values():
        if(j["bfs_type"] == "Synchronous"):
            sync_total_time += float(j["time"])
            sync_total_msg += int(j["msg_count"])
        else:
            async_total_time += float(j["time"])
            async_total_msg += int(j["msg_count"])

print("--------------------------------------")
print(f"Node: {cell_count}x{cell_count} | Distance: {tx_range} Test Result")
print("\n")
print(f"Test Count: {length}")
print(f"Sync Msg Average: {sync_total_msg/length}")
print(f"Sync Time Average: {sync_total_time/length}" )
print(f"Async Msg Average: {async_total_msg/length}")
print(f"Async Time Average: {async_total_time/length}")
print("--------------------------------------\n")


with open(f'{'x'.join(test_id_ls)}_results.txt', 'w') as f:
        f.write(json.dumps(data, indent=4))

