import os
import re
import argparse
import pandas as pd
from bs4 import BeautifulSoup

def lyrics2csv(path, output):
    '''
    Extracts the pure lyrics from all htmls in path and returns a csv file with artist name, song title and lyric.
    The htmls have to be saved in a separate folder (path) with the following syntax 'Artist_Name-Song_Title.html' (example: 'Red_Hot_Chili_Peppers-Under_The_Bridge.html')
    output defines the name of the csv file.
    '''
    lyrics = []
    artists = []
    song_names = []
    for file in os.listdir(path):
        print(file)
        if file.endswith('html'):
            #print(file)
            with open(path + file, 'r') as f:
                lyric_html = f.read()
            if len(re.findall('no lyrics found', lyric_html)) > 0:
                print('no lyrics found in ' + file)
                continue
            soup = BeautifulSoup(lyric_html, 'html.parser')
            lyric_all = soup.find_all(name='pre', class_='lyric-body')
            text = lyric_all[0].get_text().lower()
            text = text.replace('\n', ' ')
            text = text.replace('''i'm''','i am')
            text = text.replace('''i'll''', 'i will')
            text = text.replace('''i've''', 'i have')
            text = text.replace('''i'd''', 'i would')
            text = text.replace('''you'll''', 'you will')
            text = text.replace('''you're''', 'you are')
            text = text.replace('''you've''', 'you have')
            text = text.replace('''they're''', 'they are')
            text = text.replace('''they'd''', 'they would')
            text = text.replace('''don't''', 'do not')
            text = text.replace('''it's''', 'it is')
            lyrics.append(text)
            artist = file[:list(file).index('-')]
            artists.append(artist)
            song_name = file[list(file).index('-')+1:-5]
            song_names.append(song_name)

    # Create a DataFrame 
    df_lyrics = pd.DataFrame({
        'artist' : artists,
        'song_name': song_names,
        'songtext' : lyrics
    })
    # Write the dataframe to .csv
    df_lyrics.to_csv(path + output, index=False)
    print('Created csv with some beautiful texts')    


# 1. initialize the parser
parser = argparse.ArgumentParser(description='extracts the text from all the htmls in the given folder')

# 2. define command line arguments
parser.add_argument('input', help='path to folder with htmls')
parser.add_argument('output', help='name of the csv output file (same location as htmls)')



# 3. read the arguments from the command line
args = parser.parse_args()

lyrics2csv(args.input, args.output)