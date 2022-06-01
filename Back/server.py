from multiprocessing import cpu_count, freeze_support

import uvicorn

def start_server(host="127.0.0.1",
                 port=8080,
                 num_workers=4,
                 loop="asyncio",
                 reload=True):

    uvicorn.run("web_server:app",
                host=host,
                port=port,
                workers=num_workers,
                loop=loop,
                reload=reload)

if __name__ == "__main__":
    freeze_support()  # Needed for pyinstaller for multiprocessing on WindowsOS
    num_workers = int(cpu_count() * 0.75)
    start_server(num_workers=num_workers)