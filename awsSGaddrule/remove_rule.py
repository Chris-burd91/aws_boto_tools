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


def add_sg_rule():
    menu = True
    while menu:
        response = ec2.revoke_security_group_ingress(
            GroupId=input("Please enter Security group ID here: "),
            IpPermissions=[
                {
                    'FromPort': 22,
                    'ToPort': 22,
                    'IpProtocol': 'tcp',
                    'IpRanges': [
                        {
                            'CidrIp': 'IP Address/CIDR Range',
                            'Description': 'Allow SSH access IP Range'
                        }
                    ],
                }
            ],
            DryRun=False
        )
        pprint(response)
        loop = True
        while loop:
            try:
                confirm = ["Yes", "No"]
                terminal_menu = TerminalMenu(confirm,
                                             title="Remove another security group rule?: ",
                                             menu_cursor_style=("fg_green", "bold"))
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


add_sg_rule()
