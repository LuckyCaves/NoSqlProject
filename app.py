# def set_username():
#     role = input('What is your role?:\n\n1: Doctor\n2: Patient\n\nEnter tour choise:')
#     username = input('Username to use app: ')
#     log.info(f"Username set to {username}")
#     return username

# def check_patient_appointments():
#     patient_name = input("Enter the patient ID: ")
#     date_to_check = in

def print_menu():
    mm_options = {
        0: "Populate data",
        1: "Show accounts",
        2: "Show appoinments",
        3: "Check vital signs",
        4: "Check Actions",
        5: "My Alerts",
        6: "Exit",
    }
    for key in mm_options.keys():
        print(key, '--', mm_options[key])