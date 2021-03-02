# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import yaml
from request_data import request
import json

friend_poor=[]

def load_config():
    f = open('_config.yml', 'r',encoding='utf-8')
    ystr = f.read()
    ymllist = yaml.load(ystr, Loader=yaml.FullLoader)
    return ymllist

def gitee_issuse(friend_poor):
    print('\n')
    print('-------获取gitee友链----------')
    baselink = 'https://gitee.com'
    config = load_config()
    print('owner:', config['setting']['gitee_friends_links']['owner'])
    print('repo:', config['setting']['gitee_friends_links']['repo'])
    print('state:', config['setting']['gitee_friends_links']['state'])
    print('labelid:', config['setting']['gitee_friends_links']['labelid'])
    try:
        for number in range(1, 100):
            print(number)
            if config['setting']['gitee_friends_links']['labelid'] =='none':
                label_plus = ''
            else:
                label_plus = '&label_ids=' + str(config['setting']['gitee_friends_links']['labelid'])
            gitee = request.get_data('https://gitee.com/' +
                             config['setting']['gitee_friends_links']['owner'] +
                             '/' +
                             config['setting']['gitee_friends_links']['repo'] +
                             '/issues?state=' + config['setting']['gitee_friends_links']['state'] + label_plus +'&page=' + str(number))
            soup = BeautifulSoup(gitee, 'html.parser')
            main_content = soup.find_all(id='git-issues')
            linklist = main_content[0].find_all('a', {'class': 'title'})
            if len(linklist) == 0:
                print('爬取完毕')
                break
            for item in linklist:
                issueslink = baselink + item['href']
                issues_page = request.get_data(issueslink)
                issues_soup = BeautifulSoup(issues_page, 'html.parser')
                try:
                    issues_linklist = issues_soup.find_all('code')
                    source = issues_linklist[0].text
                    if "{" in source:
                        source = json.loads(source)
                        print(source)
                        friend_poor.append(source)
                except:
                    continue
    except Exception as e:
        print('爬取完毕')

    print('------结束gitee友链获取----------')
    print('\n')
    
def github_issuse(friend_poor):
    print('\n')
    print('-------获取github友链----------')
    baselink = 'https://github.com/'
    config = load_config()
    print('owner:', config['setting']['github_friends_links']['owner'])
    print('repo:', config['setting']['github_friends_links']['repo'])
    print('state:', config['setting']['github_friends_links']['state'])
    print('label:', config['setting']['github_friends_links']['label'])
    try:
        for number in range(1, 100):
            print(number)
            if config['setting']['github_friends_links']['label'] =='none':
                label_plus = ''
            else:
                label_plus = '+label%3A' + config['setting']['github_friends_links']['label']
            github = request.get_data('https://github.com/' +
                             config['setting']['github_friends_links']['owner'] +
                             '/' +
                             config['setting']['github_friends_links']['repo'] +
                             '/issues?q=is%3A' + config['setting']['github_friends_links']['state'] + str(label_plus) + '&page=' + str(number))
            soup = BeautifulSoup(github, 'html.parser')
            main_content = soup.find_all('div',{'aria-label': 'Issues'})
            linklist = main_content[0].find_all('a', {'class': 'Link--primary'})
            if len(linklist) == 0:
                print('爬取完毕')
                break
            for item in linklist:
                issueslink = baselink + item['href']
                issues_page = request.get_data(issueslink)
                issues_soup = BeautifulSoup(issues_page, 'html.parser')
                try:
                    issues_linklist = issues_soup.find_all('pre')
                    source = issues_linklist[0].text
                    if "{" in source:
                        source = json.loads(source)
                        print(source)
                        friend_poor.append(source)
                except:
                    continue
    except Exception as e:
        print('爬取完毕')

    print('------结束github友链获取----------')
    print('\n')


#友链规则
def get_friendlink(friend_poor):
    config = load_config()
    if config['setting']['gitee_friends_links']['enable']:
        gitee_issuse(friend_poor)
    if config['setting']['github_friends_links']['enable']:
        github_issuse(friend_poor)


get_friendlink(friend_poor)
filename='friendlist.json'
with open(filename,'w',encoding='utf-8') as file_obj:
   json.dump(friend_poor,file_obj,ensure_ascii=False)
