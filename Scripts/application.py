import logging
import yt_dlp
from googleapiclient.discovery import build
from pytube import YouTube
import streamlit as st
#url="https://www.youtube.com/watch?v=S6fjqe4chRM"
API_KEY = 'AIzaSyBIgjXBxYaWBgproZi0ZPZJtRMFg_7W2aw'
logging.basicConfig(filename='modularlog.log',level=logging.INFO,format='%(asctime)s  %(levelname)s  %(message)s)')
if 'page' not in st.session_state:
    st.session_state.page = 1

if 'user_input' not in st.session_state:
    st.session_state.user_input = ""
class Video_Info:
    def VideoInfo(self,url):
        """This function takes a URL and returns video information"""
        try:
            self.url=url
            self.video_details = self.get_video_details(self.url)
            logging.info('Video successfully retrieved')
            return self.video_details
        except Exception as e:
            self.e=e
            logging.error(self.e)
            return self.e
        
    def get_video_details(self,url):
        """This function takes a URL and returns video information to Video_Info()""" 
        self.url=url
        self.ydl_opts = {
                    'quiet': True,  # Suppress console output
                    'skip_download': True,  # Do not download the video
            }
        try :
                self.ydl =yt_dlp.YoutubeDL(self.ydl_opts)
                self.info_dict = self.ydl.extract_info(self.url, download=False)
                
                self.video_details = {
                    "Video_Title": self.info_dict.get("title"),
                    "Author ": self.info_dict.get("uploader"),
                    "Video_Views": self.info_dict.get("view_count"),
                    "Video_Likes": self.info_dict.get("like_count"),
                    "Video_Dislikes": self.info_dict.get("dislike_count"),
                    'Video_Comments': self.info_dict.get('comment_count', 0),
                    "Video thumbnail" : self.info_dict.get('thumbnail', "Channel image not available."),
                    "Video_Description": self.info_dict.get("description"),
                    "Video_Duration": self.info_dict.get("duration"),
                }
                logging.info("Video details function Executed successfully")
                return self.info_dict.get("uploader"),self.video_details
        except Exception as e:
            self.e=e
            logging.error(e)
            return self.e

    # Replace with your YouTube API key and video ID  
class subscribers_counts(Video_Info):
    """This Class represents the number of subscribers"""
    def subscribers_info(self, api_key,url):
        """This method takes api_key and url and returns subscribers count"""
        try:
            self.api_key = api_key
            self.url=url
            self.index=self.url.find('v=')
            self.video_id=self.url[self.index+2:]
            self.api_key = api_key
            st.write(f"VIDEO ID : {self.video_id}")
            self.channelid=self.get_channel_id(self.api_key,self.video_id)
            st.write(f'Channel ID : {self.channelid}')
            self.subscriber_count=self.get_subscriber_count(self.api_key,self.channelid)
            logging.info("Subscribers count executed successfully")
            return self.subscriber_count
        except Exception as e:
            self.e=e
            logging.error(self.e)
            return self.e
    def get_channel_id(self,api_key, video_id):
        """This method takes apikey and video_id and returns the channel id """
        try:
            self.api_key = api_key
            self.video_id = video_id
            self.youtube = build("youtube", "v3", developerKey=api_key)

            self.request = self.youtube.videos().list(
                part="snippet",
                id=self.video_id
            )
            self.response = self.request.execute()

            if "items" in self.response and len(self.response["items"]) > 0:
                self.snippet = self.response["items"][0]["snippet"]
                self.channel_id = self.snippet.get("channelId", "Channel ID not available")
                return self.channel_id
            else:
                return "Video not found or channel ID not available."
        except Exception as e:
            self.e=e
            logging.error(e)
            return e 
    def get_subscriber_count(self,api_key, channel_id):
        """This method returns the number of subscribers to subscribers_info() function"""
        try:
            self.api_key = api_key
            self.channelid=channel_id
            self.youtube = build("youtube", "v3", developerKey=self.api_key)

            self.request = self.youtube.channels().list(
                part="statistics",
                id=self.channel_id
            )
            self.response = self.request.execute()

            if "items" in self.response and len(self.response["items"]) > 0:
                self.statistics = self.response["items"][0]["statistics"]
                self.subscribers = self.statistics.get("subscriberCount", "Subscriber count not available")
                return self.subscribers
            else:
                return "Channel not found or subscriber count not available."
        except Exception as e:
            self.e=e
            logging.error(self.e)
            return e

# Replace with your YouTube API key and channel ID
class Channel_profile(subscribers_counts):
    
    def channel_profile_info(self,api_key, url):
        """This function takes api key and url and returns channel profile"""
        try:
            self.api_key = api_key
            self.url=url
            self.index=self.url.find('v=')
            self.video_id=self.url[self.index+2:]
            self.api_key = api_key
            self.channelid=self.get_channel_id(self.api_key,self.video_id)
            self.channel_proflepic(self.url,self.channelid,self.api_key)
            return ""
        except Exception as e:
            self.e=e
            logging.error(self.e)
            return self.e
    def channel_proflepic(self,url,channel_id,api_key):
        """This function takes channel id and api key and returns channel profile to channel_profile_info()"""
        self.api_key = api_key
        self.channel_id=channel_id
        self.url=url
        self.youtube = build("youtube", "v3", developerKey=self.api_key)
        self.channel_request = self.youtube.channels().list(
        part='snippet',
        id=self.channel_id
        )
        self.channel_response = self.channel_request.execute()
        try:
            if 'items' in self.channel_response:
                #Author name
                AuthorName=self.get_video_details(self.url)
                st.write(f"Channel Name : {AuthorName[0]}")
                #st.write(f"Author Name : {self.channel_response['items'][0]['snippet']['title']}")
                #channel description
                st.write("Channel Description :",self.channel_response['items'][0]['snippet']['description'].replace('\n', ' '))
                #Joined by date
                self.Joined_by=self.channel_response['items'][0]['snippet']['publishedAt']
                from datetime import datetime
                self.datetime_obj = datetime.strptime(self.Joined_by, '%Y-%m-%dT%H:%M:%SZ')
                st.write(f"Joined at  {self.datetime_obj}")
                #Author profile pic
                st.write(f"Channel profile pic : {self.channel_response['items'][0]['snippet']['thumbnails']['high']['url']}")
                #self.sub=self.get_subscriber_count(self.api_key, self.channel_id)
                #print(f"Total subscribers : {self.sub}")
                logging.info("Channel profile pic function Executed successfully")
                #self.channel_coverpic(channel_id)
            else:
                st.write("No channel information found in the response.")
                #logging.error("No channel information found in the response.")
        except Exception as e:
            self.e=e
            logging.error(self.e)
class Channel_coverpic(Channel_profile):
    """This class represents a channel cover pic"""
    def channel_coverpic_info(self,api_key, url):
        """This method takes api key and url and returns a channel cover pic"""
        try:
            
            self.api_key = api_key
            self.url=url
            self.index=self.url.find('v=')
            self.video_id=self.url[self.index+2:]
            self.api_key = api_key
            self.channelid=self.get_channel_id(self.api_key,self.video_id)
            self.channel_coverpic(self.channelid,self.api_key)
            return ""
        except Exception as e:
            self.e=e
            logging.error(self.e)
            return self.e
    def channel_coverpic(self,channel_id,api_key):
        """This method takes channel id and api key and returns a channelcover pic to the channel_cover_pic_info() """ 
        self.channel_id=channel_id
        self.api_key=api_key
        self.youtube = build("youtube", "v3", developerKey=self.api_key)
        self.channel_request = self.youtube.channels().list(
            part='brandingSettings',
            id=self.channel_id
        )
        self.channel_response_1 = self.channel_request.execute()
        try:
            #Author Country
            st.write(f"Country : {self.channel_response_1['items'][0]['brandingSettings']['channel']['country']}")
            #Channel coverpic
            st.write(f"Channel cover pic : {self.channel_response_1['items'][0]['brandingSettings']['image']['bannerExternalUrl']}")
            #Channel keywords
            st.write(f"Channel keywords : {self.channel_response_1['items'][0]['brandingSettings']['channel']['keywords']}")
            logging.info("Channel coverpic function executed successfully")
        except Exception as e:
            self.e=e
            logging.error(self.e)
class Playlists(Channel_coverpic):
    """This class represents a Playlists information"""
    def Playlist_info(self,api_key,url):
        """This function takes api_key and url and returns Playlist info"""
        self.api_key = api_key
        self.url=url
        self.index=self.url.find('v=')
        self.video_id=self.url[self.index+2:]
        self.api_key = api_key
        self.channel_id=self.get_channel_id(self.api_key,self.video_id)
        try:
            self.youtube = build("youtube", "v3", developerKey=self.api_key)
            self.playlists = self.get_all_channel_playlists(self.api_key,self.channel_id)
            if self.playlists:
                st.write("Playlist Names and Video Counts:  Url : ")
                for self.playlist in self.playlists:
                    self.playlist_name = self.playlist['snippet']['title']
                    self.playlist_id = self.playlist['id']
                    self.video_count = self.get_playlist_video_count(self.youtube, self.playlist_id)
                    self.playlist_url = f"https://www.youtube.com/playlist?list={self.playlist_id}"
                    st.write(f"{self.playlist_name} - Videos: {self.video_count}- Url: {self.playlist_url}")
            logging.info('Playlists function Executed successfully')
            return ""
        except Exception as e:
            self.e=e
            logging.error(self.e)
            return self.e
    def get_all_channel_playlists(self,api_key,channel_id):
        self.api_key = api_key
        self.channel_id = channel_id
        self.youtube = build("youtube", "v3", developerKey=self.api_key)
        self.playlists = []
        self.next_page_token = None
        try:
                while True:
                    self.playlists_request = self.youtube.playlists().list(
                        part='snippet',
                        channelId=self.channel_id,
                        maxResults=50,  # Adjust as needed
                        pageToken=self.next_page_token
                    )
                    self.playlists_response = self.playlists_request.execute()

                    self.playlists.extend(self.playlists_response.get('items', []))
                    self.next_page_token = self.playlists_response.get('nextPageToken')

                    if not self.next_page_token:
                        break
                return self.playlists
        except Exception as e:
            self.e=e
            logging.error(self.e)
            return self.e
        

    def get_playlist_video_count(self,youtube, playlist_id):
        try:
            self.youtube=youtube
            self.playlist_id=playlist_id
            self.playlist_items_request = self.youtube.playlistItems().list(
                part='id',
                playlistId=self.playlist_id
            )
            self.playlist_items_response = self.playlist_items_request.execute()
            self.video_count = len(self.playlist_items_response.get('items', []))
            return self.video_count
        except Exception as e:
            self.e=e
            logging.error(self.e)
            return self.e

class Video_Full__Info(Playlists):
    def __init__(self,api_key,url):
        self.api_key = api_key
        self.url = url
        print("------------------------Video_Info----------------------------")
        try:
            for self.key, self.value in self.VideoInfo(self.url)[1].items():
                st.write(f"{self.key}: {self.value}")
                pass 
        except Exception as e :
            self.e=e
            #print("Error :",video_url) 
            st.write(self.e)
            logging.error(self.e)
        
class Channel_Full_Info(Playlists): 
    def __init__(self,api_key,url):
        try:
            self.api_key = api_key
            self.url = url       
            self.channel_id=self.get_channel_id(self.api_key,self.url)
            print("------------------------Channel_Info----------------------------")
            #st.write(f"Channel id : {self.channel_id}")
            self.sub_count=self.subscribers_info(self.api_key,self.url)
            st.write(f"Total Subscribers : {self.sub_count}") 
            self.channel_pro_pic=self.channel_profile_info(self.api_key,self.url)
            #st.write(self.channel_pro_pic)
            st.write(self.channel_coverpic_info(self.api_key,self.url))
        except Exception as e:
            self.e=e
            logging.error(self.e)
            st.write(self.e)
            
                
class Playlist_full_info(Playlists):      
    def __init__(self,api_key,url):
        try:
        
            self.api_key = api_key
            self.url = url      
            #print("------------------------PLAYLISTS----------------------------")
            st.write(self.Playlist_info(self.api_key,self.url))
            logging.info("All executed successfully")
        except Exception as e:
            self.e=e
            logging.error(self.e)
            print(self.e)

def page1():
    st.title("Youtube content scrapper ")
    
    # Input fields on the first page
    url = st.text_input("Paste the Youtube URL :")
    
    # Submit button to navigate to the second page
    if st.button("Submit"):
        st.session_state.page = 2  # Set the page to 2 for redirection
        st.session_state.url = url  # Store user input for page 2

# Page 2: Second Web Page
def page2():
    
    #st.write("VIDEO INFO.")
    st.write("YOUR URL:", st.session_state.url)
    #get_video_details(st.session_state.url)
    API_KEY = 'AIzaSyBIgjXBxYaWBgproZi0ZPZJtRMFg_7W2aw'
    try:
        B=Video_Full__Info(API_KEY,st.session_state.url)
        print(B)
    except Exception as e :
        #print("Error :",video_url)
        st.write("Given URL is invalid ,Kindly recheck Youtube URL of the video, and give valid url of youtube video")
        logging.error(e)
    if st.button("Channel INfo"):
        st.session_state.page = 3  # Set the page to 2 for redirection
        #st.session_state.url = url  # Store user input for page 2
    # Add content for the second page as needed
def page3():
    #st.write("You have successfully submitted the information.")
    #st.write("Entered Information (from Page 1):", st.session_state.user_input)
    API_KEY = 'AIzaSyBIgjXBxYaWBgproZi0ZPZJtRMFg_7W2aw'
    A=Channel_Full_Info(API_KEY,st.session_state.url)
    print(A)
    st.title("   ")
    st.title("Playlists info")
    C=Playlist_full_info(API_KEY,st.session_state.url)
    print(C)


# Initialize the 'page' attribute if it doesn't exist


def main():
    if st.session_state.page == 1:
        page1()
    elif st.session_state.page == 2:
        st.empty()  # Clear content of Page 1
        st.title("VIDEO DETAILS")
        page2()
    elif st.session_state.page == 3:
        st.empty()  # Clear content of Page 2
        st.title("Channel INfo")
        page3()

if __name__ == "__main__":
    main()
