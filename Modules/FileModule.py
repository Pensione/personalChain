import os, pathlib

class File:
    
    def __init__(self):
        pass
    
    #The method below checks whether a certain directory exists in the CURRENT directory.
    #If it doesn't it creates the specific directory
    @staticmethod
    def validate_directory(additional_dir):
        current_path = pathlib.Path().resolve()
        final_path = os.path.join(current_path, additional_dir)
                 
        if not os.path.isdir( final_path ):
            os.mkdir( additional_dir )
            
            
    #Returns the current directory joined with the parameter
    @staticmethod
    def get_directory(additional_dir):
        current_path = pathlib.Path().resolve()
        final_path = os.path.join(current_path, additional_dir)
        
        return final_path