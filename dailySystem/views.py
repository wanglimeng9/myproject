from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from jira import JIRA
import requests, json
# Create your views here.
# def index(request):
#     return render(request, 'index.html')
from requests import Response

server = 'http://192.168.1.86:8090/'
jira = JIRA(server, basic_auth=('support_effect', 'effect12345'))


def searchIssues(jql, max_results=100):
    try:
        issues = jira.search_issues(jql, maxResults=max_results)
        return issues
    except Exception as e:
        print(e)


def get_data_key():
    list = []
    jql2 = 'component in (招聘-商业, 招聘-基础,  招聘-会员, B-profile) AND status in ("IN TEST") AND created >= 2020-11-06 AND created <=now() ORDER BY component DESC, status DESC '
    issues2 = searchIssues(jql2)
    for issue in issues2:
        data = ('{0}'.format(issue.key))
        list.append(data)
    # print(list)
    return list


def get_data_summary():
    list = []
    jql2 = 'component in (招聘-商业, 招聘-基础, 招聘-会员, B-profile) AND status in ("IN TEST") AND created >= 2020-11-06 AND created <=now() ORDER BY component DESC, status DESC '
    issues2 = searchIssues(jql2)
    for issue in issues2:
        data = ('{0}'.format(issue.fields.summary))
        list.append(data)
    # print(list)
    return list

#经办人
# def get_data_assignee():
#     list = []
#     jql2 = 'component in (招聘-商业, 招聘-基础, 招聘-会员, B-profile) AND status in ("IN TEST") AND created >= 2020-11-06 AND created <=now() ORDER BY component DESC, status DESC '
#     issues2 = searchIssues(jql2)
#     for issue in issues2:
#         data = ('{0}'.format(issue.fields.assignee))
#         list.append(data)
#     # print(list)
#     return list
#
# 报告人
# def get_data_reporter():
#     list = []
#     jql2 = 'component in (招聘-商业, 招聘-基础, 招聘-会员, B-profile) AND status in ("IN TEST") AND created >= 2020-11-06 AND created <=now() ORDER BY component DESC, status DESC '
#     issues2 = searchIssues(jql2)
#     for issue in issues2:
#         data = ('{0}'.format(issue.fields.reporter))
#         list.append(data)
#     # print(list)
#     return list

#用需求中的提测人获取RD的相关信息
def get_data_RD():
    list = []
    jql2 = 'component in (招聘-商业, 招聘-基础, 招聘-会员, B-profile) AND status in ("IN TEST") AND created >= 2020-11-06 AND created <=now() ORDER BY component DESC, status DESC '
    issues2 = searchIssues(jql2)
    for issue in issues2:
        data = ('{0}'.format(issue.fields.customfield_10503))
        list.append(data)
    # print(list)
    return list

def get_data_QA():
    list = []
    jql2 = 'component in (招聘-商业, 招聘-基础, 招聘-会员, B-profile) AND status in ("IN TEST") AND created >= 2020-11-06 AND created <=now() ORDER BY component DESC, status DESC '
    issues2 = searchIssues(jql2)
    for issue in issues2:
        data = ('{0}'.format(issue.fields.customfield_10531))
        list.append(data)
    # print(list)
    return list


def get_data_PM():
    list = []
    jql2 = 'component in (招聘-商业, 招聘-基础, 招聘-会员, B-profile) AND status in ("IN TEST") AND created >= 2020-11-06 AND created <=now() ORDER BY component DESC, status DESC '
    issues2 = searchIssues(jql2)
    for issue in issues2:
        data = ('{0}'.format(issue.fields.customfield_10505))
        list.append(data)
    # print(list)
    return list

def get_data_url(key):
    url = 'http://jira.in.taou.com/browse/' + key
    return url

def get_data_response_text(key):
    url = server + 'rest/api/2/issue/' + key
    headers = {
        'authorization': "Basic c3VwcG9ydF9lZmZlY3Q6ZWZmZWN0MTIzNDU=",
        'cache-control': "no-cache",
        'postman-token': "1bf59087-8bd9-2900-849a-563bd9425d25"
    }

    response = requests.request("GET", url, headers=headers)
    result = json.loads(response.text)
    # print(result)
    return result


# def get_data_response_text1():
#     for i in range(len(get_data_key())):
#         list = []
#         if i < len(get_data_key()):
#             data = get_data_response_text(get_data_key()[i])
#             i = i + 1
#             list.append(data)
#     print(list)
#     return list

def get_all_bug(response):
    all_bug = len(response['fields']['issuelinks'])
    # print(all_bug)
    return all_bug

# def get_all_bug1():
#     list=[]
#     for i in range(len(get_data_key())):
#         if i <len(get_data_key()):
#             all_bug=len(get_data_response_text(get_data_key()[i])['fields']['issuelinks'])
#             i = i+1
#             list.append(all_bug)
#     print(list)
#     return list


def get_unsolved_bug(all_bug, response):
    list = []
    all_list=[]
    for i in range(all_bug):
        unsolved = response['fields']['issuelinks'][i]
        if 'inwardIssue'  in unsolved:
            unsolved_status_id = unsolved['inwardIssue']['fields']['status']['id']
            if unsolved_status_id == '1':
                list.append(unsolved['id'])
        elif 'outwardIssue' in unsolved:
            unsolved_status_id1 = unsolved['outwardIssue']['fields']['status']['id']
            if unsolved_status_id1 == '1':
                list.append(unsolved['id'])
        else:
            print("啥也不用打印")
    # print(len(list))
    return (len(list))

def get_solved_bug(all_bug, response):
    list = []
    for i in range(all_bug):
        unsolved = response['fields']['issuelinks'][i]
        if 'inwardIssue'  in unsolved:
            unsolved_status_id = unsolved['inwardIssue']['fields']['status']['id']
            if unsolved_status_id == '5':
                list.append(unsolved['id'])
        elif 'outwardIssue' in unsolved:
            unsolved_status_id1 = unsolved['outwardIssue']['fields']['status']['id']
            if unsolved_status_id1 == '5':
                list.append(unsolved['id'])
        else:
            print("啥也不用打印")
    # print(len(list))
    return (len(list))

def get_all_data():
    list=[]
    for i in range(len(get_data_key())):
        if i <len(get_data_key()):
            list.append(get_data_key()[i])
            list.append(get_data_summary()[i])
            # list.append(get_data_assignee()[i])
            # list.append(get_data_reporter()[i])
            list.append(get_data_RD()[i])
            list.append(get_data_QA()[i])
            list.append(get_data_PM()[i])
            list.append(get_all_bug(get_data_response_text(get_data_key()[i])))
            list.append(get_unsolved_bug(get_all_bug(get_data_response_text(get_data_key()[i])),get_data_response_text(get_data_key()[i])))
            list.append(get_solved_bug(get_all_bug(get_data_response_text(get_data_key()[i])),get_data_response_text(get_data_key()[i])))
            list.append(get_data_url(get_data_key()[i]))
            i=i+1
    # print(list)
    # print(type(list))
    return list


def data_grouping():
    list=[]
    t=get_all_data()
    step = 9
    b = [t[i:i + step] for i in range(0, len(t), step)]
    for x in b:
        list.append(x)
    # print(list)
    return list

def get_all_result(request):
    list=[]
    list1=["需求的key", "需求的描述", "RD", "QA", "产品", "全部bug", "未解决的bug", "未验证的bug", "jira地址"]
    list2=data_grouping()
    for i in range(len(list2)):
        d = {}
        if i <len(list2):
            for j in range(len(list1)):
                if j<len(list1):
                    d[list1[j]]=list2[i][j]
                    j = j + 1
            list.append(d)
            i = i + 1
    # print(list)
    data = {i: v for i, v in enumerate(list)}

    return JsonResponse(data, safe=False)
    # dict1 = {}
    # dict1["id"] = 1
    # dict1["result"] = "success"
    # return Response(dict1)

###################

if __name__ == '__main__':
    print(get_all_result())

