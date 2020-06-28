"""Michael Randall
    mrandall@ucsd.edu"""

import time
import yaml
from ocs import matched_client

class Menu:
    
    def __init__(self, menu_header, menu_choices, menu_prompt):
        self.menu_header = menu_header
        self.menu_choices = menu_choices
        self.menu_prompt = menu_prompt
        
    
    def show_menu(self):
        print(self.menu_header)
        print("~~~~~~~~~~~~~~~~~~~~~~~")
        for c, value in enumerate(self.menu_choices, 1):
            print(str(c) + ".", value)
        
        print("0. Exit")
        print("")
        menu_response = input(self.menu_prompt)
        print("")
        return menu_response

coarse_sweep_parameters = {"frequency_start":10,
                           "frequency_end":200,
                           "frequency_step":5,
                           "time_step":30*60}

fine_sweep_parameters = {"frequency_start":1,
                         "frequency_end":20,
                         "frequency_step":1,
                         "time_step":60}
   
    
def main_menu(buttkicker, coarse_sweep_parameters, fine_sweep_parameters):
    buttkicker_on = False
    main_menu_success = False
    while not main_menu_success:
        main_menu_header = "SOBUTT Main Menu"
        
        main_menu_choices = []
        
        main_menu_choices.append("Turn ButtKicker on")
        main_menu_choices.append("Turn ButtKicker off.")
        main_menu_choices.append("Set ButtKicker to static frequency.")
        main_menu_choices.append("Set ButtKicker amplitude.")
        main_menu_choices.append("Coarse sweep.")
        main_menu_choices.append("Fine sweep.")
        main_menu_choices.append("Custom sweep.")
        
        main_menu_prompt = ("Select an operation: ")
        
        main_Menu = Menu(main_menu_header, main_menu_choices, main_menu_prompt)
        main_menu_response = main_Menu.show_menu()
        
	#Turn on
        if main_menu_response == "1":
            turn_on_buttkicker(buttkicker)
            print("Buttkicker turned on.\n")
        
	#Turn off
        elif main_menu_response == "2":
            turn_off_buttkicker(buttkicker)
            print("Buttkicker turned off.\n")
        
	#Set static frequency   
        elif main_menu_response == "3":
            set_buttkicker_frequency(buttkicker)
        
	#Set peak to peak amplitude
        elif main_menu_response == "4":
            set_buttkicker_amplitude(buttkicker)
            
        #Coarse sweep
        elif main_menu_response == "5":
            print("Beginning coarse sweep...\n")
            frequency_sweep(buttkicker, coarse_sweep_parameters)
            print("Coarse sweep finished!\n")
            
        #Fine sweep
        elif main_menu_response == "6":
            print("Beginning fine sweep...\n")
            frequency_sweep(buttkicker, fine_sweep_parameters)
            print("Fine sweep finished!")
        
        elif main_menu_response == "7":
            print("Beginning custom sweep...\n")
            custom_sweep(buttkicker)
            print("Custom sweep finished!")
                  
        #Exit
        elif main_menu_response == "0":
            print("Thanks for using SOBUTT!")
            main_menu_success = True


def set_buttkicker_frequency(buttkicker):
    frequency_choice = input("Enter a frequency (-1 to cancel): ")
    print("")
    buttkicker.set_frequency.start(frequency=40)
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


def frequency_sweep(buttkicker, sweep_parameters):
    frequency_start = int(sweep_parameters["frequency_start"])
    frequency_end = int(sweep_parameters["frequency_end"])
    frequency_step = int(sweep_parameters["frequency_step"])
    time_step = int(sweep_parameters["time_step"])

    #Initialize pysmurf                                                                             
    pysmurf = matched_client.MatchedClient('pysmurf-controller-s2', args=[])
    print("Initialize pysmurf client")
    smurf_start_script_path = '/sodetlib/scratch/max/stream_data_on.py'
    smurf_stop_script_path = '/sodetlib/scratch/max/stream_data_off.py'
    args = ['--config-file', '/data/pysmurf_cfg/experiment_ucsd_sat1_smurfsrv16_lbOnlyBay0.cfg',
            '--epics-root','smurf_server_s2',
        ]
    
    print("Turning on ButtKicker...\n")
    turn_on_buttkicker(buttkicker)

    print("Running {}...".format(smurf_start_script_path))
    pysmurf.run.start(script=smurf_start_script_path , args=args)
    pysmurf.run.wait()
    print("Pysmurf script has finished.\n")
    
    current_frequency = frequency_start
    while current_frequency <= frequency_end:
        print("Setting ButtKicker frequency to {}Hz...".format(current_frequency))
        buttkicker.set_frequency.start(frequency=current_frequency)
        time.sleep(.5)
        
        time.sleep(30)

        current_frequency += frequency_step
    
    print("Turning off ButtKicker...\n")
    turn_off_buttkicker(buttkicker)
    time.sleep(.5)

    print("Running {}...".format(smurf_stop_script_path))
    pysmurf.run.start(script=smurf_stop_script_path , args=args)
    pysmurf.run.wait()
    print("Pysmurf script has finished.\n")
    
    return 1


def custom_sweep(buttkicker):
    with open("/home/manny/users/Mrandall/SOBUTT/custom_sweep_range.yaml") as sweep_yaml:
        custom_sweep_dict = yaml.load(sweep_yaml, Loader=yaml.FullLoader)
    
    sweep_finished = False
    sweep_index = 1
    while not sweep_finished:
        try: 
            custom_sweep_parameters = custom_sweep_dict[sweep_index]

            start_frequency = custom_sweep_parameters["Start frequency"]
            stop_frequency = custom_sweep_parameters["Stop frequency"]
            time_step = custom_sweep_parameters["Time step"]
            
            sweep_parameters = {"frequency_start": start_frequency,
                                "frequency_end": stop_frequency,
                                "frequency_step": 1,
                                "time_step": time_step}

            frequency_sweep(buttkicker, sweep_parameters)

            sweep_index +=1
            
        except:
            sweep_finished = True
            
            
if __name__ == "__main__":
    print("Welcome to SOBUTT!\n")
    buttkicker = matched_client.MatchedClient('tektronix', args=[])
    #Initialize pysmurf

    buttkicker.init.start()
    main_menu(buttkicker, coarse_sweep_parameters, fine_sweep_parameters)
