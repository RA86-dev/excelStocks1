import os
import platform
print(f"Running on Compiler {platform.python_compiler()}")
print(f"Python Version {platform.python_version()}")
os_name = os.uname().sysname
if os_name.lower() == "linux":
    print('Running installation...')
    os.system('sudo apt install python3-pip')
    os.system('sudo apt install python3-flask')
    os.system('sudo apt install neofetch')
    os.system('sudo apt install lm-sensors')
    
    os.system('pip install -r requirements.txt')
    os.system('clear')
    os.system('neofetch')
    os.system('sensors')
    print('Program has finished installing.')
elif os_name.lower() == "darwin":
    print('Installing MacInstall')
    os.system('pip install -r macinstall.txt')
else:
    print('Defaulting to main install for Win10/Win11,etc.')
    os.system('pip install -r requirements.txt')
yml_file_lines = '''
# default main used.
debug_log_filename: debugLog
logsLocation: file_location_create
percentage_filter_default: 25
repeat: true
repeatfileLocation: default_store_location
usefilepath: true
# stock method
max_price_threshold: 200

'''
with open('settings.yml','w') as _:
    _.write(yml_file_lines)
    print('Sucessfully preset settings!')
