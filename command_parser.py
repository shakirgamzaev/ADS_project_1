import sys
import re


#function that parses a command line and extracts arguments and a function name. Example: Initialize(3) -> (Initialize, [3]). Return a tuple as you can see
def parse_command(line: str):
    command = line.strip()
    
    #regex that splits a command into function name and arguments
    match = re.match(r'(\w+)\((.*)\)', command)
    if not match:
        return None, None
    
    function_name = match.group(1)
    parameters_string = match.group(2).strip()
    
    parameters: list[int] = []
    
    if parameters_string:
        parameters_list = parameters_string.split(",")
        for parameter in parameters_list:
            parameter = parameter.strip()
            parameters.append(int(parameter))  
    
    return function_name, parameters


#Executes commands that are read from input file. Return True only if command name is Quit, and ends the loops, else returns false and sequence of command executions continues
def execute_command(scheduler, command_name: str, parameters: list):
    
    if command_name == "Initialize":
        scheduler.initialize(parameters[0])
        
    elif command_name == "SubmitFlight":
        scheduler.submit_flight(parameters[0], parameters[1], parameters[2], parameters[3], parameters[4])
    
    elif command_name == "CancelFlight":
        scheduler.cancel_flight(parameters[0], parameters[1])
        
    elif command_name == "Reprioritize":
        scheduler.reprioritize_flight(parameters[0], parameters[1], parameters[2])
        
    elif command_name == "AddRunways":
        scheduler.add_runways(parameters[0], parameters[1])
        
    elif command_name == "GroundHold":
        scheduler.ground_hold(parameters[0], parameters[1], parameters[2])
        
    elif command_name == "PrintActive":
        scheduler.print_active()
    
    elif command_name == "PrintSchedule":
        scheduler.print_schedule(parameters[0], parameters[1])
        
    elif command_name == "Tick":
        scheduler.tick(parameters[0])
        
    elif command_name == "Quit":
        print("Program terminated!!")
        return True
    
    return False

