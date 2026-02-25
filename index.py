import json
import datetime
import random
from textblob import TextBlob
import re
import os
from geotext import geotext
from bardapi import Bard
import customtkinter
import emoji
import urllib.request
from tkcalendar import Calendar
import geocoder
from geopy.geocoders import Nominatim
from text2emotion import get_emotion
from googletrans import Translator
import requests
import pyowm
from PIL import Image
import io
from datetime import timedelta
import pandas as pd
import pycountry
from sklearn.metrics import f1_score, precision_score, recall_score
def read_json_files(file_names):
  """Reads JSON files and returns a list of dictionaries."""
  ##data = []
  for file_name in file_names:
    with open(file_name, "r") as f:
      data=(json.load(f))
  return data


def analyse_hashtag(hashtags):
  sentiment_scor=[]
  for hash in hashtags:
    blob= TextBlob(hash)
    sentiment_scor.append((hash, blob.sentiment.polarity))
  return sentiment_scor
##parsed_json = json.loads(file_content)

def analuse_post(post):
  blob=TextBlob(post)
  sentiment_scor= blob.sentiment.polarity
  return sentiment_scor

def getuserpost(id):
  posts=[]
  with open('posts.json') as post_file:
      file_content=(json.load(post_file))
  for file in file_content:
    if(file['postownerid'] == id):
      posts.append(file)
  return posts    

def extarct_hashtag(text):
  hashtag= re.findall(r'\#\w+', text)
  return hashtag



def detect_places(hashtag):
  places=[]
  explaces=["dubai", "algerie", "oran"]
  for hash in hashtag:
    for ex in explaces:
      if (hash == "#"+ex ):
        places.append(ex)
        break
  return places


def extarct_hashtag(text):
  hashtag= re.findall(r'\#\w+', text)
  return hashtag

def getfinellist(posts):
 finalposts=[]
 for pst in posts:
    hashtags= extarct_hashtag(pst['post_content'])
    finalposts.append({"date": pst['date'], "post_content": pst['post_content'], "comment_count": pst['comment_count'], "likes_count": pst['likes_count'], "hashtags": hashtags})
 return finalposts   






def get_season(d):
  seasons = {
    'winter': ((d.replace(month=12, day=21), d.replace(month=12, day=31))),
    'spring': ((d.replace(month=3, day=21), d.replace(month=6, day=20))),
    'summer': ((d.replace(month=6, day=21), d.replace(month=9, day=22))),
    'autumn': ((d.replace(month=9, day=23), d.replace(month=12, day=20))),
    'winter': ((d.replace(month=1, day=1), d.replace(month=3, day=20)))
  }
  for season, (start, end) in seasons.items():
    if start <= d <= end:
      return season
  return None









## localisation
def localisastion(city):
   local_data=[]
   g = geocoder.ip('me')
   latitude, longitude = g.latlng
   geolocator = Nominatim(user_agent="my_app")
   geolocator.headers['Accept-Language'] = 'fr-FR' 
   location = geolocator.reverse(f"{latitude}, {longitude}")
   place_name = None
   country= None
   if 'address' in location.raw:
     if 'state' in location.raw['address']:
       place_name = location.raw['address']['state']
     if 'country' in location.raw['address']:
        country = location.raw['address']['country']  
   api_key= 'e445aa766780ac11cd6408b6cf77761f'
   #city="Alger"
   url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
   #f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}&units=metric"
   response = requests.get(url)
   if response.status_code==404:
     print("error")
   else:
    data = response.json()
    temperature = data['main']['temp']
    weather_description = data['weather'][0]['description']
    print(weather_description)
    icon= data['weather'][0]['icon']
    local_data.append({"localisation": place_name, "temp": temperature, "icon": icon, "dis": weather_description})
   #print(f"latitude: {latitude} longitude: {longitude} \n name: {place_name} \n weather: {data}")
   return local_data


class Home(customtkinter.CTkScrollableFrame):
  def __init__(self, master, command=None, **kwargs):
    super().__init__(master, **kwargs)
    self.grid_columnconfigure(2, weight=1)

    self.command= command
    self.lable_list=[]

  def add_item(self, item, item_post):
    frame = customtkinter.CTkFrame(self, corner_radius=10)
    frame.pack(fill="x", padx=30,pady=(5, 20), expand= True)
    f_date= customtkinter.CTkFrame(frame, fg_color="transparent", corner_radius=10)
    f_date.pack(fill="x", expand=True, padx=10)
    f_post= customtkinter.CTkFrame(frame, fg_color="transparent", corner_radius=10)
    f_post.pack(fill="x", expand=True, padx=10)
    lable = customtkinter.CTkLabel(f_date, text=f"date: {item}" ,compound="center", padx=5, corner_radius=10)
    lable.grid(row=len(self.lable_list), column=1, pady=10, padx=20, sticky="w")
    lable_post = customtkinter.CTkLabel(f_post, text=f"post: {item_post}" ,compound="center", padx=5, corner_radius=10)
    lable_post.grid(row=len(self.lable_list), column=1, pady=10, padx=20, sticky="w")
    #lable_hashtag = customtkinter.CTkLabel(f_post, text=f"hashtag: {hastags}" ,compound="center", padx=5, corner_radius=10)
    #lable_hashtag.grid(row=len(self.lable_list), column=1, pady=20, padx=10, sticky="w")
    self.lable_list.append({lable, lable_post})



class Yelp(customtkinter.CTkScrollableFrame):
  def __init__(self, master, command=None, **kwargs):
    super().__init__(master, **kwargs)
    self.grid_columnconfigure(2, weight=1)

    self.command= command
    self.lable_list=[]

  def add_item(self, name, stars, address):
    frame = customtkinter.CTkFrame(self, corner_radius=10)
    frame.pack(fill="x", padx=30,pady=(5, 20), expand= True)
    f_date= customtkinter.CTkFrame(frame, fg_color="transparent", corner_radius=10)
    f_date.pack(fill="x", expand=True, padx=10)
    f_post= customtkinter.CTkFrame(frame, fg_color="transparent", corner_radius=10)
    f_post.pack(fill="x", expand=True, padx=10)
    lable = customtkinter.CTkLabel(f_date, text=f"nom: {name}" ,compound="center", padx=5, corner_radius=10)
    lable.grid(row=len(self.lable_list), column=1, pady=10, padx=20, sticky="w")
    lable_post = customtkinter.CTkLabel(f_post, text=f"address: {address}" ,compound="center", padx=5, corner_radius=10)
    lable_post.grid(row=len(self.lable_list), column=1, pady=10, padx=20, sticky="w")
    lable_stars = customtkinter.CTkLabel(f_post, text=f"stars: {stars}" ,compound="center", padx=5, corner_radius=10)
    lable_stars.grid(row=len(self.lable_list), column=1, pady=10, padx=20, sticky="w")
    #lable_hashtag = customtkinter.CTkLabel(f_post, text=f"hashtag: {hastags}" ,compound="center", padx=5, corner_radius=10)
    #lable_hashtag.grid(row=len(self.lable_list), column=1, pady=20, padx=10, sticky="w")
    self.lable_list.append({lable, lable_post, lable_stars})
       


class Sideleftbar(customtkinter.CTkFrame):
   def __init__(self, master, command=None, **kwarg):
      super().__init__(master, **kwarg)
      self.grid_columnconfigure(4, weight=1)
      self.command= command
      self.lable_list=[]
   def show(self, icon, text):
      frame = customtkinter.CTkFrame(self, corner_radius=10)
      frame.pack(fill="x", padx=30,pady=(5, 20), expand= True, side="top")
      f_date= customtkinter.CTkFrame(frame, fg_color="transparent", corner_radius=10)
      f_date.pack(fill="x", expand=True, padx=7)
      image_icon= customtkinter.CTkImage(Image.open(io.BytesIO(icon)))
      lable= customtkinter.CTkLabel(f_date, image=image_icon, text=text)
      lable.grid(row=len(self.lable_list), column=1, pady=10, padx=20, sticky="w")
      self.lable_list.append(lable)

   def add_item(self, item):
      frame = customtkinter.CTkFrame(self, corner_radius=10)
      frame.pack(fill="x", padx=30,pady=(5, 20), expand= True, side="top")
      f_date= customtkinter.CTkFrame(frame, fg_color="transparent", corner_radius=10)
      f_date.pack(fill="x", expand=True, padx=7)
      lable = customtkinter.CTkLabel(f_date, text=item ,compound="center", padx=5)
      lable.grid(row=len(self.lable_list), column=1, pady=10, padx=20, sticky="w")
      self.lable_list.append(lable)

   


datay =[]
with open('yelp dataset/yelp_academic_dataset_business.json', 'r', encoding='utf-8') as file:
    for line in file:
        datay.append(json.loads(line))


data2=[]
class App(customtkinter.CTk):

  def __init__(self, input_user, input_cats):
    super().__init__()

    self.title("test")
    self.geometry("1100x450")

    # set grid layout 1x2
    self.grid_rowconfigure(0, weight=1)
    self.grid_columnconfigure(3, weight=1)
    chemnin = input_user
    cats= catsv_list=[x.strip() for x in input_cats.split(";")]
    print(cats)
    fichiers = os.listdir(chemnin)
    list_data=[]
    pref_set= set(cats)
    post=[]
    data3=[]
    dataA=[]
    categoriesH = ["Outdoor activities", "walk or hike in nature", "travel", "parks", "museums", "restaurant", "relaxation", "Beauty & Spas", "hobbies", "theater performances", "live events", "attending concerts","animal shelters or parks", "celebrations", "recreational activities", "sports", "botanical gardens", "Traditional Chinese Medicine" ,"cofee", "Bookkeepers"]
    categoriesS = ["shopping", "sea", "Self-Care Rituals", "Spending Time with Pets", "yoga or Physical activity", "Reading in library", "Listening to Music", "Nature Walks or Parks", "fashion", "Restaurent", "Bookkeepers"]
    categoriesA = ["rest areas", "stores", "Physical activity gym", "mountains", "nature", "yoga", "Traditional Chinese Medicine", "food", "Bookkeepers"]
    
    date= datetime.datetime.now()
    final_file_name=""
    comptes_sentiments = {"heureux": 0, "normal": 0, "triste": 0}
    date_n= datetime.datetime.now().strftime("%H:%M:%S")
    excel_file= 'last caption.xlsx'
    df= pd.read_excel(excel_file)
    table= df[['users', 'address', 'city', 'state', 'Country']]
    t=table[table["users"]== input_user]
    if t['city'].empty:
      print("no citi")
    else:
      print(t['city'])
    
    for fichier in fichiers:
      if fichier.endswith(".json"):
          chemin_fichier= os.path.join(chemnin, fichier)
          file_name= os.path.splitext(fichier)[0]
          final_file_name = file_name.replace("_", " ")
          date_format= "%Y-%m-%d %H-%M-%S %Z"
          date= datetime.datetime.strptime(final_file_name, date_format)
          with open(chemin_fichier, "r", encoding='utf-8') as f:
            contenu = json.load(f)
            list_data.append({"nom": date, "content":contenu})
    for content in list_data:
      data= content["content"]
      text_location = data["node"]["edge_media_to_caption"]["edges"]
      comment_location= data["node"]["edge_media_to_comment"]
      likes_location = data["node"]["edge_media_preview_like"]
      #time= content["nom"].strftime("%H:%M:%S")
      #time_x= datetime.datetime.strptime(date_n, "%H:%M:%S")- datetime.datetime.strptime(time, "%H:%M:%S")
      #time_def= time_x.total_seconds()/3600
      #print(time_def)
      #date_obj= datetime.datetime.strptime(content['nom'], "%Y-%m-%d %H:%M:%S")
      dif_date= abs(date - content['nom'])
      limit= timedelta(hours=4)
      if dif_date <= limit:
        print("ok")
      else:
        print("no")  
      if len(text_location)>0:
        txt= emoji.demojize(text_location[0]["node"]["text"])
        #text= f"translate {text_location[0]["node"]["text"]} in elnglish"
        #os.environ['_BARD_API_KEY']="cwimMFisbVFOtl9b7PAZX2YIbA7DZnzUvSHpabFQhDM0BWNxr59T8Oe7ZOTHdFFBvXl5Qg."
        #txt_fr = Translator().translate(txt, dest='en')
        if dif_date <= limit:
          blob = TextBlob(txt)
          for sentec in blob.sentences:
            for word, tag in sentec.tags:
              if tag == 'GPE':
                  print(word)
          if blob.sentiment.polarity > 0:
            comptes_sentiments["heureux"]+=1
          elif blob.sentiment.polarity < 0:
            comptes_sentiments["triste"]+=1
          else:
            comptes_sentiments["normal"]+=1
        else:
          comptes_sentiments["normal"]+=1   
        post.append({"date" : content["nom"], "post_content" : text_location[0]["node"]["text"], "comment_count" : comment_location["count"], "likes_count": likes_location["count"]})
      else:
        post.append({"date" : content["nom"], "post_content" : "", "comment_count" : comment_location["count"], "likes_count": likes_location["count"]})
    finallist= getfinellist(post)

    list_triee=sorted(comptes_sentiments.items(), key=lambda x: x[1], reverse=True)
    local_weather= localisastion("alger")
    date_now= datetime.datetime.now().date()
    season= get_season(date_now)
    #cats_shos= re.findall(r'+\w\;', input_cats)
    #print(cats_shos)
    print(local_weather)
    print(season)
    print(list_triee[0][0])
    sentiment=0
    f1=0
    for p in post:
      print(p['date'])
    if list_triee[0][0] == "normal":
      cat_set= set(categoriesA)   
      pref_cat=[]
      for cat1 in categoriesA:
        if cat1 in pref_set:
          pref_cat.append(cat1)
      for d in datay:
        if d['categories'] is not None and d["is_open"] is not None and d["is_open"]==1:
          for cat in pref_cat:
            if cat in d["categories"]:
              data2.append(d)
    if list_triee[0][0] == "triste":
      cat_set= set(categoriesS)   
      pref_cat=[]
      for cat1 in categoriesS:
        if cat1 in pref_set:
          pref_cat.append(cat1)
      for d in datay:
        if d['categories'] is not None and d["is_open"] is not None and d["is_open"]==1:
          for cat in pref_cat:
            if cat in d["categories"]:
              data2.append(d)
    if list_triee[0][0] == "heureux":
      cat_set= set(categoriesH)  
      pref_cat=[]
      for cat1 in categoriesH:
        if cat1 in pref_set:
          pref_cat.append(cat1)
      for d in datay:
        if d['categories'] is not None:
          for cat in pref_cat:
            if cat in d["categories"]:
              data2.append(d)   
    #print(data2)
    #data_list = [json.loads(item) for item in data2]
    if t['city'].empty:
        print("no city")
    else:
        for d in data2:
          #print(d["name"])
          #print(d["categories"])
          #print(d["city"])
          if (t['city'] == d["city"]).all():
            #print("aqual")
            f1=f1+1
            data3.append(d)
          #else:
            #print("!=")  
    #print(data3)
    sorted_data3= sorted(data3, key=lambda x: x["stars"], reverse=True)
    cat_list=[]
    for d3 in data3:
      cat_list+= d3["categories"].split(", ")
    print(cat_list)
    precision = [x for x in cat_list if x in pref_set]
    f2=0
    f3=0
    for d9 in data3:
      for c in pref_set:
        if c in d9["categories"]:
          f2+=1   #set.intersection(set(cats), set(cat_list))
    print("f1 scor: ", f2) 
    for c9 in cat_list:
      for c8 in pref_set:
        if c9 == c8:
          f3+=1
    print("f12 ", f3)  
    # create navigation frame
    self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
    self.navigation_frame.grid(row=0, column=0, sticky="nsew")
    self.navigation_frame.grid_rowconfigure(4, weight=1)

    self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text=input_user,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
    self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

    self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                    anchor="w", command=self.home_button_event)
    self.home_button.grid(row=1, column=0, sticky="ew")


    self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Frame 2",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                       anchor="w", command=self.frame2_button_event)
    self.frame_2_button.grid(row=2, column=0, sticky="ew")

    self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event)



    local_data= localisastion("Alger")

    self.home_frame = Home(self, width=600, command=None, corner_radius=5, fg_color= "transparent")
    self.home_frame.grid(row=0, column=2, padx=20, pady=10, sticky="nsew")
    for pst in finallist:
       self.home_frame.add_item(pst["date"], pst["post_content"])
 
    #left side
    self.left_side= Sideleftbar(self, command=None, fg_color="transparent")
    self.left_side.grid(row=0, column=3, sticky="nsew")
    #self.left_side.add_item(f"meteo: {local_weather}")
    #self.left_side.add_item(f"localisation: {t['city'][1]}")
    self.left_side.add_item(f"temperature{local_weather[0]["temp"]}")
    #image_icon= f"http://openweathermap.org/img/wn/{local_weather[0]["icon"]}.png"
    #resp= requests.get(image_icon)
    #icon= resp.content
    #self.left_side.show(icon, local_weather[0]["temp"])


    # create second frame
    self.second_frame = customtkinter.CTkScrollableFrame(self, width=600, corner_radius=0, fg_color="transparent")
    for c in cats:
      self.label_cat= customtkinter.CTkLabel(self.second_frame, text=f"{c}")
      self.label_cat.pack()
      for i in sorted_data3:
        if c in i["categories"]:
          self.lbl_frame = customtkinter.CTkFrame(self.second_frame, fg_color="gray25", width=600, corner_radius=10)
          self.lbl_frame.pack(fill="x", padx=30,pady=(5, 20), expand= True)
          self.second_frame_large_image_label = customtkinter.CTkLabel(self.lbl_frame, width=500, text= f"nom: {i["name"]}")
          self.second_frame_large_image_label.pack()
          self.second_frame_stars_label = customtkinter.CTkLabel(self.lbl_frame, width=500, text=f"note: {i["stars"]}")
          self.second_frame_stars_label.pack()
          self.second_frame_address_label = customtkinter.CTkLabel(self.lbl_frame, width=500, text=f"address: {i["address"]}")
          self.second_frame_address_label.pack()

    # create third frame
    self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
    self.third_frame_large_image_label = customtkinter.CTkLabel(self.third_frame, text="3")
    self.third_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)

    # select default frame
    self.select_frame_by_name("home")

  def select_frame_by_name(self, name):
    # set button color for selected button
    self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
    self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
    self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")
    if name == "home":
      self.home_frame.grid(row=0, column=1, sticky="nsew")
    else:
        self.home_frame.grid_forget()
    if name == "frame_2":
        self.second_frame.grid(row= 0, column=1, sticky="nsew")
    else:
        self.second_frame.grid_forget()


  def home_button_event(self):
        self.select_frame_by_name("home")

  def frame2_button_event(self):
        self.select_frame_by_name("frame_2")




  def change_appearance_mode_event(self, new_appearance_mode):
      customtkinter.set_appearance_mode(new_appearance_mode)                 






class Login(customtkinter.CTk):
  def __init__(self):
    super().__init__()
    self.title("test")
    self.geometry("1100x450")
    self.lable_user = customtkinter.CTkLabel(self, text="Nom utilisateur")
    self.lable_user.pack()
    self.input_user= customtkinter.CTkEntry(self)
    self.input_user.pack(pady=10)
    self.lable_cats = customtkinter.CTkLabel(self, text="les preferences (ex: shopping; food; yoga)")
    self.lable_cats.pack()
    self.input_cats = customtkinter.CTkEntry(self)
    self.input_cats.pack(pady=10)
    self.login_button = customtkinter.CTkButton(self, text="log in", command=self.loginbtn)
    self.login_button.pack()
    
  def loginbtn(self):
    global chemnin
    value_input= self.input_user.get()
    cats_value= self.input_cats.get()
    #chemnin= self.input_user.get()
    new_window= App(input_user= value_input, input_cats=cats_value)
    new_window.mainloop()
    self.destroy()



if __name__=="__main__":
  # -*- coding: utf-8 -*-
  customtkinter.set_appearance_mode("system")
  app= Login()
  #app= App()
  app.mainloop()
  ##main()  