from port import *
from random import randint

ships_string = """ukkie,100,150,200,400,5
retainer,150,200,500,500,10
grande,150,220,500,600,20
luchador,150,200,200,600,30
xi-min,180,230,600,800,50
sensui,160,240,300,800,70
eldiablo,200,260,600,900,100
massachusetts,180,300,300,10000,150"""

if __name__ == "__main__":
    docks = []
    ships = []
    for i in range(2):
        docks.append(Dock('Simple dock {}'.format(i)))

    for shipstr in ships_string.split('\n'):
        shiparr = shipstr.split(',')
        ships.append(
            Ship(shiparr[0], int(shiparr[1]), int(shiparr[2]), int(shiparr[3]), int(shiparr[4]), int(shiparr[5]),
                 randint(0, int(shiparr[5])), DockingPurpose.Unloading))

    for ship in ships:
        print(ship)

    port = Port('Haven', 'Rotterdam', 300, docks)
    print(port)

    """first come first serve"""
    cont = True
    cycle = 0
    while cont:
        for ship in ships:
            if ship.containers != 0 and ship.purpose == DockingPurpose.Unloading or \
                    ship.containers != ship.max_containers and ship.purpose == DockingPurpose.Loading:
                status, x = port.request_place(ship)
                if status and not ship.busy:
                    x.dock_ship(ship)
                    print('Starting to process: ', ship.get_status())
                else:
                    print(x)
            else:
                print('Ship already done and on its way home!', ship.get_status())

        cycle += 1
        print('========================= Cycle {} ========================='.format(cycle))

        for dock in port.docks:
            weather_clear, warnings = port.check_custom_weather(1000, 62)
            if weather_clear:
                dock.process()
                print('Processing: ', dock)
                if dock.docked_ship is not None:
                    print('Docked ship: ', dock.docked_ship.get_status())
            else:
                for warning in warnings:
                    print(warning)

        i = input('Continue?')
        cont = i.lower() == 'y'
