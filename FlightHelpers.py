from Flight import Flight
from Flight import FlightState
from MinHeap import MinHeap
from MaxPairingHeap import MaxPairingHeap

class FlightHelpers:
    
    #method that collects all unsatisfied flights in a list
    @staticmethod
    def collect_unsatisfied_flights(new_current_time: int, active_flights: dict[int, Flight]):
        """method that collects all unsatisfied flights in a list"""
        unsatisfied_flights: list[Flight] = []
        
        for flight_id, flight in active_flights.items():
            if flight.state == FlightState.PENDING:
                unsatisfied_flights.append(flight)
            elif flight.state == FlightState.SCHEDULED and new_current_time < flight.start_time:
                unsatisfied_flights.append(flight) 
        return unsatisfied_flights
    
    @staticmethod
    def store_old_etas(unsatisfied_flights: list[Flight]):
        """collects old_etas of all flights to be later used for comparison if etas of them changed"""
        
        old_etas = {}
        
        for flight in unsatisfied_flights:
            if flight.eta != -1: #-1 means that the flight was never scheduled
                old_etas[flight.flight_id] = flight.eta
            # clear all previous assignments
            flight.runway_id = -1
            flight.start_time = -1
            flight.eta = -1
            flight.state = FlightState.PENDING
            flight.pairing_heap_node = None
        
        return old_etas
    
    @staticmethod
    def rebuild_runway_pool(runway_pool: MinHeap, 
                            occupied_runways: dict[int, int], 
                            new_current_time: int):
        """
        Rebuilds run way pool with new next_free_times if necessary
        Args:
            runway_pool: Current MinHeap of runways
            occupied_runways: Dict mapping runway_id -> nextFreeTime for IN_PROGRESS flights
            new_current_time: Current system time
            
        Returns:
            MinHeap: Fresh runway pool with correct nextFreeTime for each runway
        """
        
        fresh_runway_pool = MinHeap()
        
        #iterate through all current runway pools
        #and assign next_free_time to current_time only to runways that are not in occupied runways, or in other words free
        for node in runway_pool.nodes:
            runway_id = node.payload["runwayID"]
            next_free_time = -1
            if runway_id in occupied_runways:
                next_free_time = occupied_runways[runway_id]
            else:
                next_free_time = new_current_time
            
            new_runway_node = MinHeap.Node(key= (next_free_time, runway_id),
                                           payload= {"runwayID": runway_id, "nextFreeTime": next_free_time})
            fresh_runway_pool.insert_node(new_runway_node)
            
        return fresh_runway_pool
    
    @staticmethod
    def rebuild_pending_queue_flights(unsatisfied_flights: list[Flight], handles: dict):
        """rebuilds a pending flights queue updating handles data stucture """
        fresh_pending_queue = MaxPairingHeap()
        
        for flight in unsatisfied_flights:
            #Add to fresh_pending_queue
            key = (flight.priority, -flight.submit_time, -flight.flight_id)
            max_pairing_node = fresh_pending_queue.push(key= key, payload= flight)
            
            flight.pairing_heap_node = max_pairing_node
            if flight.flight_id not in handles:
                handles[flight.flight_id] = {}
            handles[flight.flight_id]["state"] = FlightState.PENDING
            handles[flight.flight_id]["pairingNode"] = max_pairing_node
        
        return fresh_pending_queue
    
    @staticmethod
    def greedy_schedule_flights(pending_flights: MaxPairingHeap, runway_pool: MinHeap, new_current_time: int, timetable: MinHeap, handles: dict):
        while pending_flights.node_count > 0:
            flight_node = pending_flights.pop()
            flight: Flight = flight_node.payload
            
            #Choose runway with earlierst nextFreeTime
            runway_node: MinHeap.Node = runway_pool.remove_min()
            runway_id = runway_node.payload["runwayID"]
            runway_next_free_time = runway_node.payload["nextFreeTime"]
            
            #assign times
            start_time = max(new_current_time, runway_next_free_time)
            eta = start_time + flight.duration
            
            flight.runway_id = runway_id
            flight.start_time = start_time
            flight.eta = eta
            flight.state = FlightState.SCHEDULED
            flight.pairing_heap_node = None
            
            #Update handles
            if flight.flight_id in handles:
                handles[flight.flight_id]["state"] = FlightState.SCHEDULED
                handles[flight.flight_id]["pairingNode"] = None
            
            runway_node.payload["nextFreeTime"] = eta
            runway_node.key = (eta, runway_id)
            runway_pool.insert_node(runway_node)
            
            #add to timetable queue
            timetable_node = MinHeap.Node(key= (eta, flight.flight_id), payload={"runwayID": runway_id})
            
            timetable.insert_node(timetable_node)
     
    @staticmethod       
    def change_priority_of_flight(
        handles: dict,
        pending_flights: MaxPairingHeap,
        flight: Flight, 
        new_priority: int):
        
        old_priority = flight.priority
        
        if flight.state == FlightState.PENDING and flight.pairing_heap_node is not None:
            if new_priority > old_priority:
                #use increase key operation of max paring heap
                new_key = (new_priority, -flight.submit_time, -flight.flight_id)
                pending_flights.increase_key(flight.pairing_heap_node, new_key)
            else:
                #priority decreased - perform erase old node and push new
                pending_flights.erase(flight.pairing_heap_node)
                new_key = (new_priority, -flight.submit_time, -flight.flight_id)
                pairing_node = pending_flights.push(key=new_key, payload=flight)
                flight.pairing_heap_node = pairing_node
                handles[flight.flight_id]["pairingNode"] = pairing_node
        
        flight.priority = new_priority
            
                
             