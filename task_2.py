import urllib.request, urllib.parse, urllib.error
import oauth
import hidden
import json

# https://apps.twitter.com/
# put your keys in hidden.py

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


def test_me(api_url, name):
    '''
    get json file from twitter API

    '''
    url = augment(api_url,
                  {'screen_name':name , 'count': '35'})
    connection = urllib.request.urlopen(url)
    data = connection.read()

    return json.loads(data)



def for_dict(json_file):
    '''
    This recursio function
    '''
    print('There are such keys in dictionary: ', end='')
    print(list(json_file.keys()), end=' ')
    print('please enter the key name which value you want to view.')
    n = input('Also, if you want to get information about all keys please enter /all: ')
    if n == '/all':
        return json_file
    elif n not in json_file:
        print('Sorry, you entered the wrong value! Try again')
        return for_dict(json_file)
    elif type(json_file[n]) == dict:
        return for_dict(json_file[n])
    elif type(json_file[n]) == list:
        return for_lst(json_file[n])
    else:
        print('The value of the entered key is:')
        return json_file[n]


def for_lst(some_lst):
    if len(some_lst) == 0:
        print('This value is empty')
        return
    print('The length of the list is ', end='')
    print(len(some_lst), end=' ,')
    print('enter the number of a index that you want to view (0-', end='')
    print(len(some_lst) - 1, end='')
    print(')')
    n = input('Also, if you want to view all list please enter /all:')
    if n == '/all':
        return some_lst
    n = int(n)
    if n < 0 or n > len(some_lst):
        print("Sorry, you entered the wrong value! Try again")
        return for_lst(some_lst)
    elif type(some_lst[n]) == dict:
        return for_dict(some_lst[n])
    elif type(some_lst[n]) == list:
        return for_lst(some_lst[n])
    else:
        print('The value of the entered index is:')
        return some_lst[n]

# EXAMPLE HOW MODULE WORKS:
#print(for_dict(test_me('https://api.twitter.com/1.1/friends/list.json','drchuck')))