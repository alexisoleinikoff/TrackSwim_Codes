from threading import Thread, active_count
from queue import Queue
import  time

q = Queue()

a = 0
chrono = time.time()
update_thread = True

def readTag():
    test()
    time.sleep(2)
    q.put(10)

def test():
    print('lancé')


while a < 30:
    if update_thread:
        t = Thread(target=readTag)
        t.start()
        update_thread = False

    if time.time() - chrono > 1:
        chrono = time.time()
        print("1 seconde passée")

    if q.qsize() != 0:
        a = a + q.get()
        print("Thread actifs : ", active_count())
        update_thread = True


        

    
