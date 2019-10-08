import time

if __name__=='__main__':
    with open('/opt/demo_data/parameters.list') as f:
        lines = f.readlines()
    
    try:
        delay = 0
        for l in lines:
            if 'BOOT_DELAY' in l:
                delay = int(l.split(",")[1])
    except:
        delay = 20
    print('Going to sleep', delay, 'seconds')
    time.sleep(delay)
    print('Delay done!')

