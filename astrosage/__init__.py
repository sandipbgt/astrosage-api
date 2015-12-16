# -*- coding: utf-8 -*-
"""
    astrosage
    ~~~~~~~~~~~~~

    astrosage module
"""

from datetime import date, timedelta
from collections import OrderedDict
from requests import get
from requests.exceptions import RequestException, Timeout
from lxml import etree
from six import u

__version__ = '0.1.0'

def is_valid_sunsign(sunsign):
    sunsigns = ['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces']
    if sunsign not in sunsigns:
        return False
    return True

def is_valid_horoscope_type(_type):
    _types = ['daily', 'weekly', 'monthly', 'yearly']
    if _type not in _types:
        return False
    return True

class HoroscopeException(Exception):
    """
    Horoscope exception
    """

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        """ Try to pretty-print the exception, if this is going on screen. """

        def red(words):
            return u("\033[31m\033[49m%s\033[0m") % words

        def blue(words):
            return u("\033[34m\033[49m%s\033[0m") % words

        msg = (
                "\n{red_error}"
                "\n\n{message}\n".format(
                    red_error=red("Error occured"),
                    message=blue(str(self.msg))
                ))
        return msg

class Horoscope(object):

    def __init__(self, sunsign=None):
        """
        Create a Horoscope
        """

        if not is_valid_sunsign(sunsign):
            raise HoroscopeException("Invalid horoscope sunsign")

        self.sunsign = sunsign.lower()

        self.base_url_string = "http://astrosage.com/horoscope/%s-%s-horoscope.asp"
        self.weekly_love_url_string = "http://astrosage.com/horoscope/weekly-%s-love-horoscope.asp"

        self.parser = etree.HTMLParser()

    def _get_horoscope(self, _type=None):
        """gets a horoscope from site html

        :param day: day for which to get horoscope. Default is 'today'

        :returns: dictionary of horoscope details
        """
        if not is_valid_horoscope_type(_type):
            raise HoroscopeException("Invalid horoscope type. Allowed days: [daily|weekly]" )

        try:
            html_resp = get(self.base_url_string % (_type, self.sunsign))
        except Timeout as e:
            raise HoroscopeException(e)
        except RequestException as e:
            raise HoroscopeException(e)

        tree = etree.fromstring(html_resp.text, self.parser)
        horoscope = str(tree.xpath('//*[@id="roundborder"]/div[2]/div[3]/div[3]/div[2]/text()')[0])

        data = OrderedDict()
        data['type'] = _type
        data['sunsign'] = self.sunsign.capitalize()
        data['horoscope'] = horoscope

        return data

    def daily(self):
        """get daily horoscope

        :returns: dictionary of daily horoscope details
        """
        return self._get_horoscope('daily')

    def weekly(self):
        """get weekly horoscope

        :returns: dictionary of weekly horoscope details
        """
        return self._get_horoscope('weekly')

    def monthly(self):
        """get monthly horoscope

        :returns: dictionary of monthly horoscope details
        """

        try:
            html_resp = get(self.base_url_string % ('monthly', self.sunsign))
        except Timeout as e:
            raise HoroscopeException(e)
        except RequestException as e:
            raise HoroscopeException(e)

        tree = etree.fromstring(html_resp.text, self.parser)

        category_general = str(tree.xpath('//*[@id="roundborder"]/div[2]/div[3]/div[2]/p[1]/text()')[0])
        category_health = str(tree.xpath('//*[@id="roundborder"]/div[2]/div[3]/div[2]/p[2]/text()')[0])
        category_family_friends = str(tree.xpath('//*[@id="roundborder"]/div[2]/div[3]/div[2]/p[3]/text()')[0])
        category_trade_finance = str(tree.xpath('//*[@id="roundborder"]/div[2]/div[3]/div[2]/p[4]/text()')[0])
        category_advice = str(tree.xpath('//*[@id="roundborder"]/div[2]/div[3]/div[2]/p[5]/text()')[0])
        lucky_days_auspicious_dates = str(tree.xpath('//*[@id="roundborder"]/div[2]/div[3]/div[2]/p[6]/text()')[0]).replace('Auspicious dates: ', '')
        lucky_days_inauspicious_dates = str(tree.xpath('//*[@id="roundborder"]/div[2]/div[3]/div[2]/p[6]/text()')[1]).replace('\nInauspicious dates: ', '')

        data = OrderedDict()
        data['type'] = 'monthly'
        data['sunsign'] = self.sunsign.capitalize()
        data['horoscope'] = OrderedDict()
        data['horoscope']['general'] = category_general
        data['horoscope']['health'] = category_health
        data['horoscope']['family_friends'] = category_family_friends
        data['horoscope']['trade_finance'] = category_trade_finance
        data['horoscope']['advice'] = category_advice
        data['horoscope']['lucky_days'] = OrderedDict()
        data['horoscope']['lucky_days']['auspicious_dates'] = lucky_days_auspicious_dates
        data['horoscope']['lucky_days']['inauspicious_dates'] = lucky_days_inauspicious_dates

        return data

    def yearly(self):
        """get yearly horoscope

        :returns: dictionary of yearly horoscope details
        """

        try:
            html_resp = get(self.base_url_string % ('yearly', self.sunsign))
        except Timeout as e:
            raise HoroscopeException(e)
        except RequestException as e:
            raise HoroscopeException(e)

        tree = etree.fromstring(html_resp.text, self.parser)

        category_general = str(tree.xpath('//*[@id="roundborder"]/div[2]/div[3]/div[2]/div[4]/text()')[0])
        category_career = str(tree.xpath('//*[@id="roundborder"]/div[2]/div[3]/div[2]/div[6]/text()')[0])
        category_finance = str(tree.xpath('//*[@id="roundborder"]/div[2]/div[3]/div[2]/div[8]/text()')[0])
        category_health = str(tree.xpath('//*[@id="roundborder"]/div[2]/div[3]/div[2]/div[10]/text()')[0])
        category_love_marriage_personal_relations = str(tree.xpath('//*[@id="roundborder"]/div[2]/div[3]/div[2]/div[12]/text()')[0])
        category_family_friends = str(tree.xpath('//*[@id="roundborder"]/div[2]/div[3]/div[2]/div[14]/text()')[0])
        category_advice = str(tree.xpath('//*[@id="roundborder"]/div[2]/div[3]/div[2]/div[16]/text()'))

        data = OrderedDict()
        data['type'] = 'yearly'
        data['sunsign'] = self.sunsign.capitalize()
        data['horoscope'] = OrderedDict()
        data['horoscope']['general'] = category_general
        data['horoscope']['career'] = category_career
        data['horoscope']['finance'] = category_finance
        data['horoscope']['health'] = category_health
        data['horoscope']['love_marriage_personal_relations'] = category_love_marriage_personal_relations
        data['horoscope']['family_friends'] = category_family_friends

        return data

    def weekly_love(self):
        """get weekly love horoscope from site html

        :returns: dictionary of weekly love horoscope details
        """

        try:
            html_resp = get(self.weekly_love_url_string % self.sunsign)
        except Timeout as e:
            raise HoroscopeException(e)
        except RequestException as e:
            raise HoroscopeException(e)

        tree = etree.fromstring(html_resp.text, self.parser)
        horoscope = str(tree.xpath('//*[@id="roundborder"]/div[2]/div[2]/div[3]/div[2]/text()')[0])

        data = OrderedDict()
        data['type'] = 'weekly-love'
        data['sunsign'] = self.sunsign.capitalize()
        data['horoscope'] = horoscope

        return data