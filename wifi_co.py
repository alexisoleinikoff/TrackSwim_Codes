import os

interface = 'wlan0'
name = 'HHJ-43488'
password = '42xi-4d8v-qany-ixxu'


os.system('iwconfig'+interface+'essid'+name+'key'+password)