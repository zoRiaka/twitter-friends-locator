import urllib.request, urllib.parse, urllib.error
import oauth
import hidden
import json
import folium

def augment(url, parameters):
    secrets = hidden.oauth()
    consumer = oauth.OAuthConsumer(secrets['consumer_key'],
                                   secrets['consumer_secret'])
    token = oauth.OAuthToken(secrets['token_key'], secrets['token_secret'])

    oauth_request = oauth.OAuthRequest.from_consumer_and_token(consumer,
                                                               token=token, http_method='GET', http_url=url,
                                                               parameters=parameters)
    oauth_request.sign_request(oauth.OAuthSignatureMethod_HMAC_SHA1(),
                               consumer, token)
    return oauth_request.to_url()


def collect_friends(name):
    # print('* Calling Twitter...')
    url = augment('https://api.twitter.com/1.1/friends/list.json',
                  {'screen_name': name, 'count': '100'})
    # print(url)
    connection = urllib.request.urlopen(url)
    data = connection.read()
    # headers = dict(connection.getheaders())
    # print(headers)
    return json.loads(data)


def get_location(name):
    dict1 = collect_friends(name)
    return_list = []
    users_info = dict1['users']
    for i in range(len(users_info)):
        return_list.append((users_info[i]["screen_name"], users_info[i]["location"]))
    return return_list


def get_coord(name):
    coord = []
    locations = get_location(name)
    from geopy.geocoders import Nominatim
    geolocator = Nominatim(user_agent='User123', timeout=3)
    print(len(locations))
    for i in range(len(locations)):
        try:
            location = geolocator.geocode(locations[i][1])
            assert isinstance(location.longitude, object)
            coord.append((location.latitude, location.longitude, locations[i][0]))
        except AttributeError:
            pass
    return coord




def map_gener(name):
    lst=get_coord(name)
    m=folium.Map(location=[10,0], zoom_start=2)
    for i in range(len(lst)):
        folium.Marker([lst[i][0], lst[i][1]],popup=lst[i][2]).add_to(m)
    m.save('templates\map.html')

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('new.html')

@app.route('/send', methods=['POST'])
def send():
    if request.method == 'POST':
        name = request.form['name']
        map_gener(name)
        return render_template('map.html')
    return render_template('new.html')

if __name__ == "__main__":
    app.run()
