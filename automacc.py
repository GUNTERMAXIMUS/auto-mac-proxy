import os, time
from tqdm import tqdm

def macchange(Iface):
    os.system(f'sudo ifconfig {Iface} down')
    os.system(f'sudo macchanger -r {Iface}')
    os.system(f'sudo ifconfig {Iface} up')

def loading_bar(r1=0, r2=100, s=1, t='\nLoading...\n'):
    print(t)
    for __ in tqdm(range(r1, r2)):
        time.sleep(s)

def display_logo():
    print('''
     █████╗ ██╗   ██╗████████╗ ██████╗ ███╗   ███╗ █████╗  ██████╗ ██████╗
    ██╔══██╗██║   ██║╚══██╔══╝██╔═══██╗████╗ ████║██╔══██╗██╔════╝██╔════╝
    ███████║██║   ██║   ██║   ██║   ██║██╔████╔██║███████║██║     ██║     
    ██╔══██║██║   ██║   ██║   ██║   ██║██║╚██╔╝██║██╔══██║██║     ██║     
    ██║  ██║╚██████╔╝   ██║   ╚██████╔╝██║ ╚═╝ ██║██║  ██║╚██████╗╚██████╗
    ╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝                                                                      
    ''')

count = 0

while True:
    
    # Getting INfo
    if count > 0:
        time.sleep(3)
    check = False
    while check == False:
        print('Trying to get data...')
        try:
            arp_list = os.popen('arp -a').read().strip('\n').split(' ')
            Iface, HWtype, HWadress = arp_list[-1], arp_list[-3], arp_list[-4]
            check = True
            print('Data found and saved!')
        except:
            print('Failed')
            print('Trying ifconfig up...')
            try:
                os.system('sudo ifconfig wlan0 up')
                print('wlan0 success!')
            except:
                print('wlan0 failed!')
                os.system('sudo ifconfig eth0 up')
                print('eth0 success!')
    # BODY
    if count > 0:
        press = input('\n\tENTER to continue...') 
    count += 1
    loading_bar(s=0.01)
    os.system('clear')
    display_logo()

    print('\n\t1. Macchange\n\t2. Set timer\n\t3. Your MAC info')
    print('\tpress q to quit')
    op = input('\n\t> ')
    if op.isnumeric() == True:
        if op == '1':
            loading_bar(s=0.02, t='\n\tChanging your MAC adress...')
            print('\n')
            macchange(Iface)
        elif op == '2':
            print('\n\tSelect the time in minutes')
            time_min = int(input('\n\t> '))
            time_sec =  time_min * 60
            loading_bar(r2=time_sec, t=f'\n\tSelected time to the next macchange: {time_min}')
            macchange(Iface)
        elif op == '3':
            print('\n')
            os.system('arp -e')
            print('\n')
            os.system(f'macchanger -s {Iface}')            
        else:        
            print('\nInvalid option.')
    else:
        if op == 'q':
            os.system('clear')
            break
        else:
            print('\nMust be numeric')