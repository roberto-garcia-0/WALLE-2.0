from pump_system import pump_system

def main():
    p = pump_system()
    try:
        p.collectSample(1)
    except KeyboardInterrupt:
        p.clean()
        exit(0)
    
    

if __name__ == '__main__':
    main()
