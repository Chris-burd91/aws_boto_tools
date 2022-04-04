import boto3
from simple_term_menu import TerminalMenu
from pprint import pprint

from botocore.exceptions import ClientError
ec2 = boto3.client('ec2')
# try:
#     response = ec2.describe_security_groups(GroupIds=[])
#     pprint(response)
# except ClientError as e:
#     print(e)
def view_sg():
    menu = True
    while menu:
        ip_address = input("Please enter IP Address: ")
        response = ec2.describe_instances(
    Filters=[
        {
            'Name': 'ip-address',
            'Values': [
                ip_address,
            ]
        },
    ],
  
)
        instance_name = response['Reservations'][0]['Instances'][0]['Tags'][0]['Value']
        list_groups = response['Reservations'][0]['Instances'][0]['SecurityGroups']
        print(f"\nSecurity Groups in {ip_address} Name --> {instance_name}\n")
        for item in list_groups:
            print(str(item).replace("{","").replace("}",""))
        loop = True
        while loop:
            print("\n")
            try:
                confirm = ["Yes", "No"]
                terminal_menu = TerminalMenu(confirm,
                title = "Would you like to continue and search another IP for their Security Groups?: ",
                menu_cursor_style= ("fg_green", "bold"))
                menu_entry_index = terminal_menu.show()
                confirm_result = str(confirm[menu_entry_index])
                loop = confirm_result
                if confirm_result == "No":
                    exit()
                if confirm_result == "Yes":
                    loop = False
                    break
            except TypeError:
                print("Exiting...")
                exit()

view_sg()