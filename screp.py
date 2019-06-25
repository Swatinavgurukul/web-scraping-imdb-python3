import requests
from bs4 import BeautifulSoup
from pprint import pprint
import json
import os
import random
import time
from pathlib import Path

URL = "https://www.imdb.com/india/top-rated-indian-movies/?ref_=nv_mv_250_in"

# TASK-1
# (for cound filels -1 | wc -l)
def scrap_to_tist():

    sample = requests.get(URL)
    soup = BeautifulSoup(sample.text, "html.parser")

    tbody = soup.find('tbody', class_="lister-list")
    # print tbody
    trs = tbody.findAll('tr')
    whole_data = []
    j = 0
    for i in trs:
        movies_data = {}
        position = j = j+1

        name = i.find('td', class_="titleColumn").a.get_text()
        # print name
        year = i.find('td', class_="titleColumn").span.get_text()
        # print year
        reng = i.find('td', class_="ratingColumn").get_text()
        # print reng
        link = i.find("a")
        # print link
        movie_link = "https://www.imdb.com/"+link["href"]
        # print movie_link
        movies_data["position"] = position
        movies_data["name"] = name
        movies_data["year"] = int(year[1:5])
        movies_data["reting"] = float(reng)
        movies_data["url"] = movie_link

        whole_data.append(movies_data)
    return whole_data


scrept = scrap_to_tist()
# pprint (scrept)

# Task - 2


def group_by_year(movies):

    years = []
    for i in movies:
        year = i["year"]
        if year not in years:
            years.append(year)

    movie_dict = {i: []for i in years}

    for i in movies:
        year = i["year"]
        for x in movie_dict:
            if str(x) == str(year):
                movie_dict[x].append(i)
    return movie_dict


year_wais = group_by_year(scrept)
# pprint (year_wais)

# TASK-3


def group_by_decade(movies):
    moviedec = {}
    list1 = []
    for index in movies:
        mod = index % 10
        # print mode
        decade = index-mod
        # print decade
        if decade not in list1:
            list1.append(decade)

    for i in list1:
        moviedec[i] = []
    for i in moviedec:
        drc10 = i+9
        for x in movies:
            if x <= drc10 and x >= i:
                for v in movies[x]:
                    moviedec[i].append(v)
    return (moviedec)


decade_movies = group_by_decade(year_wais)
# pprint (decade_movies)


# Task - 4
def scrape_top_list(movie_url):
    # print movie_url
    # print(cast)
    Id = movie_url.split("/")
    file_name_id = Id[5]
    # print file_name_id

    # Task - 8
    file_name = "IMDB-caching/"+file_name_id+".json"
    filepath = Path(file_name)
    if filepath.exists():
        with open(file_name,'r') as json_data:
            data = json_data.read()
            data2 = json.loads(data)
            # print ("exist")
        return data2

    else:
        # print ("file not exsits")
        movies_data_scrape = {}
        sample = requests.get(movie_url)
        soup = BeautifulSoup(sample.text, "html.parser")
        # Task - 13
        table=soup.find('table',class_="cast_list")
        trs=table.find_all('tr')
        cast=[]
        for tr in trs:
            # print (tr)
            tds=tr.find_all('td',class_='')
            new={}
            for act in tds:
                a=act.find('a')
                name = (a.get_text())
                imdb_id = (a['href'])[6:15]
                new['imdb_id']=imdb_id
                new['name']=name
                cast.append(new)

        movie_name = soup.find('h1', class_="").get_text().split("(")
        # return movie_name[0]

        movie_Directors = soup.find('div', class_="credit_summary_item")
        director_list = movie_Directors.findAll("a")
        director_name = []
        for i in director_list:
            director_name.append(i.get_text())
        # return director_name
        # return movie_Directors[0]

        movie_poster_link = soup.find("div", class_="poster").a["href"]
        movie_poster = "https://www.imdb.com"+movie_poster_link
        # return movie_poster

        movies_bio = soup.find("div", class_="summary_text").get_text().strip()
        # return movies_bio
        movie_genres1 = soup.find("div", class_="subtext")
        gener = movie_genres1.findAll("a")
        gener.pop()
        movie_gener = []
        for i in gener:
            movie_gener.append(i.get_text())
        # return movie_gener
        extra_details = soup.find("div", attrs={"class": "article", "id": "titleDetails"})
        list_of_div = extra_details.find_all("div")
        for div in list_of_div:
            tag_h4 = div.find_all("h4")
            for text in tag_h4:
                if "Language:" in text:
                    tag_anchor = div.find_all("a")
                    movie_language = [language.get_text()
                                        for language in tag_anchor]
                elif "Country:" in text:
                    tag_anchor = div.find_all("a")
                    movie_country = "".join(
                        [country.get_text() for country in tag_anchor])
        # return movie_language
        # return movie_country

        movie_time = soup.find("div", class_="subtext")
        run_time = movie_time.find("time").get_text().strip()
        run_time_hours = int(run_time[0])*60
        run_minuts = 0
        if 'min' in run_time:
            run_minuts = int(run_time[3:].strip("min"))
            movie_runtime = run_time_hours + run_minuts
        else:
            movie_runtime = run_time_hours
        # # return movie_runtime

        movies_data_scrape["name"] = movie_name[0]
        movies_data_scrape["director"] = director_name
        movies_data_scrape["country"] = movie_country
        movies_data_scrape["language"] = movie_language
        movies_data_scrape["poster_image_url"] = movie_poster
        movies_data_scrape["bio"] = (movies_bio)
        movies_data_scrape["runtime"] = movie_runtime
        movies_data_scrape["genre"] = movie_gener
        movies_data_scrape["cast"] = cast
        with open(file_name,"w") as data:
            data.write(json.dumps(movies_data_scrape))
        return movies_data_scrape


# url = scrept[0]['url']
# print url
# movie_top_list=scrape_top_list(url) 
# print movie_top_list


# Task-5
def get_movie_list_details(movies_list):
    random_sleep=random.randint(1,3)
    # print (random_sleep)
    time.sleep(random_sleep)
    movie_10_list = []
    for i in scrept[:250]:
        url = i['url']
        movieDetails = scrape_top_list(url)
        # print (movieDetails)
        movie_10_list.append(movieDetails)
    return movie_10_list

storage = get_movie_list_details(scrept)
# pprint(storage)

# Task -14

# def analyse_co_actors(movies_list):
#     return movies_list
# pprint(analyse_co_actors(storage))
# pprint(storage())
#This function returns a dictionary with list of frequent_co actors with which lead actor of every movie has woked with
def analyseCoActors(movies):
    moviesW = movies[0:250]
    dicById = {}
    for i in moviesW:   #Iterating loop over all movies
        cast = i['cast']
        dicById[cast[0]['imdb_id']] = {'name' : cast[0]['name'],'frequent_co_actors' : []} #Creating a dictionary key for the lead actor

    for j in dicById:       #Iterating loop over the newly created dictionary
        for k in movies:    #Iterating loop over all movies
            for l in k:
                if(l == 'cast'):
                    index = 0
                    main = k[l][0]['imdb_id']
                    if(main == j):      #Checking if lead actor key matches
                        for cast in k[l][1:6]:    #Iterating loop over next five actors
                            count = 1
                            for idmatch in dicById[j]['frequent_co_actors']:
                                if(idmatch['id']==cast['imdb_id']):
                                    count+=idmatch['num_movies']    #Incrementing the count of the movies if actor already exist in the dictionary
                            n = {'id' : cast['imdb_id'], 'name' : cast['name'], 'num_movies' : count}      #Creating a new dictionary for every new co-actor
                            dicById[j]['frequent_co_actors'].append(n)     #Appending the dictionary in frequent_co_actors list of the main dictionary
    return dicById
pprint(analyseCoActors(storage))

# Task - 15
def analyse_actors(movies_list):
    # print (movies_list)
    analyse_actors_dic={}
    for i in movies_list:
        cast_no = i['cast'] 
        for j in cast_no:
            imdb_id_no=j['imdb_id']
            imdb_name=j['name']
            if imdb_id_no in analyse_actors_dic:
                dic['num_movies'] +=1
            else:
                analyse_actors_dic[imdb_id_no]={}
                dic=analyse_actors_dic[imdb_id_no]
                dic['name']=imdb_name
                dic['num_movies'] = 1
    return analyse_actors_dic
analyse_actors_name=analyse_actors(storage) 
# pprint(analyse_actors_name)

# task-6


def analyse_movies_language(movies_language_list):
    movie_language_details = {}

    for movie_name in movies_language_list:

        if movie_name not in movie_language_details:

            movie_language_details[movie_name] = 1
        else:
            movie_language_details[movie_name] += 1

    return movie_language_details


movie_languages = []
for storage_language in storage:
    languages = storage_language["language"]
    # print languages
    movie_languages.extend(languages)
# print movie_languages
movies_language_count = analyse_movies_language(movie_languages)
# print movies_language_count

# #Task 7


def analyse_movies_director(movies_director_list):
    movie_director_details = {}

    for movie_director in movies_director_list:

        if movie_director not in movie_director_details:

            movie_director_details[movie_director] = 1
        else:
            movie_director_details[movie_director] += 1

    return movie_director_details


movie_director = []
for storage_director in storage:
    directors = storage_director["director"]
    movie_director.extend(directors)
# print movie_director
movies_director_count = analyse_movies_director(movie_director)
# print movies_director_count

# task 10

def analyse_language_and_directors(movie_list):
    detailDirector = {}
    for movie in movie_list:
        for dirtecor in movie['director']:
            detailDirector[dirtecor] ={}
    for movie in movie_list:
        for dirtecor in movie['director']:  
            for lang in movie['language']:
                if dirtecor in detailDirector:
                    detailDirector[dirtecor][lang] = 0
    for movie in movie_list:
       for dirtecor in movie['director']:  
            for lang in movie['language']:
                if dirtecor in  detailDirector:
                    detailDirector[dirtecor][lang] += 1                
    return  detailDirector 
# pprint(analyse_language_and_directors(storage))

# Task - 11
def analyse_movies_genre(movie_list):
    gerne_list = []
    for movie in movie_list:
        gerne = movie['genre'] 
        gerne_list .extend(gerne)
        gerne_dic = {}
        for data in gerne_list:
            if data not in  gerne_dic :
                gerne_dic [data] = 1
            else:
                gerne_dic [data] += 1 
    return  gerne_dic 
# pprint(analyse_movies_genre(storage))


# Task - 12

def  scrape_movie_cast(url):
    Id = url.split("/")
    file_name_id = Id[5]
    file_name = "Movies_cast/"+file_name_id+"_cast.json"
    filepath = Path(file_name)
    if filepath.exists():
        with open(file_name,'r') as json_data:
            data = json_data.read()
            data2 = json.loads(data)
            # print ("exist")
        return data2
    else:
        # print ("file not exsits")
        page=requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")
        table=soup.find('table',class_="cast_list")
        trs=table.find_all('tr')
        cast=[]
        for tr in trs:
            # print (tr)
            tds=tr.find_all('td',class_='')
            new={}
            for act in tds:
                a=act.find('a')
                name = (a.get_text())
                imdb_id = (a['href'])[6:15]
                new['imdb_id']=imdb_id
                new['name']=name
                cast.append(new)
        with open(file_name,"w") as data:
            data.write(json.dumps(cast))
        return(cast)
for i in scrept[:250]:
    url = i['url']
    cast_movies_url = scrape_movie_cast(url)
    # pprint(cast_movies_url)


# Task - Bonus Task -1

def scrape_movie_details(url):
    page=requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    # print (soup)
    div=soup.find('div',class_="rec_page")
    # print(div)
    movie_class=div.findAll('div',class_='rec_item')
    more_like={}
    for i in movie_class:
        movie_link=i.a["href"].split('/')
        movie_id=movie_link[2]
        movie_name=i.img['title']
        # print (movie_name)
        more_like['movie_id']=movie_id
        more_like['movie_name']=movie_name
        # print (more_like)
    # print("*****************************************")
for url in scrept:
    url = scrept[5]['url']
    # print (url)
    movie_top_list=scrape_movie_details(url) 
# print movie_top_list
