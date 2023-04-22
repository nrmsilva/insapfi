import requests
import concurrent.futures
import threading
import time

def task(file_name):
    print(f'start thread for {file_name}')
    start = time.perf_counter()
    url = "https://ordstst.mch.moc.sgps/cfo02r/tst/file/upload_download/"
    with open('C:\\Users\\DC_FRAMOS\\git\\test\\Eficiencia_Entrepostos_Worten_MAJ_small.csv','rb') as f:
        data = f.read()

    payload=data
    headers = {
        'filename': 'test.csv',
        'ignore_erros': '0',
        'Content-Type': 'text/csv'
    }
    try:
        response = requests.request("POST", url, headers=headers, data=payload, verify=False)
    except Exception as e:
        print(e)

    end = time.perf_counter()
    print(f"{file_name} - Elapsed time - " + time.strftime("%S,{}".format(str((end - start) % 1)[2:])[:15], time.gmtime((end - start))))
    print(response.text)
    

print('init')
num_workers=20
with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as pool:
    futures = []
    for i in range(0,num_workers):
        file_name = f'test_{i}.csv'
        futures.append(pool.submit(task, file_name))
while True:
    try:
        time.sleep(.1)
        terminated = [future.done() for future in futures]
        print(terminated)
        if False not in terminated:
            break
    except KeyboardInterrupt:
        print('Main interrupted! Terminating all threads. Exiting.')
        pool.shutdown(wait=True, cancel_futures=True)