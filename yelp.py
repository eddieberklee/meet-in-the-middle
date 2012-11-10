# Nikita Kouevda, Eddie Lee, Anthony Sutardja
# 2012/11/10

import json, oauth2, urllib, urllib2

def results(location="2599 Hearst Ave, Berkeley, CA 94709", radius="800", category="restaurants", limit="5", sort="2", host="api.yelp.com", path="/v2/search", consumer_key="X7e6zliG8gBvtgy_2wf9Aw", consumer_secret="RJjzuCabr65kHqiH7JxhNk3K-H4", token="5tnxLUliPPENIFMtrTpQUDrgtbuu3Ukw", token_secret="lQ51AJSBQfpMuJ8gxT7eVD7ZRQw"):
    # URL params
    url_params = {"location": location, "radius_filter": radius, "category_filter": category, "limit": limit, "sort": sort}

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

        return {"results": [{"address": str(result["location"]["address"][0]), "name": str(result["name"])} for result in results]}
    except:
        return None
