#class that represents a flight request object
from enum import Enum

class FlightState(Enum):
    PENDING = "PENDING"
    SCHEDULED = "SCHEDULED"
    IN_PROGRESS = "IN_PROGRESS"
    LANDED = "LANDED"

#class that represents a flight request object
class Flight:
    
    def __init__(self, flight_id: int, airline_id: int, submit_time: int, priority: int, duration: int):
        self.flight_id = flight_id
        self.airline_id = airline_id
        self.submit_time = submit_time
        self.priority = priority
        self.duration = duration
        
        #scheduling information that is initially unassigned, indicated by -1
        self.runway_id = -1
        self.start_time = -1
        self.eta = -1
        
        self.state: FlightState = FlightState.PENDING
        self.pairing_heap_node = None # stores the reference to a flight in the max pairing heap node.
        
        
        