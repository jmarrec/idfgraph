import eppy
from eppy.modeleditor import IDF
import os
import re

# need a file or text_holder to add the log to 
try:
    log_file = open("log.txt", 'a+')
    #log_file.write("Log file created at time %s"%os.time() )
    log_file.close() 

    #return "Creation of log file failed. See Mad Dog for details"


    idf_parser = "" # for global eppy shizam such as idfversion
    version = ""
except:
    print("Failed to initialise the eppy requirements, See Mad Dog for details")

def set_version(v=None):
    """Set the version on the global data doody 
    Args:
        v (string): The version for idf eppy thing
    Returns:
        None
    Raises:
        None
    """
    if v is None:
        log("idf version not found, defaulting to Version 8.2")
        version = 8.2
    if v is not None:
        version = v
        log("idf version %s "%version)


def handle_uploaded_file(f):
    """skeleton file for getting this party started. 

    A file to sporn the import and do stuff process. 

    Args:
        f (file): The user uploaded file

    Returns:
        True or False

     """

    f_name = f.name() 

    log("Importing file: %s and running checks"%f.name())
    
    if runchecks(f_name):
        # get version
        with open(f,'r') as fi:
            for line in fi.readlines():
                result = re.search("Version,\d.\d;", line)
                if result:
                    try:
                        version = re.search(r"\d.\d",line).group(0)
                        set_version(version)
                        return True
                    except:
                        set_version()   # default is 8.2
    else:
        log("idf fails basic validity checks")
        return "checks failed"

def log(txt, f=log_file):
    """Logs the txt argument.
    Args:
        txt (string): Text describing the error, warning or other note
        f (file)
    Returns:
        Nothing
    Raises:
        Nothing

     """
    log_file.write(txt)
    log_file.close()

# function to read the imported idf
def read_idf(f):
    """Read the idf into the database"""
    
    # name of file uploaded
    # user name idf uploader
    # log the user activity
  
# run some checks on the file, to prevent processing malicious/erroneous files

def runchecks(f):
    """Check file for malcious looking code and malformed idf"""

    # prohibited characters

    # prohibited keywords

    # check file length reasonable
    max_lines = 33000
    num_lines = 0

    for chunk in f.chunks():
        num_lines += chunk.read().count("\n")
    if num_lines > max_lines:
        log("File length is larger than max allowed %s lines" %max_lines)
        return False # Too Baku
        #return "The idf has not passed a check of basic requirements for a valid simulation file"
    
    return True

# procedural bit
# set f

def find_links(f):
    """Find target/source links between e+ objects 

    Args:
        objs (idf.idfobjects()) 
    Returns
        list of dicts, 
        [ {"source": int, "target":int}, .. ]
    Raises:
        dunno yet

    """
    # start eppy
    iddfile = "/usr/local/EnergyPlus-8-0-0/Energy+.idd"

    IDF.setiddname(iddfile) # only do this once
    # geometry_filename = os.path.join(input_directory, "model.idf") #"//home/tom/repos/www-maddog/mde/tutorials/ods-studio/afn0/ep/Output
    idf = IDF(f)
    #get a idf.idfobjects
    # get all idfobjects
    try:
        listed_objects = [obj[1] for obj in idf.idfobjects.iteritems() if len(obj[1]) > 0]
        all_objects = [x for lst in listed_objects for x in lst]
        #all_objects = [key for key, value in idf1.idfobjects.items() if len(value) > 0]
    except:
        return "couldnt get all objects, Santosh - whats up?"
    
    """all_objects = idf.idfobjects
    non_empty = []
    for obj in allobjects.iteritems():
        if obj[1]:
            non_empty.append(obj[1][0])
    """
    #afn_surfaces = idf.idfobjects['AirflowNetwork:Multizone:Surface'.upper()]

    list_of_names = []
    for obj in all_objects:
        try: 
            n = getattr(obj, 'Name')
            list_of_names.append(n)
        except:
            pass
    list_of_names

    # make list of all object names, source id

    # loop over objects, look for other names in that object
    links = []
    for name in list_of_names:
        for obj in all_objects:
            if name in obj.obj:
                #links.append("name %s found in %s" %(name, obj) )
                #print(obj.Name)
                #print(name)
                try: 
                    if name != obj.Name:
                        #print(" link from name : %s to name %s "%(name, obj.Name))
                        links.append(["source :%s"%name, "target: %s"%obj.Name ])
                except:
                    try: 
                        if name != obj.Zone_Name:
                            #print(" \tlink from name : %s to Zone Name %s "%(name, obj.Zone_Name))
                            links.append(["source :%s"%name, "target: %s"%obj.Zone_Name ])
                    except:
                        #print("\t \t Variables are not supported couldnt get name from %s"%obj.obj)
                        pass

    # when other object name appears in an object's detail, make that a target 

    # create a new dict {source, target}, append to the list to be returned
    # needs to be fucken ids, not names. 
    #https://gist.github.com/mbostock/2706022

# now the energy plus objects are in the database


# from here, run django model queries to tell webpage what links exist btween objects 

""" next steps
make layout draggable and fixable
make hover show up something
get this script working (concept is proven now)
"""
