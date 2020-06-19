import os, requests, time

try:
  os.system('pip3 install proxyscrape')
  from proxyscrape import create_collector, get_collector
  os.system('sudo service tor start')
  os.system('sudo service tor status')
  print('\n\tTor is working!')
  time.sleep(5)
except:
  print('\nTor service down or proxyscrape not found.')
finally:
  os.system('clear')

######
def add_data(data, path_config, mode):
  with open(path_config, mode) as proxychains_config: 
    proxychains_config.write(data)

def check_ping(proxy_list, lenght, packages=3):
  filtered_proxies = []
  count = 0
  for i in proxy_list:
    if count <= lenght:
      try:
        l = list(i)
        host, port, country, anonymous, Type = l[0], l[1], l[3], l[4], l[5]
        average_ping = os.popen(f'ping -c {packages} -p {port} -q {host} | grep avg').read()
        average_ping = float(average_ping.split('/')[4])
        if anonymous == True:
          if Type != 'https' and Type != 'http':
            if average_ping <= 200:
              count += 1
              print(f'{count}.| host:port {host}:{port} | country: {country} | type: {Type} | anonymous: {anonymous} | ping: {average_ping}')
              filtered_proxies.append([Type, host, port])
      except:
        print(False)
        pass
    else:
      break
  return filtered_proxies

####BODY#####

# path
path_config = '/etc/proxychains.conf'

# Create collector
collector = create_collector('my-collector', ['socks4', 'socks5']) # Proxy(host='81.252.38.12', port='8080', code='fr', country='france', anonymous=True, type='http', source='free-proxy-list')

# Proxy list scrapped
proxies = collector.get_proxies({'anonymous':True})

# Options
print('\n\t@@@## C H E C K I N G--P R O X Y--L I S T: ##@@@\n')
print(f'\t- Lenght: {len(proxies)}')
print('\tInput the lenght of the list and set the packages per ping (recommended between 1-7). Every package will be sent with an interval of 1 sec.')
print('\tE.g.: LENGHT PACKAGES')
print('\t       120      3')
check = False
while check == False:
  lenght, pcks = input('\n\t> ').split(' ')
  if lenght.isnumeric() == True:
    if pcks.isnumeric() == True:
      check = True
  else:
    print('\tYou must input lenght and packages. E.g.: 100 1')

# Check ping and anonymous state from list
proxy_list = check_ping(proxy_list=proxies, lenght=int(lenght), packages=pcks)

# Create a check_point
check_point = '# Proxy_list:'
with open(path_config, 'a+') as f:
  for line in f:
    if check_point in line:
      break
    else:
      add_data('# Proxy_list:', path_config=path_config, mode='a')

# add proxies filtered
for i in proxy_list:
  data = (' '.join(i) + '\n')
  add_data(data=data, path_config=path_config, mode='a')

print('\n')
os.system('proxychains curl ifconfig.me/ip')
print('\nSuccessfully completed.')