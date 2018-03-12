##http://www.billboard.com/charts/hot-100/
import bs4, re, os, csv
import urllib.request
import pandas as pd

##SET EMPTY OBJECTS
years_range = []
target_weeks = []
songs = []
artists = []

df = pd.DataFrame()

##SET RUN PARAMETERS
remove = ['STONE', 'STORM', 'STORY', 'SEVEN', 'RIVER', 'QUEEN', 'KING', 'CHINA', 'LOVE', 'ROCK', 'BABY', 'RAIN', 'HEAVEN', 'ANGEL', 'AMERICA', 'DREAM', 'LONG', 'WILL', 'SUMMER', 'MISS', 'EVER', 'GUY', 'STAR', 'SKY', 'SAID', 'MY', 'WINTER', 'DREAM', 'PARADISE', 'DOCK', 'CLOVER', 'FAITH', 'CHANCE', 'DESIRE', 'MIRACLE']
add = ['DR', 'MRS', 'MISS', 'MR', 'MISTER', 'MISTRESS', 'MASTER', 'DOCTOR']
StartYear = 1990
EndYear = 1991
dir_path = "C:/Python 3.6/Python/Git Personas/DanWhalen/Billboard_Hot_100/names"
threshold = 100

##DEFINE CUSTOM FUNCTIONS
def get_names(threshold=100, remove_list=remove, add_list=add):
    global human_names
    human_names = []
    song_titles = []
    for file in os.listdir(dir_path):
        if file.endswith(".txt"):
            yob = os.path.join(dir_path, file)
            with open(yob) as current_yob:
                for line in current_yob:
                    if int(line.split(",")[2]) >= threshold:
                        human_names.append(line.split(",")[0].upper())
    human_names = list(set(human_names))
    for a in add:
        human_names.append(a.upper())
    human_names = [n for n in human_names if n not in remove]
    human_names.sort()
    return(human_names)

def get_years(StartYear = 1958, EndYear = 2017):
    for year in range(StartYear,(EndYear+1)):
        years_range.append(year)
    return(years_range)

def get_weeks():
    for year in years_range:
        yr_url = urllib.request.urlopen("http://www.billboard.com/archive/charts/"+str(year)+"/hot-100").read()
        year_html = bs4.BeautifulSoup(yr_url, 'lxml')
        for link in year_html.find_all('a'):
            if link.get('href')[16:20] == str(year):
                week = str(year)+ "-" + str(link.get('href')[21:26])
                if len(week) == 10:
                    target_weeks.append(week)
    return(target_weeks)

def get_songs(w):
    global main_df
    wk_url = urllib.request.urlopen("http://www.billboard.com/charts/hot-100/"+w).read()
    week_html = bs4.BeautifulSoup(wk_url, 'lxml')
    for s in week_html.find_all('h2', {'class' :'chart-row__song'}):
        songs.append(s.text)
    for a in week_html.find_all(['a', 'span'], {'class' :'chart-row__artist'}):
        artists.append(a.text)
        artists_ = [i.strip() for i in artists]

    if len(artists_) == len(songs):
        main_df = pd.DataFrame({'DATE':str(w), 'SONG':songs, 'ARTIST':artists_})
        main_df = main_df[['DATE','ARTIST','SONG']]
        return(main_df)
    else:
        print('Error in week ' + str(w))
        print(str(len(artists_)) + " Artists")
        print(str(len(songs)) + " Songs")
        print("")
        pass

def check_song_titles(data):
    global detected_name
    global last_item
    detected_name = []
    last_item = []
    df_song_titles = data['SONG'].tolist()
    for song in df_song_titles:
        #remove "appostrophe s"
        a = song.replace("'s","")
        #replace elipses with a space
        b = a.replace("..."," ")
        #strip out extraneous punctuation
        c = re.sub(r"\!|\+|\(|\)|\,|\"|\?|\.|\$|\&|\"|", r"", b)
        #caps lock
        d = c.upper()
        #ignore fwd slash
        title_as_list = []
        title_as_list = re.split(r'\s|/|-',d.strip())
        detected_name.append(title_as_list)

    for dn in detected_name:
        col = []
        for ldn in dn:
            if ldn in human_names:
                col.append(ldn)
        dn.append(col)

    for l in detected_name:
        last_item.append(str(l[-1]))
        


##GET, SCRAPE, FORMAT, OUTFILE
get_names(threshold, remove, add)
get_years(StartYear,EndYear)
get_weeks()
for w in target_weeks:
    print("adding "+str(w))
    get_songs(w)
    df = pd.concat([df,main_df])
    dataframe = df.drop_duplicates(['SONG','ARTIST'], keep='first')
check_song_titles(dataframe)
last_item = pd.Series(last_item)
dataframe['NAME_SUSPECTED'] = last_item.values
dataframe.to_csv(('Billboard Hot 100 ['+str(target_weeks[0])+' -- '+str(target_weeks[-1])+', t='+ str(threshold)+'].csv'),index=False)

##_______________________________________________
##PICKLE I/O
##import pickle
##
##file_to_pickle = dataframe
##
##pickle_out = open('C:/Python 3.6/Python/Git Personas/DanWhalen/Billboard_Hot_100/df.pickle', 'wb')
##pickle.dump(file_to_pickle, pickle_out)
##pickle_out.close()
##pickle_in = open('df.pickle', 'rb')
##df = pickle.load(pickle_in)
