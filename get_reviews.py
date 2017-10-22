import requests
from pyquery import PyQuery as pq
from datetime import datetime

def construct_form_data(app_id, page_n):
    form_data = {
        "reviewType": 0,
        "pageNum": page_n,
        "id": app_id,
        "xhr": 1,
        "token": "rqjOBqwuYgCQlEuuKuKW0sCMdaA:1508469536771"
    }
    return form_data

def replace_unicode(text):
    ret = text
    ret = ret.replace('\\u003c', '<')
    ret = ret.replace('\\u003e', '>')
    ret = ret.replace('\\u003d', '=')
    ret = ret.replace('\\u0026', '&')
    ret = ret.replace('\\u200b', '')
    ret = ret.replace('\\"', '"')
    return ret


def get_one_page_reviews(app_id, page_n):
    """ Get one page reviews of an application"""

    request_url = "https://play.google.com/store/getreviews?hl=en"
    f_data = construct_form_data(app_id, page_n)
    res = requests.post(request_url, data=f_data)
    html_text = replace_unicode(res.text)
    html = pq(html_text)
    reviews = html('.review-body')
    ret = []
    if len(reviews) > 0:
        for review in reviews:
            review = pq(review)
            text = review.text()
            text = text[:-len("Full Review ")]
            ret.append(text)
    return ret


def get_reviews_of_one_app(app_id):
    """ Get all reviews of one application by given application id"""
    page_n = 0
    reviews_collector = []
    while page_n >= 0:
        reviews = get_one_page_reviews(app_id, page_n)
        reviews_collector.extend(reviews)
        if len(reviews) == 0:
            page_n = -1
        else:
            page_n += 1
    return reviews_collector


def log_complete(log_loc, appid):
    """ log out which app has completed"""
    with open(log_loc, 'a') as log_f:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_f.write(now + ' ' + appid + ' complete')
        log_f.write('\n')


def get_app_ids():
    """ get app ids list"""
    ret = []
    with open('./appsid.txt', 'r') as appids:
        ids = appids.readlines()
        for i in ids:
            i = i.strip()
            ret.append(i)
    return ret


def get_reviews(appsid, start):
    """ Get all reviews of appsid list"""
    for i in range(start, len(appsid)):
        appid = appsid[i]
        reviews = get_reviews_of_one_app(appid)
        save_reviews(reviews, './data/'+appid+'.txt')
        log_complete('./log.txt', appid)


def save_reviews(reviews, file_loc):
    """ Save reviews into file"""
    with open(file_loc, 'w') as output:
        for review in reviews:
            output.write(review)
            output.write('\n')


def main():
    """ main function"""
    appids = get_app_ids()
    get_reviews(appids, start=0)

if __name__ == '__main__':
    main()
