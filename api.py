import itertools
import requests
from queue import Queue
import time
import threading
import os.path
from tqdm import tqdm


class cdsapi_p:
    def __init__(self, keys, url="https://cds.climate.copernicus.eu/api/v2"):
        self._url = url
        self._params = []
        self._init_auths(keys)

    def key2auth(self, key):
        return tuple(key.split(":", 2))

    def _init_auths(self, keys):
        keys = set(keys)
        auths = [self.key2auth(i) for i in keys]
        self._nauth = len(auths)
        self._auths = itertools.cycle(enumerate(auths))

    def add(self, param):
        self._params.append(param)

    def count(self):
        return len(self._params)

    def Poster(self, overwrite):
        # item = self.q_c2p.pop()
        # name, param, out, auth = *item[0], item[1]
        idx, auth = next(self._auths)
        for param in self._params:
            name, request, outfile = param
            if os.path.isfile(outfile) and not overwrite:
                continue

            url = f"{self._url}/resources/{name}"

            resp = requests.post(url, json=request, auth=auth)
            json = resp.json()

            if resp.status_code == 200:
                item = (json["location"], outfile)
                self._qloc.put(item)
            elif resp.status_code == 202:
                item = (auth, json["request_id"], outfile)
                # self.q_rid.put(item)
                self._tasks[idx].put(item)
                idx, auth = next(self._auths)

        for i in self._tasks:
            i.put(self._sentinel)

    def Checker(self, idx):
        while True:
            item = self._tasks[idx].get()
            if item == self._sentinel:
                with self.__lock:
                    self.__flag += 1
                    if self.__flag == self._nauth:
                        self._qloc.put(self._sentinel)
                break

            while True:
                auth, request_id, outfile = item
                url = f"{self._url}/tasks/{request_id}"

                resp = requests.get(url, auth=auth)
                json = resp.json()

                if json["state"] == "completed":
                    item = (json["location"], outfile)
                    self._qloc.put(item)
                    break
                else:
                    time.sleep(0.5)

    def Downloader(self, pbar):
        while True:
            item = self._qloc.get()
            if item == self._sentinel:
                self._qloc.put(item)
                break
            location, outfile = item

            with requests.get(location, stream=True) as r:
                r.raise_for_status()
                with open(outfile, "wb") as f:
                    for chunk in r.iter_content(chunk_size=1024):
                        f.write(chunk)

            pbar.update(1)
            pbar.set_postfix_str(f"lastest: {outfile}")

    def run(self, overwrite=False, workers=None):
        pbar = tqdm(total=self.count(), desc="Download")

        if workers is None or workers > self._auths:
            workers = self._nauth

        self._qloc = Queue()
        self._tasks = [Queue() for _ in range(self._nauth)]
        self._sentinel = object()
        self.__lock = threading.Lock()
        self.__flag = 0

        # create threads
        d_threads = []
        for _ in range(workers):
            d_thread = threading.Thread(target=self.Downloader, args=(pbar,))
            d_threads.append(d_thread)
            d_thread.start()

        c_threads = []
        for i in range(self._nauth):
            c_thread = threading.Thread(target=self.Checker, args=(i,))
            c_threads.append(c_thread)
            c_thread.start()

        p_thread = threading.Thread(target=self.Poster, args=(overwrite,))
        p_thread.start()

        # join threads
        for d_thread in d_threads:
            d_thread.join()

        for c_thread in c_threads:
            c_thread.join()

        p_thread.join()
