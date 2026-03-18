import requests,os
from lib.logs import event_log
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
    
    metric['node'] = serverIP
    
    def process_node(nodes, suffix, unit):
        for node in nodes:
            vol = node['metric'].get('volume','unknown').replace(':','')
            val = float(node['value'][1])
            
            metric[f'Disk {vol} {suffix}'] = f'{val:.2f} {unit}'
            
    process_node(diskTotal, 'size', 'GB')
    process_node(diskUsage, 'usage', 'GB')
    process_node(diskPercent, 'usage percent', '%')
    
    return metric