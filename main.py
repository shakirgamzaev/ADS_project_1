from minHeap import MinHeap
from maxPairingHeap import MaxPairingHeap

#Central piece of the entire program. This class has all of the 6 data structures required for the project, as well as all of the function implementations to make the program run

class FlightScheduler:
    def __init__(self):
        self.current_time = 0 # system time that a flight scheduler keeps track of
        self.pending_flights = MaxPairingHeap() # a max pairing heap queue of flights that are in PENDING state
        self.runway_pool: MinHeap = MinHeap() # a pool of availble runways, initilazed at program start
        self.active_flights = {} # hash table that stores all flights that are in ACTIVE state, with key being flightID
        self.timetable: MinHeap = MinHeap() # min heap of scheduled flights
        self.airline_index = {}
        self.handles = {} 
       
    
    def settle_completions(self, current_time: int):
        #collect all flights that should complete
        completed_flights = []
        
        while len(self.timetable.nodes) > 0:
            popped_flight = self.timetable.peek_min()
            eta, flight_id = popped_flight.key
            
            if eta > current_time:
                break #No more flights to pop
            #remove the flight from the timetable queue
            self.timetable.remove_min()
            completed_flights.append((eta, flight_id))
        
            

       
    def initialize(self, count_runways: int):
        if count_runways <= 0:
            print("Invalid input.")
            return
        self.current_time = 0
        self.pending_flights = MaxPairingHeap()
        self.runway_pool = MinHeap()
        self.active_flights = {}
        self.timetable = MinHeap() # min heap of scheduled flights
        self.airline_index = {}
        self.handles = {} 
        
        #initilaize all runways by incrementing id's
        for i in range(1, count_runways + 1):
            new_runway = MinHeap.Node(key=(0, i), payload={"runwayID": i, "nextFreeTime" : 0}) # key structure: (nextFreeTime, runwayID)
            self.runway_pool.insert_node(new_runway)
        print(f"{count_runways} Runways are now available")
        
    





#main program entry point
if __name__ == "__main__":
    flight_scheduler = FlightScheduler() # initialize global flight scheduler class that keeps track of all the data needed
    flight_scheduler.initialize(3)
    
    
        
