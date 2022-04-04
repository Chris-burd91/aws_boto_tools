import boto3
from simple_term_menu import TerminalMenu
from pprint import pprint

client_ecs = boto3.client('ecs')

clusters = client_ecs.list_clusters(

)

cluster_arn_list = list(clusters['clusterArns'])
cluster_list = [i.split('/', 1)[1] for i in cluster_arn_list]
#print(cluster_list)

def cluster_pick():
    try:
        cluster_menu = TerminalMenu(cluster_list,
        title = "Select Cluster: ",
        menu_cursor_style = ("fg_green", "bold"))
        menu_entry_index = cluster_menu.show()
        result = str(cluster_list[menu_entry_index])
        return result
    except TypeError:
        return

cluster_pick_result = cluster_pick()



services = client_ecs.list_services(
    cluster = cluster_pick_result,
    maxResults=100
)

services_arn_list = list(services['serviceArns'])
services_list = [i.split('/')[-1] for i in services_arn_list]
services_list.sort()



def service_pick():
    try:
        service_menu = TerminalMenu(services_list,
        title = "Select Service: ",
        menu_cursor_style = ("fg_green", "bold"))
        menu_entry_index = service_menu.show()
        result = str(services_list[menu_entry_index])
        return result
    except TypeError:
        return

service_pick_result = service_pick()

# describe_service = client.describe_services(
#     cluster = cluster_pick_result,
#     services = [service_pick_result]
# )
# pprint(describe_service)#['ResponseMetadata'])


list_tasks = client_ecs.list_tasks(
    cluster = cluster_pick_result,
    serviceName = service_pick_result
)

#print(list_tasks['taskArns'])

task_list = [i.split('/')[-1] for i in list_tasks['taskArns']]

task_describe = client_ecs.describe_tasks(
    cluster = cluster_pick_result,
    tasks=task_list
)

container_list = []
for item in task_describe['tasks']:
    container_instance = item['containerInstanceArn']
    container_instance_id = container_instance.split('/')[-1]
    container_list.append(container_instance_id)
    #print(container_list)


container_instance_describe = client_ecs.describe_container_instances(
    cluster=cluster_pick_result,
    containerInstances = container_list
)

ec2_instance_ids_list = []
for i in range(len(container_instance_describe['containerInstances'])):
    ec2_instance_ids_list.append(container_instance_describe['containerInstances'][i]['ec2InstanceId'])
   
#print(ec2_instance_ids_list)

client_ec2 = boto3.client('ec2')

ec2_describe = client_ec2.describe_instances(
    InstanceIds=ec2_instance_ids_list
)

for item in ec2_describe['Reservations']:
    ip_level = item['Instances'][0]
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
   

#pprint(ec2_describe)