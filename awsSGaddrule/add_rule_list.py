import boto3
from simple_term_menu import TerminalMenu
from pprint import pprint
import sys

from botocore.exceptions import ClientError
ec2 = boto3.client('ec2')

# sg_list[
# Here is where you would put a whole list of Security group ID's to be used to add the rule too
# ]
#


def add_sg_rule():
    for item in sg_list:
        response = ec2.authorize_security_group_ingress(
            GroupId=item,
            IpPermissions=[
                {
                    'FromPort': 22,
                    'ToPort': 22,
                    'IpProtocol': 'tcp',
                    'IpRanges': [
                        {
                            'CidrIp': '<Replace with IP address or CIDR block>',
                            'Description': 'Allow SSH access from IP range'
                        }
                    ],
                }
            ],
            DryRun=False
        )

        pprint(response)


sys.stdout = open("rules_added.txt", "w")
add_sg_rule()
sys.stdout.close()
