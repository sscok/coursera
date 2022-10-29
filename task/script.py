import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE="https://www.coursera.org"
URL = "https://www.coursera.org/browse"

def find_categories(URL):

    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    cols = soup.find_all('div', class_=["promoted-topic-column","topic-column"])
    category_url=[]
    for col in cols:
        for i in range(len(col)):
            category_url.append({'category': col.find_all('a')[i]['aria-label'],'url': col.find_all('a')[i]['href']})

    return category_url


def get_url(category):
    categories=find_categories(URL)
    url = [x['url'] for x in categories if category == x['category']]
    split=url[0].split('/')
    return split[len(split)-1]

def get_course_list(category):
    url=URL + '/' + get_url(category)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    courses = soup.find_all('div', class_="rc-CardSection productCard-titleSection")
    course_url=[]
    for course in courses:
        course_url.append({'course': course.find('a').text,'url': course.find('a', class_="CardText-link")['href']})
    return course_url

def get_attr(category):
    all_courses=get_course_list(category)
    attributes=[]
    for course in all_courses:
        url=BASE + course['url']
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        name = course['course'] if soup.find('h1', class_="banner-title m-b-0") == None else soup.find('h1', class_="banner-title m-b-0").text
        try:
            instructor = soup.find('div', class_="rc-BannerInstructorInfo rc-BannerInstructorInfo__seo-experiment").text.split(' +')[0]
            if "Top" in instructor:
                instructor = instructor.split('Top')[0]
            description = soup.find('div', class_="description").text
            enr=soup.find('div', class_="_1fpiay2")
            enrolled = 'NA' if enr == None else enr.text.split(' ')[0] 
            rating = soup.find('div', class_="_wmgtrl9").text.split(" ")[0]
            sub_categories=soup.find_all('div', class_="_1ruggxy")
            sub_category=sub_categories[len(sub_categories)-1]
            if sub_categories[len(sub_categories)-2].text == category:
                sub_category=sub_categories[len(sub_categories)-1].text
            else:
                continue            
        except AttributeError:
            try:
                instructor = soup.find('h3', class_="instructor-name headline-3-text bold").text
                description = soup.find('div', class_="description").text
                enrolled = soup.find('div', class_="_1fpiay2").text.split(' ')[0]
                rating = soup.find('div', class_="_wmgtrl9").text.split(" ")[0]
                if sub_categories[len(sub_categories)-2].text == category:
                    sub_category=sub_categories[len(sub_categories)-1].text
                else:
                    continue            

            except (TypeError, AttributeError) as e:
                try:
                    name = course['course'] if soup.find('h1', class_="cds-33") == None else soup.find('h1', class_="cds-33 css-1shw822 cds-35").text
                    instructor = soup.find('p', class_="cds-33 css-1j071wf cds-35").text.split(' +')[0]
                    description = soup.find('div', class_="content-inner").text
                    ratings = soup.find('p', class_="cds-33 css-14d8ngk cds-35").text.split(" ")
                    rating = ratings[0]
                    enrolled = ratings[2]
                    sub_categories=soup.find_all('ol', class_="css-1sswpa3")
                    sub_category=sub_categories[len(sub_categories)-1]
                    if sub_categories[len(sub_categories)-2].text == category:
                        sub_category=sub_categories[len(sub_categories)-1].text
                    else:
                        continue
                except:
                    continue
        if "Top" in instructor:
            instructor = instructor.split('Top')[0]
        data={'Category Name': sub_category, 'Course Name': name, 'First Instructor Name': instructor.strip(), 'Course Description': description, '# of Students Enrolled': enrolled, '# of Ratings': rating}
        attributes.append(data)
    return attributes
