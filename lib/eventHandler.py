import requests,os
from logs import event_log
from dotenv import load_dotenv

load_dotenv()
PROMETHEUS_API = os.getenv("PROMETHEUS_API")


def prometheus_query(query:str):
    url = f"{PROMETHEUS_API}/api/v1/query"
    event_log.info(f"Fetching Prometheus API data")
    try:
        response = requests.get(url, params={'query': query})
        response.raise_for_status() # Check for HTTP errors
        return response.json()['data']['result']
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []

def disk(serverIP:str):
    
    metric = {}
            
    diskUsageQuery = (
        f'(windows_logical_disk_size_bytes{{job="{serverIP}", volume!~"Harddisk.*"}} '
        f'- windows_logical_disk_free_bytes{{job="{serverIP}", volume!~"Harddisk.*"}}) / 1073741824'
    )
    
    diskTotalQuery = (
        f'windows_logical_disk_size_bytes{{job="{serverIP}", volume!~"Harddisk.*"}} / 1073741824'
    )
    
    diskPercentquery = (
        f'(windows_logical_disk_size_bytes{{job="{serverIP}", volume!~"Harddisk.*"}} '
        f'- windows_logical_disk_free_bytes{{job="{serverIP}", volume!~"Harddisk.*"}}) '
        f'/ windows_logical_disk_size_bytes{{job="{serverIP}", volume!~"Harddisk.*"}} * 100'
    )

    diskTotal = prometheus_query(diskTotalQuery)
    diskUsage = prometheus_query(diskUsageQuery) 
    diskPercent = prometheus_query(diskPercentquery)
    
    for node in diskTotal:
        instance = node['metric'].get('job', 'Unknown')
        metric['instance'] = instance    
        
        for node2 in diskUsage:
            diskUsagePartition = node2['metric'].get('volume')
            usage = float(node2['value'][1])
            if diskUsagePartition == 'D:':
                metric['Disk D usage'] = f'{usage:.2f} GB'
            else:
                metric['Disk C usage'] = f'{usage:.2f} GB' 
                
        for node3 in diskPercent:
            diskUsagePartition = node3['metric'].get('volume')
            Percent = float(node3['value'][1])
            if diskUsagePartition == 'D:':
                metric['Disk D usage percent'] = f'{Percent:.2f} %'
            else:
                metric['Disk C usage percent'] = f'{Percent:.2f} %' 
        
        disk = node['metric'].get('volume')
        size = float(node['value'][1])
        if disk == "D:":
            metric['Disk D size'] = f'{size:.2f} GB'
        else:
            metric['Dick C size'] = f'{size:.2f} GB'
        
    return print(metric)
