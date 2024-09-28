import threading, multiprocessing, time, math, os

# from threading import Lock,Condition,Thread
from multiprocessing import Process, Lock, Condition, Barrier, Pipe


class Macinatore(Process):

    def __init__(self, min, max, b):

        super().__init__()
        self.min = min
        self.max = max
        self.totale = 0
        self.pipe = b

    def eprimo(self, n):
        if n <= 3:
            return True
        if n % 2 == 0:
            return False
        for i in range(3, int(math.sqrt(n) + 1), 2):
            if n % i == 0:
                return False
        return True

    def contaPrimiSeq(self):

        for i in range(self.min, self.max + 1):

            if (self.eprimo(i)):
                self.totale += 1

    def getTotale(self):
        return self.totale

    def run(self):
        #  self.barriera.info("Start Process",self.min,self.max)
        self.contaPrimiSeq()
        self.pipe.send(self.totale)


class BarrieraMacinatore:

    def contaPrimi(self, MIN, MAX):

        if MAX < MIN:
            return 0

        threadReali = multiprocessing.cpu_count()
        # threadReali = 1
        print(threadReali)
        fetta = (MAX - MIN + 1) // threadReali
        while fetta == 0:
            threadReali -= 1
            fetta = (MAX - MIN + 1) // threadReali

        ciucci = []
        pipes = []
        for i in range(threadReali - 1):
            min = MIN + i * fetta
            max = min + fetta - 1
            pipes.append(Pipe())
            ciucci.append(Macinatore(min, max, pipes[i][1]))
            ciucci[i].start()

        pipes.append(Pipe())
        ciucci.append(Macinatore(MIN + (threadReali - 1) * fetta, MAX, pipes[threadReali - 1][1]))
        ciucci[threadReali - 1].start()
        print("Main thread waiting")

        totale = 0
        for i in range(threadReali):
            totale += pipes[i][0].recv()
        return totale


if __name__ == '__main__':
    start = time.time()
    mac = BarrieraMacinatore()
    print("Primi tra 1'000'000 e 10'000'000: %d" % (mac.contaPrimi(100000, 10000000)))
    elapsed = time.time() - start
    print("Tempo trascorso: %d secondi." % elapsed)