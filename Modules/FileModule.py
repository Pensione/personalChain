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
    def create_or_validate( path):          
        if not os.path.isdir( path ):
            os.mkdir( path )
            
    @staticmethod
    def check_file_existence( dir, filename):
        file_dir = os.path.join( dir, filename)
        return os.path.isfile( file_dir )