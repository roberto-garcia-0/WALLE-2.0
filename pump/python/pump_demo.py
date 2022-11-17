from pump_system import pump_system

def main():
    p = pump_system()
    try:
        p.demo()
    finally:
        p.cleanup()

if __name__ == '__main__':
    main()