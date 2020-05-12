from Queue.arrays import Array
from Queue.arrayqueue import ArrayQueue
from simplepeople import Passenger, TicketAgent
from random import random


class TicketCounterSimulation:
    def __init__(self, numAgents, numMinutes, betweenTime, serviceTime):
        self._arriveProb = 1.0 / betweenTime
        self._serviceTime = serviceTime
        self._numMinutes = numMinutes

        self._passengerQ = ArrayQueue()
        self._theAgents = Array(numAgents)
        for i in range(numAgents):
            self._theAgents[i] = TicketAgent(i+1)

        self._totalWaitTime = 0
        self._numPassengers = 0
        self.passenger_id = 1

    def _handleArrival(self, curTime):
        self._totalWaitTime += len(self._passengerQ)
        if random() < self._arriveProb:
            passenger = Passenger(self.passenger_id, curTime)
            self._passengerQ.add(passenger)
            print(f'Time {curTime}: Passenger {passenger.idNum()} has arrived.')
            self._numPassengers += 1
            self.passenger_id += 1
            # print(len(self._passengerQ))

    def _handleBeginService(self, curTime):
        for agent in self._theAgents:
            if agent.isFree():
                # print(self._passengerQ._size)
                if len(self._passengerQ) > 0:
                    # print(1)
                    # print(self._passengerQ)

                    passenger = self._passengerQ.pop()
                    agent.startService(passenger,
                                       curTime + self._serviceTime)
                    print(
                        f'Time {curTime}: Agent {agent.idNum()} started serving passenger {passenger.idNum()}.')

    def _handleEndService(self, curTime):
        for agent in self._theAgents:
            if agent.isFinished(curTime):
                passenger = agent.stopService()
                print(
                    f'Time {curTime}: Agent {agent.idNum()} stopped serving passenger {passenger.idNum()}.')
                print(
                    f'Time {curTime}: Passenger {passenger.idNum()} has departed.')

        # Run the simulation using the parameters supplied earlier.

    def run(self):
        for curTime in range(self._numMinutes + 1):
            self._handleArrival(curTime)
            self._handleBeginService(curTime)
            self._handleEndService(curTime)

    def printResuts(self):
        numServed = self._numPassengers - len(self._passengerQ)
        avgWait = float(self._totalWaitTime) / numServed
        print()
        print("Number of passengers served = ", numServed)
        print("Number of passengers remaining in line = %d" %
              len(self._passengerQ))
        print("The average wait time was %4.2f minutes." % avgWait)
