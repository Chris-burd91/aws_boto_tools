import boto3
from simple_term_menu import TerminalMenu
from pprint import pprint

client = boto3.client('ec2')

response = client.describe_instances(
)

count = 0
instance_list = []
for item in response['Reservations']:
    if item['Instances'][0]['State'].get('Name') == 'running':
        count += 1
        instance_id = item['Instances'][0]['InstanceId']
        names = item['Instances'][0].get('Tags')
        try:
            for name in names:       
                if name.get('Key') == 'Name':
                    instance_name = name.get('Value')
        except TypeError:
            instance_name = "No name assocaiated with this Instance"
        instance_list.append(f"{instance_name}:{instance_id}")
    
instance_list.sort()

def host_pick():
    try:
        host_menu = TerminalMenu(instance_list,
        title = "Select Host: ",
        menu_cursor_style = ("fg_green", "bold"))
        menu_entry_index = host_menu.show()
        result = str(instance_list[menu_entry_index])
        return result
    except TypeError:
        return

host_picked = host_pick()
name = host_picked.split(':')[0]
instance_id = host_picked.split(':')[1]
#print(instance_id)

# for item in response:
#     count += 1
#     print(item, f"\n")
    
# print(count)

ec2_describe = client.describe_instances(
    InstanceIds=[instance_id]
)

for item in ec2_describe['Reservations']:
    ip_level = item['Instances'][0]
    print(f"EC2 Name: {name}")
    print(f"EC2 ID: {ip_level['InstanceId']}") 
    try:
        print(f"Public Ipv4 Address: {ip_level['PublicIpAddress']}")
    except KeyError:
        print("No Public Ipv4 Address")

    print(f"Private Ipv4 Address {ip_level['PrivateIpAddress']}")
       
    try:  
        print(f"Ipv6 Address {ip_level['Ipv6Address']}\n")
    except KeyError:
        print(f"No Ipv6 Address \n")