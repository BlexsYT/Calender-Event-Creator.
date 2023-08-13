import psutil

def get_active_applications():
    active_apps = []
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        if proc.info['name'] in ('Code.exe', 'idea64.exe', 'RobloxStudioBeta.exe'):
            active_apps.append(proc.info['name'])
    return active_apps

active_apps = get_active_applications()
print("Active applications:", active_apps)
