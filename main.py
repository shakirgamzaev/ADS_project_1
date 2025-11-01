from MinHeap import MinHeap
from MaxPairingHeap import MaxPairingHeap
from Flight import Flight, FlightState
from FlightHelpers import FlightHelpers

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
        
    # helper function to print flights that had updated ETAs 
    #(flight_id, flight.eta)
    def print_updated_etas(self, updated_flights: list[tuple[int, int]]):
        final_text = "Updated ETAs: ["
        for i in range(len(updated_flights)):
            flight_id, eta = updated_flights[i]
            string = f"{flight_id}: {eta}"
            if i != len(updated_flights) - 1:
                string += ", "
            final_text += string
        final_text += "]"
        print(final_text)
    
    
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
            if flight_id not in self.active_flights:
                continue #skip if already removed
            
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
            
        #Promotion step
        for flight_id, flight in list(self.active_flights.items()):
            if flight.state == FlightState.SCHEDULED and flight.start_time <= current_time:
                flight.state = FlightState.IN_PROGRESS
                if flight_id in self.handles:
                    self.handles[flight_id]["state"] = FlightState.IN_PROGRESS    
          
          
    
         
            
    def reschedule_unsatisfied_flights(self, new_current_time: int, print_updates: bool = True):
        
        #collect unsatisifed flights
        unsatisfied_flights: list[Flight] = FlightHelpers.collect_unsatisfied_flights(new_current_time, self.active_flights)

        #use this dict to store old ETA for each flight, what will be required for comparing if some ETAs changed
        old_etas: dict[int, int] = FlightHelpers.store_old_etas(unsatisfied_flights)
        
        
        #Step 3: Rebuild runway pool
        occupied_runways: dict[int, int] = {} # (key: runway_id) : (value: nextFreeTime)
        for flight_id, flight in self.active_flights.items():
            if flight.state == FlightState.IN_PROGRESS:
                occupied_runways[flight.runway_id] = flight.eta
        
        fresh_runway_pool = FlightHelpers.rebuild_runway_pool(self.runway_pool, occupied_runways, new_current_time)
        
        #replace old runway pool with a new one
        self.runway_pool = fresh_runway_pool
        
        #step 4: rebuild a pending queues flight 
        fresh_pending_queue = FlightHelpers.rebuild_pending_queue_flights(unsatisfied_flights, self.handles)
        
        self.pending_flights = fresh_pending_queue

        #step 5: greedy scheduling
        #loop while the pendling_flights queue is not empty
        FlightHelpers.greedy_schedule_flights(self.pending_flights, self.runway_pool, new_current_time, self.timetable, self.handles)
         
           
        #step 6: print flights with ETAs that changed, if print flag is true
        if print_updates is True:
            updated_flights = []
            for flight_id, old_eta in old_etas.items():
                flight = self.active_flights[flight_id]
                if flight.eta != old_eta:
                     updated_flights.append((flight_id, flight.eta))
                
            if len(updated_flights) > 0:
                updated_flights.sort()
                self.print_updated_etas(updated_flights)
            
            
                
     
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
     
   
    
    def submit_flight(self, flight_id: int, airline_id: int, submit_time: int, priority: int, duration: int):
        # Step 1: Advance time and settle any completions and reschedule
        self.settle_completions(submit_time)
        self.reschedule_unsatisfied_flights(submit_time)
        
        # Step 2: Check for duplicate flight_id
        if flight_id in self.active_flights:
            print("Duplicate FlightID")
            return
        
        # Step 3: Create new Flight object
        new_flight = Flight(flight_id, airline_id, submit_time, priority, duration)
        
        # Step 4: Add to active_flights (master registry)
        self.active_flights[flight_id] = new_flight
        
        # Step 5: Add to airline_index
        if airline_id not in self.airline_index:
            self.airline_index[airline_id] = set()
        self.airline_index[airline_id].add(flight_id)
        
        # Step 6: Add to pending_flights (MaxPairingHeap)
        key = (priority, -submit_time, -flight_id)
        pairing_node = self.pending_flights.push(key=key, payload=new_flight)
        new_flight.pairing_heap_node = pairing_node
        
        # Step 7: Add to handles
        self.handles[flight_id] = {
            "state": FlightState.PENDING,
            "pairingNode": pairing_node
        }
        
        # Step 8: Update current_time and reschedule to try to assign the new flight
        self.current_time = submit_time
        self.reschedule_unsatisfied_flights(submit_time)
        
        # Step 9: Print the result
        flight = self.active_flights[flight_id]
        if flight.eta != -1:
            print(f"Flight {flight_id} scheduled - ETA: {flight.eta}")
        else:
            # In case flight was not scheduled, safety precaution
            print(f"Flight {flight_id} is pending")


    #TODO: might need to delete airline later at step 5
    def cancel_flight(self, flight_id: int, new_current_time: int):
        self.settle_completions(new_current_time)
        self.reschedule_unsatisfied_flights(new_current_time, print_updates=False)
        self.current_time = new_current_time
        
        #if a flight does not exist in the system, print that it does not exist
        if flight_id not in self.active_flights:
            print(f"Flight {flight_id} does not exist")
            return
         
        flight = self.active_flights[flight_id] 
        
        if flight.state == FlightState.IN_PROGRESS or flight.state == FlightState.LANDED:
            print(f"Cannot cancel: Flight {flight_id} has already departed")
            return
        
        #TODO: remove in final code , defensive check 
        if flight.state == FlightState.SCHEDULED and flight.start_time <= new_current_time:
            print(f"Cannot cancel. Flight {flight_id} already departed")
            return
        
        #remove from pending max pairing heap
        if flight.state == FlightState.PENDING and flight.pairing_heap_node is not None:
            self.pending_flights.erase(flight.pairing_heap_node)
        
        #remove from active flights
        del self.active_flights[flight_id]
        
        airline_id = flight.airline_id
        if airline_id in self.airline_index:
            self.airline_index[airline_id].discard(flight_id)

        #remove from handles
        if flight_id in self.handles:
            del self.handles[flight_id]
            
        print(f"Flight {flight_id} has been canceled")
        
        self.reschedule_unsatisfied_flights(new_current_time)

        


#main program entry point
if __name__ == "__main__":
    flight_scheduler = FlightScheduler() # initialize global flight scheduler class that keeps track of all the data needed
    flight_scheduler.initialize(3)
    flight_scheduler.submit_flight(501, 20, 0, 8, 4)
    flight_scheduler.submit_flight(502, 21, 0, 7, 6)
    flight_scheduler.submit_flight(503, 22, 0, 7, 5)
    flight_scheduler.submit_flight(510, 23, 0, 9, 3)
    flight_scheduler.submit_flight(511, 23, 0, 9, 3)
    flight_scheduler.submit_flight(504, 24, 0, 6, 4)
    flight_scheduler.cancel_flight(505,7)
    
        
