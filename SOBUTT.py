"""Michael Randall
    mrandall@ucsd.edu"""

import time
#from ocs import matched_client

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

        menu_response = input(self.menu_prompt)
        print("")
        return menu_response

coarse_sweep_parameters = {"frequency_start":10,
                           "frequency_end":200,
                           "frequency_step":5,
                           "time_step":30*60}

fine_sweep_parameters = {"frequency_start":10,
                         "frequency_end":200,
                         "frequency_step":1,
                         "time_step":20}
   
    
def main_menu(buttkicker, coarse_sweep_parameters, fine_sweep_parameters):
    buttkicker_on = False
    
    main_menu_success = False
    while not main_menu_success:
        main_menu_header = "SOBUTT Main Menu"
        
        main_menu_choices = []
        
        if buttkicker_on:
            main_menu_choices.append("Turn ButtKicker off.")
        else:
            main_menu_choices.append("Set ButtKicker to static frequency.")
            
        main_menu_choices.append("Coarse sweep.")
        main_menu_choices.append("Fine sweep.")
        
        main_menu_prompt = ("Select an operation: ")
        
        main_Menu = Menu(main_menu_header, main_menu_choices, main_menu_prompt)
        main_menu_response = main_Menu.show_menu()
        
        if main_menu_response == "1":
            if buttkicker_on:
                turn_off_buttkicker(buttkicker)
                buttkicker_on = False
            else:
                set_buttkicker_frequency(buttkicker)
                buttkicker_on = True
        
        #Coarse sweep
        elif main_menu_response == "2":
            print("Beginning coarse sweep...\n")
            frequency_sweep(buttkicker, coarse_sweep_parameters)
            print("Coarse sweep finished!\n")
            
        #Fine sweep
        elif main_menu_response == "3":
            print("Beginning fine sweep...\n")
            frequency_sweep(buttkicker, fine_sweep_parameters)
            print("Fine sweep finished!")
        
        #Exit
        elif main_menu_response == "0":
            print("Thanks for using SOBUTT!")
            main_menu_success = True



def set_buttkicker_frequency(buttkicker):
    frequency_choice = input("Enter a frequency (0 to cancel): ")
    print("")
    
    if frequency_choice == 0:
        return 0
    
    #Set buttkicker frequency here!
    return 1


def turn_off_buttkicker(buttkicker):
    #Turn off buttkicker here!
    return 1


def turn_on_buttkicker(buttkicker):
    #Turn on buttkicker here!
    return 1


def frequency_sweep(buttkicker, sweep_parameters):
    frequency_start = sweep_parameters["frequency_start"]
    frequency_end = sweep_parameters["frequency_end"]
    frequency_step = sweep_parameters["frequency_step"]
    time_step = sweep_parameters["time_step"]
    
    current_frequency = frequency_start
    while current_frequency < frequency_end:
        print("Setting ButtKicker frequency to {}Hz...".format(current_frequency))
        #Set buttkicker frequency to current_frequency here!
        time.sleep(.1)
        
        print("Starting SMuRF stream...")
        #Start smurf stream here!
        time.sleep(.1)
        
        print("Turning on ButtKicker...")
        #turn on buttkicker here!
        time.sleep(.1)
        
        print("Sleeping for {} seconds...".format(time_step))
        time.sleep(.1)
        
        print("Measurement at {}Hz finished!".format(current_frequency))
        time.sleep(.1)
        
        print("Stopping SMuRF stream...")
        #Stop smurf stream here!
        time.sleep(.1)
        
        print("Turning off ButtKicker...\n")
        time.sleep(.1)
        current_frequency += frequency_step
    
    return 1


if __name__ == "__main__":
    print("Welcome to SOBUTT!\n")
    #Initiate buttkicker here!
    buttkicker = "Test"
    main_menu(buttkicker, coarse_sweep_parameters, fine_sweep_parameters)