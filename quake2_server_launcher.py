#!/usr/bin/env python
import requests
from lxml import html
import os
import subprocess
import sys

def return_q2_server_strings():
    q2_server_url = 'http://q2servers.com/?s=pd'

    user_agent_string = 'Mozilla/5.0'
    user_agent = {'User-agent': user_agent_string}
    ssl_verify=False
    page = requests.get(q2_server_url, headers = user_agent, verify=ssl_verify)
    http_code = page.status_code
    if http_code != 200:
        print("Error HTTP RESPONSE " + http_code + " exiting now.")
        exit()
    tree = html.fromstring(page.content)

    server_list = []
    servers = tree.xpath("//*[@class='server']")
    for i in range(0, 9, 1):
        for element, attribute, link, pos in servers[i].iterlinks():
            if 'quake2' in link:
                server_addr = link.replace("quake2://","")
                server_list.append('set adr' + str(i) + ' "' + server_addr + '"')
    return server_list

cfg_list = []
cfg_file = os.path.join(os.environ['HOME'] ,'.yq2/baseq2/config.cfg')

## Read in the existing config file without server addresses and store as list
if os.path.isfile(cfg_file):
    with open(cfg_file) as q2file:
        q2_lines = q2file.readlines()
        for line in q2_lines:
            if 'set adr' not in line:
                cfg_list.append(line.rstrip(os.linesep))

    ## Write the new config file with our scraped servers appended to the end
    cfg_list = cfg_list + return_q2_server_strings()
    with open(cfg_file,'w') as q2file:
        for line in cfg_list:
             q2file.write(line + os.linesep)

if os.uname()[0] == 'Darwin':
    os.environ["PATH"] += os.pathsep + '/Applications/Quake 2.app/Contents/Resources/'
subprocess.Popen(['quake2'])
exit()
