from minHeap import MinHeap
from maxPairingHeap import MaxPairingHeap

class FlightScheduler:
    def __init__(self):
        self.current_time = 0 # system time that a flight scheduler keeps track of
        self.pending_flights = None # a max pairing heap of 
        self.runway_pool: MinHeap = None # a pool of availble runways, initilazed at program start
        
    def initialize(self, count_runways):
        if count_runways <= 0:
            print("Invalid input.")
            return
        self.current_time = 0
        self.runway_pool = MinHeap()
        #initilaize all runways by incrementing id's
        for i in range(1, count_runways + 1):
            new_runway = MinHeap.Node(key=(0, i), payload={"runwayID": i, "nextFreeTime" : 0}) # key structure: (nextFreeTime, runwayID)
            self.runway_pool.insert_node(new_runway)
        print(f"{count_runways} Runways are now available")
        
    

#main program entry point
if __name__ == "__main__":
    flight_scheduler = FlightScheduler() # initialize global flight scheduler class that keeps track of all the data needed
    flight_scheduler.initialize(-5)
    
        
