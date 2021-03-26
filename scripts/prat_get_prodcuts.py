import datetime
import timeit

import SOAPpy

client = None
session = None


def setup():
    global client, session
    # your domain here
    client = SOAPpy.WSDL.Proxy("http://www.ferreteriaprat.cl/index.php/api/v2_soap?wsdl=1&type=soap")
    # your credentials here
    session = client.login('cactus', 'C4ctusc0.s2021')


def test_update():
    global client, session
    name = 'Blackberry Playbook 7 WiFi Tablet - 64GB ' + \
           str(datetime.datetime.now())
    result = client.catalogProductUpdate(session, '10', {'name': name}, 0, 'id')
    print(result)


if __name__ == '__main__':
    print('Session Setup:')
    print(timeit.timeit('setup()',
                        setup='from __main__ import setup',
                        number=1))
    print('Updates')
    print(timeit.timeit('test_update()',
                        setup='from __main__ import test_update',
                        number=20))