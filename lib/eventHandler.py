import requests
from dotenv import load_dotenv
from logs import event_log
import os, json

load_dotenv()
PROMETHEUS_API = os.getenv("PROMETHEUS_API")


def prometheus_query(query):
    url = f"{PROMETHEUS_API}/api/v1/query"
    event_log.info(f"Fetching Prometheus API data")
    try:
        response = requests.get(url, params={'query': query})
        response.raise_for_status() # Check for HTTP errors
        return response.json()['data']['result']
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []
    

def queryDiskInGB(serverIP:str):
    
    metric = {}
            
    query = (
        f'(windows_logical_disk_size_bytes{{job="{serverIP}", volume!~"Harddisk.*"}} '
        f'- windows_logical_disk_free_bytes{{job="{serverIP}", volume!~"Harddisk.*"}}) '
        f'/ 1073741824'
    )

    queryResult = prometheus_query(query) 
    for node in queryResult:
        instance = node['metric'].get('job', 'Unknown')
        disk = node['metric'].get('volume')
        usage = float(node['value'][1])
        
        metric['instance'] = instance
        if disk == "D:":
            metric['Disk D'] = f'{usage:.2f} GB'
        else:
            metric['Dick C'] = f'{usage:.2f} GB'
    
    return print(metric)


def queryDiskInPercent(serverIP:str):
    
    metric = {}

    query = (
        f'(windows_logical_disk_size_bytes{{job="{serverIP}", volume!~"Harddisk.*"}} '
        f'- windows_logical_disk_free_bytes{{job="{serverIP}", volume!~"Harddisk.*"}}) '
        f'/ windows_logical_disk_size_bytes{{job="{serverIP}", volume!~"Harddisk.*"}} * 100'
    )

    result = prometheus_query(query)
    for node in result:
        instance = node['metric'].get('job', 'Unknown')
        disk = node['metric'].get('volume')
        usage = float(node['value'][1])
        
        metric['instance'] = instance
        if disk == "D:":
            metric['Disk D'] = f'{usage:.2f} %'
        else:
            metric['Dick C'] = f'{usage:.2f} %'
    
    return print(metric)



# For Test Purposes
# if __name__ == "__main__":
#     queryDiskInPercent("192.168.22.9")
#     queryDiskInGB("192.168.22.9")