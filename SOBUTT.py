"""Michael Randall
    mrandall@ucsd.edu"""

import time
import yaml
from ocs import matched_client

 
#Define Sweep parameters here. Change them here to change the pre-set sweep functions
COARSE_SWEEP_PARAMETERS = [{"frequency_start":10,
                           "frequency_end":200,
                           "frequency_step":5,
                           "time_step":30*60}]

FINE_SWEEP_PARAMETERS = [{"frequency_start":1,
                         "frequency_end":200,
                         "frequency_step":1,
                         "time_step":5}]


class Menu:
    
    def __init__(self, menu_header, menu_choices, menu_prompt):
        self.menu_header = menu_header
        self.menu_choices = menu_choices
        self.menu_prompt = menu_prompt
        
    
    def show_menu(self):
        if self.menu_header is not None:
            print(self.menu_header)
            print("~~~~~~~~~~~~~~~~~~~~~~~")
            
        for c, value in enumerate(self.menu_choices, 1):
            print(str(c) + ".", value)
        
        print("0. Exit")
        print("")
        time.sleep(.1)
        menu_response = input(self.menu_prompt)
        print("")
        return menu_response


#A main menu function that is called when the script is run from command line or compiler.
#Do not call function directly from command-line.
#This is only to create a UI for easy use of script
def main_menu(buttkicker, COARSE_SWEEP_PARAMETERS, FINE_SWEEP_PARAMETERS):
    buttkicker_on = False
    smurf_status = False
    custom_sweep_list = []
    main_menu_success = False
    while not main_menu_success:
        main_menu_header = "SOBUTT Main Menu"
        
        main_menu_choices = []
        
        main_menu_choices.append("Manual Control")
        main_menu_choices.append("Coarse sweep.")
        main_menu_choices.append("Fine sweep.")
        main_menu_choices.append("Custom sweep.")
        
        if run_smurf = False:
            main_menu_choices.append("Run Sweep with SMuRF (SMuRF is currently OFF).")
        else:
            main_menu_choices.append("Run sweep without SMuRF (SMuRF is currently ON).")
            
        main_menu_prompt = ("Select an operation: ")
        
        main_menu = Menu(main_menu_header, main_menu_choices, main_menu_prompt)
        main_menu_response = main_menu.show_menu()
        
        if main_menu_response == "1":
            manual_control_menu(buttkicker)
            
        #Coarse sweep
        elif main_menu_response == "2":
            print("Beginning coarse sweep...\n")
            frequency_sweep(buttkicker, COARSE_SWEEP_PARAMETERS, run_smurf)
            print("Coarse sweep finished!\n")
            
        #Fine sweep
        elif main_menu_response == "3":
            print("Beginning fine sweep...\n")
            frequency_sweep(buttkicker, FINE_SWEEP_PARAMETERS, run_smurf)
            print("Fine sweep finished!")
        
        elif main_menu_response == "4":
            custom_sweep_menu(buttkicker, custom_sweep_list, run_smurf)
                  
        #Exit
        elif main_menu_response == "0":
            print("Thanks for using SOBUTT!")
            main_menu_success = True


#Menu for manually controlling the buttkicker when script is called through command line or compiler
#Do not call function directly.
def manual_control_menu(buttkicker):
    manual_control_menu_success = False
    while not manual_control_menu_success:
        manual_control_menu_header = "Manual Control Menu"
        
        manual_control_menu_choices = []
        manual_control_menu_choices.append("Turn on ButtKicker")
        manual_control_menu_choices.append("Turn off ButtKicker")
        manual_control_menu_choices.append("Set ButtKicker Frequency")
        manual_control_menu_choices.append("Set ButtKicker Amplitude")
        
        manual_control_menu_prompt = "Select an operation:"
        
        manual_control_menu = Menu(manual_control_menu_header,
                                   manual_control_menu_choices,
                                   manual_control_menu_prompt)
    
        manual_control_menu_response = manual_control_menu.show_menu()
        
    	#Turn on
        if manual_control_menu_response == "1":
            turn_on_buttkicker(buttkicker)
            print("Buttkicker turned on.\n")
        
        #Set off
        elif manual_control_menu_response == "2":
            turn_off_buttkicker(buttkicker)
            print("Buttkicker turned off.\n")
        
        #Set static frequency   
        elif manual_control_menu_response == "3":
            set_buttkicker_frequency(buttkicker)
        
        #Set peak to peak amplitude
        elif manual_control_menu_response == "4":
            set_buttkicker_amplitude(buttkicker)
            
        elif manual_control_menu_response == "0":
            manual_control_menu_success = True

            
#Takes a buttkicker OCS session
#Gets a frequency from the user
#Sets buttkicker to that frequency
#Can be called directly for manual control
def set_buttkicker_frequency(buttkicker):
    frequency_choice = input("Enter a frequency (-1 to cancel): ")
    print("")
    if frequency_choice == "-1":
        return 0
    
    buttkicker.set_frequency.start(frequency=int(frequency_choice))
    print("Buttkicker frequency set to {}Hz.\n".format(frequency_choice))
    return 1


def set_buttkicker_amplitude(buttkicker):
    amplitude_choice = input("Enter a peak to peak amplitude (-1 to cancel): ")
    print("")
    
    if amplitude_choice == "-1":
        return 0
    
    buttkicker.set_amplitude.start(amplitude=int(amplitude_choice))
    print("Buttkicker peak to peak amplitude set to {}V.\n".format(amplitude_choice))
    return 1

                             
def turn_off_buttkicker(buttkicker):
    buttkicker.set_output.start(state=False)
    return 1


def turn_on_buttkicker(buttkicker):
    buttkicker.set_output.start(state=True)
    return 1


#frequency_sweep takes a list of dictionaries of sweep parameters
#Each dict has a freq start, freq end, freq step, and time step
#frequency_sweep loops through all sweep dicts and loops through their range
#Can be called directly, see the sweep_parameter_lists defined above for the list format
def frequency_sweep(buttkicker, sweep_list, run_smurf):
    
    #Initialize pysmurf 
    abandon_smurf = False
    if run_smurf:
        try:
            pysmurf = matched_client.MatchedClient('pysmurf-controller-s2', args=[])
            print("Initialize pysmurf client")
            smurf_start_script_path = '/sodetlib/scratch/max/stream_data_on.py'
            smurf_stop_script_path = '/sodetlib/scratch/max/stream_data_off.py'
            args = ['--config-file', '/data/pysmurf_cfg/experiment_ucsd_sat1_smurfsrv16_lbOnlyBay0.cfg',
                    '--epics-root','smurf_server_s2',
                ]

            print("Running {}...".format(smurf_start_script_path))
            pysmurf.run.start(script=smurf_start_script_path , args=args)
            pysmurf.run.wait()
            print("PySMuRF script has started.")
            time.sleep(1)
            
        except:
            print("There was an issue running SMuRF... abandoning SMuRF streaming.")
            abandon_smurf = True
            
    print("Turning on ButtKicker...\n")
    turn_on_buttkicker(buttkicker)
    
    for subsweep_parameters in sweep_list:
        frequency_start = int(subsweep_parameters["frequency_start"])
        frequency_end = int(subsweep_parameters["frequency_end"])
        frequency_step = int(subsweep_parameters["frequency_step"])
        time_step = int(subsweep_parameters["time_step"])
        
        current_frequency = frequency_start
        current_frequency_is_valid = True
        while current_frequency_is_valid:
            print("Setting ButtKicker frequency to {}Hz...".format(current_frequency))
            buttkicker.set_frequency.start(frequency=current_frequency)
            time.sleep(.5)
            
            time.sleep(time_step)
            if frequency_start <= frequency_end:
                current_frequency += frequency_step
                if current_frequency > frequency_end:
                    current_frequency_is_valid = False
            else:
                current_frequency -= frequency_step
                if current_frequency < frequency_end:
                    current_frequency_is_valid = False

    print("Turning off ButtKicker...\n")
    turn_off_buttkicker(buttkicker)
    time.sleep(.5)
    
    if run_smurf and not abandon_smurf:
        print("Running {}...".format(smurf_stop_script_path))
        pysmurf.run.start(script=smurf_stop_script_path , args=args)
        pysmurf.run.wait()
        print("PySMuRF script has finished.\n")

    return 1


#A menu function called from main menu
#Guides the user through creating a custom sweep
#Do not call function directly,
def custom_sweep_menu(buttkicker, custom_sweep_list):
    custom_sweep_menu_success = False
    while not custom_sweep_menu_success:
        #Print dictionary
        print_custom_sweep_list(custom_sweep_list)

        #Create menu
        custom_sweep_menu_header = "Custom Sweep Menu"
        custom_sweep_menu_choices = []
        custom_sweep_menu_choices.append("Add new range to sweep")
        custom_sweep_menu_choices.append("Remove range from sweep")
        custom_sweep_menu_choices.append("Edit range in sweep")
        custom_sweep_menu_choices.append("Run custom sweep")

        custom_sweep_menu_prompt = "Select an operation: "

        custom_sweep_menu = Menu(custom_sweep_menu_header,
                                custom_sweep_menu_choices,
                                custom_sweep_menu_prompt)

        #Get menu response
        custom_sweep_menu_response = custom_sweep_menu.show_menu()

        #Functions:
        ##Add 
        if custom_sweep_menu_response == "1":
            add_range_to_custom_sweep_list(custom_sweep_list)

        ##Remove
        elif custom_sweep_menu_response == "2":
            remove_range_from_custom_sweep_list(custom_sweep_list)

        ##Edit
        elif custom_sweep_menu_response == "3":
            edit_range_in_custom_sweep_list(custom_sweep_list)

        ##Save -- V2 

        ##Run
        elif custom_sweep_menu_response == "4":
            frequency_sweep(buttkicker, custom_sweep_list)
        
        elif custom_sweep_menu_response == "0":
            custom_sweep_menu_success = True
            

#Used in custom_sweep_menu to display the current custom sweep
#Do not call function directly
def print_custom_sweep_list(custom_sweep_list):
    print("Custom Sweep Parameters")
    print("~~~~~~~~~~~~~~~~~~~~~~")
    if len(custom_sweep_list) == 0:
        print("No sweep parameters defined")
    else:
        for i, parameters in enumerate(custom_sweep_list, 1):
            frequency_start = parameters["frequency_start"]
            frequency_end = parameters["frequency_end"]
            frequency_step = parameters["frequency_step"]
            time_step = parameters["time_step"]
            print("{}. [Range: {}-{}, Freq. Step: {}, Time step: {}]".format(i, frequency_start,
                                                                            frequency_end,
                                                                            frequency_step,
                                                                            time_step))
    print("")


#Just checks whether a user response is "CANCEL".
#Yes this is a dumb looking function
#Its purpose is to make the following custom-sweep functions more clear
def check_for_cancel(response):
    if response == "-1":
        return True
    return False


#Used to create a range for a custom sweep.
#Gets user inputs for frequency start, end, step, and time step
#Then compiles it into a dict which is appended to custom sweep.
#Do not call function directly.
def add_range_to_custom_sweep_list(custom_sweep_list):
    frequency_start = input("Frequency start? (-1 to cancel):")
    if check_for_cancel(frequency_start):
            return -1
        
    frequency_end = input("Frequency end? (-1 to cancel):")
    if check_for_cancel(frequency_end):
            return -1
        
    frequency_step = input("Frequency step? (-1 to cancel):")
    if check_for_cancel(frequency_step):
            return -1
        
    time_step = input("Time step? (-1 to cancel):")
    if check_for_cancel(time_step):
            return -1
        
    
    custom_sweep_list.append({"frequency_start": frequency_start,
                              "frequency_end": frequency_end,
                              "frequency_step": frequency_step,
                              "time_step":time_step})
    print("")
    return 1


#Used to delete a range that was created by the user when creating a custom sweep.
#Do not directly call function.
def remove_range_from_custom_sweep_list(custom_sweep_list):
    range_to_remove = input("Remove which range? (-1 to cancel):")
    if check_for_cancel(range_to_remove):
            return -1
    
    try:
        range_to_remove = int(range_to_remove)
        
        if 0 < range_to_remove <= len(custom_sweep_list):
            print("Removed: {}".format(custom_sweep_list.pop(range_to_remove - 1)))
            
        else:
            print("Response must be in list range.")
            
    except:
        print("Response must be an integer.")
    
    print("")
            

#Used to edit a range that was created by the user when creating a custom sweep.
#Do not directly call function.
def edit_range_in_custom_sweep_list(custom_sweep_list):
    range_to_edit = input("Edit which range? (-1 to cancel):")
    if check_for_cancel(range_to_edit):
            return -1
    
    try:
        range_to_edit = int(range_to_edit)
        
        if 0 < range_to_edit <= len(custom_sweep_list):
            
            frequency_start = input("Frequency start? (-1 to cancel):")
            if check_for_cancel(frequency_start):
                    return -1

            frequency_end = input("Frequency end? (-1 to cancel):")
            if check_for_cancel(frequency_end):
                    return -1

            frequency_step = input("Frequency step? (-1 to cancel):")
            if check_for_cancel(frequency_step):
                    return -1

            time_step = input("Time step [in seconds]? (-1 to cancel):")
            if check_for_cancel(time_step):
                    return -1
            
            custom_sweep_list[range_to_edit - 1] = {"frequency_start": frequency_start,
                                                    "frequency_end": frequency_end,
                                                    "frequency_step": frequency_step,
                                                    "time_step":time_step}
        else:
            print("Response must be in list range.")
            
    except:
        print("Response must be an integer.")
    
    print("")
    

#Initializes a buttkicker session using OCS and calls the main menu function.
if __name__ == "__main__":
    print("Welcome to SOBUTT!\n")
    buttkicker = matched_client.MatchedClient('tektronix', args=[])
    buttkicker.init.start()
    
    main_menu(buttkicker, COARSE_SWEEP_PARAMETERS, FINE_SWEEP_PARAMETERS)
