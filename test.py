from time import sleep
from tqdm import trange, tqdm

for i in tqdm(range(10), desc='Processing', leave=True):
    for j in tqdm(range(5), desc='Sub Processing', leave=False):
        sleep(0.2)