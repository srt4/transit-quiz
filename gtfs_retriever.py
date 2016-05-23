import requests
import click

# Go to http://transitfeeds.com/api/keys to get an API key
api_key = 'REPLACE_ME'

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
