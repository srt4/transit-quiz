import requests
import click

api_key = '4bd02eb9-d9c4-47f8-a4e5-fdc23ee0f342'

@click.command()
def list_agencies():
    r = requests.get('https://api.transitfeeds.com/v1/getLocations?key='
            + api_key)
    response = r.json()
    for location in response['results']['locations']:
        print ' * ' + location['t'] + ': [' + str(location['pid']) + ']'
    print
    retrieve_agency()

@click.command()
@click.option('--pid', prompt='Which PID would you like to download?',
              help='The agency PID to download')
def retrieve_agency(pid):
    print "Okay, we're going to download the GTFS bundle for " + pid

if __name__ == '__main__':
    list_agencies()
