import requests
import click
import shutil
import zipfile

# Go to http://transitfeeds.com/api/keys to get an API key
api_key = 'TODO'

@click.command()
def list_agencies():
    r = requests.get('https://api.transitfeeds.com/v1/getLocations?key='
            + api_key)
    response = r.json()
    for location in response['results']['locations']:
        print ' * ' + location['t'] + ': [' + str(location['id']) + ']'
    print
    retrieve_agency()

@click.command()
@click.option('--id', prompt=' -- Which ID would you like to download?',
              help='The agency ID to download')
def retrieve_agency(id):
    print
    print " -- Okay, we're going to download the GTFS bundle for " + id
    r = requests.get('https://api.transitfeeds.com/v1/getFeeds?key=' +
            api_key + '&location=' + id)
    response = r.json()
    try:
        bundle_url = response['results']['feeds'][0]['u']['d']
        print
        print " -- The URL for the bundle is " + str(bundle_url)
        r = requests.get(bundle_url, stream=True)
        if r.status_code == 200:
            filename = 'gtfs/' + response['results']['feeds'][0]['id'].split('/')[0] + '.zip'
            with open(filename, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
                print
                print " -- Saved bundle to " + filename
                print
                print " -- Unzip the file into gtfs/ with $ unzip " + filename
                        + " and update transit_quiz.py#10"
        else:
            raise Exception("Could not download bundle...")
    except:
        print "Could not determine bundle URL for agency \n " + str(response)
        raise

if __name__ == '__main__':
    list_agencies()
