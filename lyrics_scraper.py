import pandas as pd
import re
import requests
import random
import time
import argparse


def find_link2lyrics(artistname, html):
    '''
    find all lyric links in the html code,
    Artistname: string with spaces (like 'Red Hot Chilli Peppers')
    returns a list with all absolute links
    '''
    artistname = '\+'.join(artistname.split())
    song_link = re.findall('<a href="(/lyric/\d+/' + artistname + '/[\w+\+]+)">', html)
    return song_link

def find_song_names(artistname, html):
    '''
    finds all song names in the html code
    Artistname: string with spaces (like 'Red Hot Chilli Peppers')
    returns a list with all song names in the order of the lyric links
    '''
    artistname = '\+'.join(artistname.split())
    song_title = re.findall('<a href="/lyric/\d+/' + artistname + '/[\w+\+]+">([\w+\s]+)', html)
    return song_title

def scrape_lyrics(artistname, header, list_links, list_names, path):
    '''
    checks songs for duplicates
    saves the html code of every song lyrics in a local directory (path)
    '''
    df_songs = pd.DataFrame({
    'names': list_names,
    'links': list_links    
    })
    print('found ' + str(df_songs.shape[0]) + 'songs')
    df_songs = df_songs.drop_duplicates('names', ignore_index=True)
    print('found ' + str(df_songs.shape[0]) + 'songs after removing duplictes')

    #for i,(title,link) in enumerate(zip(song_title, song_link)):
    for index, row in df_songs.iterrows():
        url = row[1]
        r = requests.get(url, headers=header)
        artistname = '_'.join(artistname.split())
        with open(path + artistname + '-' + row[0].replace(' ', '_') + '.html', mode='w') as file:
            file.write(r.text)
        print('(' + str(index+1) + '/' + str(df_songs.shape[0]) + ')... saving ' + row[0] + '......')
        time.sleep(random.random())


# 1. initialize the parser
parser = argparse.ArgumentParser(description='saves all lyrics of one artist from www.lyrics.com as html')

# 2. define command line arguments
parser.add_argument('artist', help='name of the artist')
parser.add_argument('url', help='url of artist page at www.lyrics.com')
parser.add_argument('output', help='path to folder where to store the html files')


# 3. read the arguments from the command line
args = parser.parse_args()

url = args.url
artist_name = args.artist

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}

# send request
r = requests.get(url, headers=headers)

links = find_link2lyrics(artist_name, r.text)
links = ['https://www.lyrics.com' + link for link in links]
#print(links)
names = find_song_names(artist_name, r.text)
#print(names)
scrape_lyrics(artist_name, headers, links, names, args.output)
