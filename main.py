from minHeap import MinHeap
from maxPairingHeap import MaxPairingHeap
from flight import Flight, FlightState
#Central piece of the entire program. This class has all of the 6 data structures required for the project, as well as all of the function implementations to make the program run

class FlightScheduler:
    def __init__(self):
        self.current_time = 0 # system time that a flight scheduler keeps track of
        self.pending_flights = MaxPairingHeap() # a max pairing heap queue of flights that are in PENDING state
        self.runway_pool: MinHeap = MinHeap() # a pool of availble runways, initilazed at program start
        self.active_flights: dict[int, Flight] = {} # hash table that stores all flights
        self.timetable: MinHeap = MinHeap() # min heap of scheduled flights
        self.airline_index: dict[int, set[int]] = {}
        self.handles = {} 
       
    
    def settle_completions(self, current_time: int):
        #collect all flights that should complete
        completed_flights = []
        
        while len(self.timetable.nodes) > 0:
            popped_flight: MinHeap.Node = self.timetable.peek_min()
            eta, flight_id = popped_flight.key
            
            if eta > current_time:
                break #No more flights to pop
            
            #remove the flight from the timetable queue
            self.timetable.remove_min()
            completed_flights.append((eta, flight_id))
            
        #after flights have been collected in completed_flights, remove them from all data structures
        for eta, flight_id in completed_flights:
            print(f"Flight {flight_id} has landed at time {eta}")
            flight = self.active_flights[flight_id] #get the flight from active_flights dict
            #first delete the flight from active_flights 
            del self.active_flights[flight_id]
            
            #delete flight from airline_index
            airline_id = flight.airline_id
            if airline_id in self.airline_index:
                self.airline_index[airline_id].discard(flight_id)
                #ATENTION!!!!! might need to delete airline if becomes empty
            
            #delete flight from handles 
            if flight_id in self.handles:
                del self.handles[flight_id]
            #print the flight has landed
            
        
        #Promotion step
        for flight_id, flight in list(self.active_flights.items()):
            if flight.state == FlightState.SCHEDULED and flight.start_time <= current_time:
                flight.state = FlightState.IN_PROGRESS
                if flight_id in self.handles:
                    self.handles[flight_id]["state"] = FlightState.IN_PROGRESS    
            
            
    def reschedule_unsatisfied_flights(self, new_current_time: int):
        unsatisifed_flights: list[Flight] = []
        
        for flight_id, flight in self.active_flights.items():
            if flight.state == FlightState.PENDING:
                unsatisifed_flights.append(flight)
            elif flight.state == FlightState.SCHEDULED and new_current_time < flight.start_time:
                unsatisifed_flights.append(flight)   

        old_etas: dict[int, int] = {} #use this dict to store old ETA for each flight, what will be required for comparing if some ETAs changed
        
        for flight in unsatisifed_flights:
            if flight.eta != -1: #-1 means that the flight was never scheduled
                old_etas[flight.flight_id] = flight.eta
            # clear all previous assignments
            flight.runway_id = -1
            flight.start_time = -1
            flight.eta = -1
            flight.state = FlightState.PENDING
            flight.pairing_heap_node = None
        
        #Step 3: Rebuild runway pool
        occupied_runways: dict[int, int] = {} # key: runway_id -> value: nextFreeTime
        for flight_id, flight in self.active_flights.items():
            if flight.state == FlightState.IN_PROGRESS:
                occupied_runways[flight.runway_id] = flight.eta
        
        fresh_runway_pool = MinHeap()
        
        #iterate through all current runway pools
        for node in self.runway_pool.nodes:
            runway_id = node.payload["runwayID"]
            next_free_time = -1
            if runway_id in occupied_runways:
                next_free_time = occupied_runways[runway_id]
            else:
                next_free_time = new_current_time
            
            new_runway_node = MinHeap.Node(key= (next_free_time, runway_id),
                                           payload= {"runwayID": runway_id, "nextFreeTime": next_free_time})
            fresh_runway_pool.insert_node(new_runway_node)
        
        #replace old runway pool with a new one
        self.runway_pool = fresh_runway_pool
            
      
      
     
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
    
    
        
