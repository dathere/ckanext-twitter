import json

import ckan.lib.base as base
from ckan.common import c, session
from ckanext.twitter.lib import twitter_api, cache_helpers


class TweetController(base.BaseController):
    '''
    A class exposing tweet functions as AJAX endpoints.
    '''

    def send(self, pkg_id):
        '''
        Posts the tweet given in the request body. The package ID is
        required for caching. Returns json data for displaying success/error
        messages.
        :param pkg_id: The package ID (for caching).
        :return: str
        '''
        body = dict(c.pylons.request.postvars)
        text = body.get('tweet_text', None)
        if text:
            posted, reason = twitter_api.post_tweet(text, pkg_id)
        else:
            posted = False
            reason = 'no tweet defined'
        return json.dumps({
            'success': posted,
            'reason': reason,
            'tweet': text if text else 'tweet not defined'
            })

    def clear(self, pkg_id):
        cache_helpers.remove_from_cache(pkg_id)
        if 'twitter_is_suitable' in session:
            del session['twitter_is_suitable']
            session.save()
