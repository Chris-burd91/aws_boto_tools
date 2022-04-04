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

describe_service = client_ecs.describe_services(
    cluster = cluster_pick_result,
    services=[service_pick_result]
)

td_arn = str(describe_service['services'][0]['deployments'][0]['taskDefinition'])
task_definition = td_arn.split('/')[-1]

task_definition_describe = client_ecs.describe_task_definition(
    taskDefinition=task_definition
)

td_data = task_definition_describe['taskDefinition']['containerDefinitions'][0]
print(f"TASK DEFINITION VERSION: {task_definition}\n")
for item in td_data.keys():
    if item == 'environment':
        print(f"\nENVIRONMENT VARIABLES HERE:\n")
        for env_var in td_data[item]:
            
            print(f"[{env_var['name']} : {env_var['value']}]")
    else:
        print(f"\n{item.upper()} : {td_data[item]}")
