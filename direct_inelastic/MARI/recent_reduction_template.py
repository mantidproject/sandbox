#pylint: disable=invalid-name
import os
#os.environ["PATH"] =\
#r"c:/Mantid/Code/builds/br_master/bin/Release;"+os.environ["PATH"]
sys.path.insert(0, "/opt/mantidnightly/bin")

""" Sample MARI reduction scrip used in testing ReductionWrapper """
from Direct.ReductionWrapper import *
try:
    import reduce_vars as web_var
except:
    web_var = None


class ReduceMARIFromFile(ReductionWrapper):
    @MainProperties
    def def_main_properties(self):
        """Define main properties used in reduction. These are the property
           a user usually wants to change
        """
        prop = {}
        # if energy is specified as a list (even with single value e.g. ei=[81])
        # The numbers are treated as a fraction of ei [from ,step, to ]. If energy is 
        # a number, energy binning assumed to be absolute (e_min, e_step,e_max)
        #
        prop['incident_energy'] = 12
        prop['energy_bins'] = [-11,0.05,11]
        #
        # the range of files to reduce. This range ignored when deployed from autoreduction,
        # unless you going to sum these files. 
        # The range of numbers or run number is used when you run reduction from PC.

        prop['sample_run'] = 11001
        prop['wb_run'] = 11060

        #
        prop['sum_runs'] = False # set to true to sum everything provided to sample_run
        #                        # list
        # Absolute units reduction properties. Set prop['monovan_run']=None to do relative units
        prop['monovan_run'] = 11015
        prop['sample_mass'] = 10
        prop['sample_rmm'] = 435.96
        return prop

    @AdvancedProperties
    def def_advanced_properties(self):
        """Set up advanced properties, describing reduction.
           These are the properties, usually provided by an instrument
           scientist

           separation between simple and advanced properties depends
           on scientist, experiment and user.   All are necessary for reduction 
           to work properly
        """
        prop = {}
        prop['map_file'] = "mari_res.map"
        prop['monovan_mapfile'] = "mari_res.map"
        #prop['hardmaskOnly']=maskfile # disable diag, use only hard mask
        prop['hard_mask_file'] = "mar11015.msk"
        prop['det_cal_file'] = 11060
        #
        #prop['wb_integr_range'] = [2,10]         
        #prop['data_file_ext']='.nxs' # if two input files with the same name and
                                    #different extension found, what to prefer.
        # there is currently bug in loadISISnexus, not loading monitors properly.
        #  When it fixed,  the value of this parameter will be irrelevant
        prop['load_monitors_with_workspace'] = True
        # change this to correct value and verify that motor_log_names refers correct and existing 
        # log name for crystal rotation to write correct psi value into nxspe files
        prop['motor_offset']=None     
        return prop
      #
    @iliad
    def reduce(self,input_file=None,output_directory=None):
        """Method executes reduction over single file

          Overload only if custom reduction is needed or 
          special features are requested
        """

        outWS = ReductionWrapper.reduce(self,input_file,output_directory)
        #SaveNexus(outWS,Filename = 'MARNewReduction.nxs')
        # Does the possibility to return PATH where to copy from web-services exist?
        return outWS

    def validate_result(self,build_validation=False):
        """Change this method to verify different results"""
        # build_validation -- if true, build and save new workspace rather then validating the old one
        rez,message = ReductionWrapper.build_or_validate_result(self,11001,"MARIReduction.nxs",build_validation,1.e-5)
        return rez,message

    def set_custom_output_filename(self):
        """ define custom name of output files if standard one is not satisfactory
          In addition to that, example of accessing reduction properties
          Changing them if necessary
        """
        def custom_name(prop_man):
            """Sample function which builds filename from
              incident energy and run number and adds some auxiliary information
              to it.
            """
            # Note -- properties have the same names as the list of advanced and
            # main properties
            ei = prop_man.incident_energy
            # sample run is more then just list of runs, so we use
            # the formalization below to access its methods
            run_num = PropertyManager.sample_run.run_number()
            name = "RUN{0}atEi{1:<4.1f}meV_One2One".format(run_num ,ei)
            return name

        # Uncomment this to use custom filename function
        # Note: the properties are stored in prop_man class accessed as
        # below.
        #return custom_name(self.reducer.prop_man)
        # use this method to use standard file name generating function
        return None


    def __init__(self,web_var=None):
        """ sets properties defaults for the instrument with Name"""
        ReductionWrapper.__init__(self,'MAR',web_var)
#-------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------------#
def main(input_file=None,output_directory=None):
    """ This method is used to run code from web service
        and should not be touched except changing the name of the
        particular ReductionWrapper class (e.g. ReduceMARI here)

        You can also change the output folder to save data to
        where web services will copy data

        This method will go when web service implements proper factory
    """
    # note web variables initialization
    rd = ReduceMARIFromFile(web_var)
    rd.reduce(input_file,output_directory)
    # change to the name of the folder to save data to
    return ''

if __name__ == "__main__":
#------------------------------------------------------------------------------------#
# SECTION USED TO RUN REDUCTION FROM MANTID SCRIPT WINDOW #
#------------------------------------------------------------------------------------#
##### Here one sets up folders where to find input data and where to save results ####
    # It can be done here or from Mantid GUI:
    #      File->Manage user directory ->Browse to directory
    # Folder where map and mask files are located:
    #map_mask_dir = 'c:/Users/wkc26243/Documents/work/Libisis/InstrumentFiles/maps'
    # folder where input data can be found
    #data_dir = 'd:/Data/Mantid_Testing/15_01_27/autoreduce_maps'
    #root=os.path.dirname(os.path.realpath(__file__))
    #data_dir = os.path.join(root,r'data')

    #config.appendDataSearchDir(root)
    #config.appendDataSearchDir(data_dir)
    #config['defaultsave.directory']=root
###### Initialize reduction class above and set up reduction properties.        ######
######  Note no web_var in constructor.(will be irrelevant if factory is implemented)
    rd = ReduceMARIFromFile()
    rd.def_advanced_properties()
    rd.def_main_properties()

#### uncomment rows below to generate web variables and save then to transfer to ###
    ## web services.
    run_dir = os.path.dirname(os.path.realpath(__file__))
    file = os.path.join(run_dir,'reduce_vars.py')
    rd.save_web_variables(file)

#### Set up time interval (sec) for reducer to check for input data file.  ####
    #  If this file is not present and this value is 0,reduction fails
    #  if this value >0 the reduction wait until file appears on the data
    #  search path checking after time specified below.
    rd.wait_for_file = 0  # waiting time interval

####get reduction parameters from properties above, override what you want locally ###
   # and run reduction.  Overriding would have form:
   # rd.reducer.property_name (from the dictionary above) = new value e.g.
   # rd.reducer.energy_bins = [-40,2,40]
   # or
   ## rd.reducer.sum_runs = False

###### Run reduction over all run numbers or files assigned to ######
     # sample_run variable

    # return output workspace only if you are going to do
    # something with it here.  Running range of runs will return the array
    # of workspace pointers.
    #red_ws = rd.run_reduction()
    # usual way to go is to reduce workspace and save it internally
    #rd.run_reduction()


#### Validate reduction result against known result, obtained earlier  ###
    rez,mess=rd.validate_result()
    if not rez:
       raise RuntimeError("validation failed with error: {0}".format(mess))
    else:
       print "ALL Fine"
