# -*- coding: UTF-8 -*-

import requests
from aws_utils import dynamodb_util as dynamodb, sns_util as sns, comprehend_util as comprehend
import commons
from datetime import datetime


def send_message(languages, since, new_repos):
    """
    Send message to the subscribers

    :param languages: e.g. python/java
    :param since: daily/weekly/monthly
    :param new_repos: new trending repository
    :return: None
    """
    if len(new_repos) == 0:
        print("No new delta!!! " + str(datetime.now()))
    else:
        reply = '🤝 Greetings!\n\n Here are new trending ' + since + ' repositories for ' + commons.trim_brackets(
            languages) + ' language(s) :\n\n'

        for new_repo in new_repos:
            description = new_repo['description']
            print(description.strip())

            if description.strip() and comprehend.detect_language(description) == 'en':
                if len(description) > 150:
                    description = description[:150] + "..."
                msg = "Name : " + new_repo['name'] + "\nURL : " + new_repo['url'] + "\nLanguage : " + new_repo[
                    'language'] + "\nDescription: " + description + "\n\n"
                reply = reply + msg

        reply = reply + "\nLove,\nDBot 🤖"
        sns.send_notification(reply)


def fetch_trending_repo(languages, since):
    """
    Fetch trending repositories from github using https://github.com/huchenme/github-trending-api
    And insert in dynamodb

    :param languages: e.g. python/java
    :param since: daily/weekly/monthly
    :return: None
    """
    for language in languages:
        url = commons.URL_PREFIX + 'language=' + language + '&since=' + since
        response_list = requests.get(url).json()

        for response in response_list:
            data = {'name': response['name'], 'description': response['description'], 'url': response[
                'url'], 'language': language, 'added_on': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            #print(response['url'])
            dynamodb.insert_data(data)
        print("successfully inserted top repository for language - " + language + " at " + datetime.now().strftime(
            '%Y-%m-%d %H:%M:%S'))


def find_new_trending_repo(languages, since):
    """
    Find new trending repository on github and update delta in dynamodb and send notification to the subscribers
    :param languages: e.g. python/java
    :param since: daily/weekly/monthly
    :return: None
    """
    new_repos = []
    for language in languages:
        url = commons.URL_PREFIX + 'language=' + language + '&since=' + since
        response_list = requests.get(url).json()

        for response in response_list:
            if not dynamodb.check_if_exists(response['url'], language):
                data = {'name': response['name'], 'description': response['description'], 'url': response[
                    'url'], 'language': language, 'added_on': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                print(response['url'])
                dynamodb.insert_data(data)
                new_repos.append(data)
    print("New Trending repositories - " + str(new_repos))
    send_message(languages, since, new_repos)


    # run as per frequency (since field)
    # fetch_trending_repo(['java', 'python'], 'weekly')


find_new_trending_repo(['java', 'python'], 'weekly')
