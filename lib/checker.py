import json
from lib.query import disk

def load_serverConfig():
    
    try:
        with open("hosts.ini",'r') as r:
            server = [line.strip() for line in r if line.strip()]
        
        return server
    
    except FileNotFoundError as fe:
        print("file Hosts.ini not found/permission required") 
    except Exception as e:
        print(e)
      
def run_diskCheck():
    
    servers = load_serverConfig()
    print(servers)

    all_result = []
    
    for ip in servers:
        result = disk(str(ip))
        if result:
            all_result.append(result)
        print(all_result)
            
            
    json_output = json.dumps(all_result,indent=4)
    
    return(json_output)

if __name__ == '__main__':
    
    run_diskCheck()