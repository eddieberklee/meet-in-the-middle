# Nikita Kouevda, Eddie Lee, Anthony Sutardja
# 2012/11/10

import json, oauth2, urllib, urllib2

def places(point="37.8717,-122.2728", category="restaurants", limit="5", sort="1", host="api.yelp.com", path="/v2/search", consumer_key="QiJTR2MWOMpYsWtGdDdq6Q", consumer_secret="-ow0GK_lnQ9jSBoNEK9AH85DZXM", token="nSrMPVUVRkcDA9unjmOREopRKMfN5OyP", token_secret="ij9D71EGJeohhvNdHKih3kwH9n8"):
    # URL params
    url_params = {"ll": point, "category_filter": category, "limit": limit, "sort": sort}

    # Encoded params
    encoded_params = urllib.urlencode(url_params)

    # Unsigned URL
    url = 'http://%s%s?%s' % (host, path, encoded_params)

    # Sign the URL
    consumer = oauth2.Consumer(consumer_key, consumer_secret)
    oauth_request = oauth2.Request('GET', url, {})
    oauth_request.update({'oauth_nonce': oauth2.generate_nonce(), 'oauth_timestamp': oauth2.generate_timestamp(), 'oauth_token': token, 'oauth_consumer_key': consumer_key})

    token = oauth2.Token(token, token_secret)
    oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
    signed_url = oauth_request.to_url()

    # Connect
    try:
        conn = urllib2.urlopen(signed_url, None)
        response = json.loads(conn.read())
        conn.close()

        results = response["businesses"]
        return [{"address": str(result["location"]["address"][0]), "name": str(result["name"]), "image_url": str(result["image_url"])} for result in results]
    except:
        return None
