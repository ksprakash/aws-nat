import yaml
import os
import boto3
import csv
from datetime import datetime
profiles= []
with open(f"./config.yaml") as ymlfile:
    data = yaml.safe_load(ymlfile)

for profile in profiles:
        session = boto3.Session(region_name=data['credentials']['region'],profile_name=profile)
        client = session.client('ec2') 
        def get_nats():
            response = client.describe_nat_gateways(MaxResults=100)
            data = response.get("NatGateways")
            while 'NextToken' in response and response.get('NextToken'):
                    token = response.get('NextToken')
                    response = client.describe_nat_gateways(MaxResults=100,NextToken=token)
                    data += response.get("NatGateways")
            return data

        natss =get_nats()

        time_now = datetime.now()
        with open(f"report.csv",mode='w') as csvfile:
            fieldnames = ["profile","PublicIp","VpcId","SubnetId",""]
            csv_writer = csv.DictWriter(csvfile,fieldnames=fieldnames) 
            csv_writer.writeheader()
            for nat in natss:
                public_ip = nat["NatGatewayAddresses"]["PublicIp"]
                vpc_id    = nat["VpcId"]
                subnet_id = nat["SubnetId"]
                
                csv_writer.writerow({
                            "Account" : profile,
                            "PublicIp":public_ip,
                            "VpcId":vpc_id,
                            "SubnetId": subnet_id})
                
