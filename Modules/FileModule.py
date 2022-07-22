import os, pathlib

class File:
    
    #Type constants for create_or_validate func
    TYPE_DIR = "dir"
    TYPE_FILE = "file"
    
    def __init__(self):
        pass
    
    #The method below checks whether a certain directory exists in the CURRENT directory.
    #If it doesn't it creates the specific directory
    @staticmethod
    def create_or_validate(additional_dir):
        current_path = pathlib.Path().resolve()
        final_path = os.path.join(current_path, additional_dir)
               
        if not os.path.isdir( final_path ):
            os.mkdir( additional_dir )
            

    #Returns the current directory joined with the parameter
    @staticmethod
    def get_current_dir(additional_dir):
        current_path = pathlib.Path().resolve()
        final_path = os.path.join(current_path, additional_dir)
        return final_path
    
    @staticmethod
    def check_file_existence( dir, filename):
        file_dir = os.path.join( dir, filename)
        return os.path.isfile( file_dir )