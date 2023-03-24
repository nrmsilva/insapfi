import requests
import concurrent.futures
import threading
import time

def task(file_name):
    print(f'start thread for {file_name}')
    start = time.perf_counter()
    url = "http://localhost:8181/ords/maj/file/upload_download/"
    
    payload={}
    files=[
    ('file',('Eficiencia_Entrepostos_Worten_MAJ.csv',
             open('others/scripts/test_files/Eficiencia_Entrepostos_Worten_MAJ.csv','rb'),'text/csv'))
    ]
    headers = {
    'filename': f'{file_name}'
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    end = time.perf_counter()
    print(f"{file_name} - Elapsed time - " + time.strftime("%H:%M:%S.{}".format(str((end - start) % 1)[2:])[:15], time.gmtime((end - start))))
    print(response.text)

print('init')
num_workers=10
with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as pool:
    futures = []
    for i in range(0,num_workers):
        file_name = f'test_{i}.csv'
        futures.append(pool.submit(task, file_name))
while True:
    try:
        time.sleep(.1)
        terminated = [future.done() for future in futures]
        if False not in terminated:
            break
    except KeyboardInterrupt:
        print('Main interrupted! Terminating all threads. Exiting.')
        pool.shutdown(wait=True, cancel_futures=True)