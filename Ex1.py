import sys
import requests
import asyncio
import aiohttp
import threading
import time
from multiprocessing import Process, Pool


def get_name(path):
    name_array = path.split('.')
    name_array2 = name_array[len(name_array)-2].split('/')
    name = name_array2[len(name_array2)-1] + '.' + \
        name_array[len(name_array)-1]
    return name


def queue(pathes, names):
    start_time = time.time()
    for i in range(len(pathes)):
        start_time_img = time.time()
        img = requests.get(pathes[i])
        out = open("./images/"+names[i], "wb")
        out.write(img.content)
        out.close()
        print(
            f"Downloaded image #{i} in {time.time() - start_time_img:.2f}seconds")
    print(f"Downloaded by queue in {time.time() - start_time:.2f}seconds")


def download(path, name, i):
    start_time_img = time.time()
    img = requests.get(path)
    out = open("./images/"+name, "wb")
    out.write(img.content)
    out.close()
    print(
        f"Downloaded image #{i} in {time.time() - start_time_img:.2f}seconds")


async def download_async(path, name, i):
    start_time_img = time.time()
    async with aiohttp.ClientSession() as session:
        async with session.get(path) as response:
            img = await response.read()
            with open("./images/"+name, 'wb') as file:
                file.write(img)
    print(
        f"Downloaded image #{i} in {time.time() - start_time_img:.2f}seconds")


async def async_method(pathes, names):
    tasks = []
    start_time = time.time()
    for i in range(len(pathes)):
        task = asyncio.ensure_future(download_async(pathes[i], names[i], i))
        tasks.append(task)
    await asyncio.gather(*tasks)
    print(
        f"Downloaded by async method in {time.time() - start_time:.2f}seconds")


def threads(pathes, names):
    threads = []
    start_time = time.time()
    for i in range(len(pathes)):
        thread = threading.Thread(
            target=download, args=[pathes[i], names[i], i])
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    print(f"Downloaded by threading in {time.time() - start_time:.2f}seconds")


def processes(pathes, names):
    processes = []
    start_time = time.time()
    if __name__ == '__main__':
        for i in range(len(pathes)):
            process = Process(target=download, args=[pathes[i], names[i], i])
            processes.append(process)
            process.start()
        for process in processes:
            process.join()
        print(
            f"Downloaded by multiprocessing in {time.time() - start_time:.2f}seconds")


# pathes = ['https://images.wallpaperscraft.ru/image/single/devushka_trava_gorod_213102_2560x1600.jpg', 'https://images.wallpaperscraft.ru/image/single/bmw_k100_mototsikl_bajk_123991_2560x1600.jpg',
#           'https://images.wallpaperscraft.ru/image/single/gorod_vid_sverhu_doroga_156925_2560x1600.jpg', 'https://images.wallpaperscraft.ru/image/single/planety_galaktika_zvezdy_146448_2560x1600.jpg']

if __name__ == "__main__":
    names = []
    for i in range(2, len(sys.argv)):
        names.append(get_name(sys.argv[i]))
    pathes = []
    for i in range(2, len(sys.argv)):
        pathes.append(sys.argv[i])
    if sys.argv[1] == '1':
        queue(pathes, names)
    elif sys.argv[1] == '2':
        threads(pathes, names)
    elif sys.argv[1] == '3':
        processes(pathes, names)
    elif sys.argv[1] == '4':
        loop = asyncio.get_event_loop()
        loop.run_until_complete(async_method(pathes, names))
    else:
        print("Incorrect input!")

# Аругменты для ввода:
# 1 https://images.wallpaperscraft.ru/image/single/devushka_trava_gorod_213102_2560x1600.jpg https://images.wallpaperscraft.ru/image/single/bmw_k100_mototsikl_bajk_123991_2560x1600.jpg https://images.wallpaperscraft.ru/image/single/gorod_vid_sverhu_doroga_156925_2560x1600.jpg https://images.wallpaperscraft.ru/image/single/planety_galaktika_zvezdy_146448_2560x1600.jpg
