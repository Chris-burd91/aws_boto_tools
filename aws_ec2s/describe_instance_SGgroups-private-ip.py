import boto3
from simple_term_menu import TerminalMenu
from pprint import pprint

from botocore.exceptions import ClientError

ec2 = boto3.client('ec2')

def view_sg():
    response = ec2.describe_instances(

)
    all_instances=response['Reservations']
    count = 0
    for item in all_instances:
        count += 1
        private_ip_address = item['Instances'][0]['NetworkInterfaces'][0]['PrivateIpAddress']
        # pprint(private_ip_address)
        response_private = ec2.describe_instances(
    Filters=[
        {
            'Name': 'private-ip-address',
            'Values': [
                private_ip_address,
            ]
        },
    ],
  
)      
        try:
            list_groups = response_private['Reservations'][0]['Instances'][0]['SecurityGroups']
        except IndexError:
            list_groups = f"List index called out of range,{private_ip_address} needs to be checked manually"
        try:
            try:
                instance_name = response_private['Reservations'][0]['Instances'][0]['Tags'][0]['Value']
            except IndexError:
                continue
        except KeyError:
            instance_name = "No tag so no name given!!!"
        print(private_ip_address)
        print(f"\nSecurity Groups in {private_ip_address} Name --> {instance_name}\n")
        for item in list_groups:            
            print(str(item).replace("{","").replace("}",""))
        print(count)
    
        
        

view_sg()