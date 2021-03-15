import os
import pickle

import google_auth_oauthlib.flow
from google.auth.transport.requests import Request
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

from random import randint
import webbrowser

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret.json"
    
    # load in credentials from a pickle file if it exists
    credentials = get_credentials(client_secrets_file)
    
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)
        
    # supply a channel ID and get the url of a random video in its "uploads" playlist
    vid_url = get_random_video_from_channel("UCHZqZf6nbTu3hnRtOJwUtkA", youtube) # Kara
    webbrowser.open(vid_url)

def get_credentials(file):
    """gets the credentials using an external json client secrets file"""
    credentials = None
    
    if os.path.exists("token.pickle"):
        print("Loading credentials from file...")
        with open("token.pickle", "rb") as token:
            credentials = pickle.load(token)

    # if there are no valid credentials saved then either refresh the token or log in
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            print("Refreshing access token...")
            credentials.refresh(Request())
        else:
            print("Fetching new tokens...")
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                client_secrets_file,
                scopes
            )
            
            flow.run_local_server(port=8080, prompt="consent")
            credentials = flow.credentials
            
            with open("token.pickle", "wb") as f:
                print("Saving credentials for future use...")
                pickle.dump(credentials, f)
                
    return credentials
    
def get_random_video_from_channel(channel_id, youtube):
    # getting the channel information; we need the id of the uploads playlist
    channel_request = youtube.channels().list(
        part="contentDetails,statistics",
        id=channel_id
    )
    channel_response = channel_request.execute()
    
    # playlist id to look up when getting the list of videos
    upload_playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    
    # need to generate a random number between 1 and videoCount, then we know we only need to page up to that point
    max_vids = int(channel_response['items'][0]['statistics']['videoCount'])
    
    # there is a limit in the youtube api that prevents new pages being return after 500 results, so putting
    # the cap here to prevent any errors that may arise from trying to access things we're not allowed
    if max_vids > 500:
        max_vids = 500
    
    # don't request so many items if we don't need to (50 is the max per page allowed)
    if max_vids >= 50:
        num_vids_to_pull = 50
    else:
        num_vids_to_pull = max_vids
    
    rand_vid_num = randint(1, max_vids)
    
    print("channel_id: " + channel_id)
    print("number of videos: " + str(max_vids))
    print("chosen video number: " + str(rand_vid_num))
    
    all_vid_links = []
    
    # get the first up to 50 videos since we don't need a pageToken
    playlist_request = youtube.playlistItems().list(
        part="contentDetails",
        playlistId=upload_playlist_id,
        maxResults=num_vids_to_pull
    )
    
    playlist_response = playlist_request.execute()
    
    for item in playlist_response['items']:
        vid_id = item['contentDetails']['videoId']
        vid_link = f"https://youtu.be/{vid_id}"
        all_vid_links.append(vid_link)
    
    # if there are more than 50 videos and the chosen video is not in the first 50, we need more pages of results
    if (max_vids > num_vids_to_pull) & (rand_vid_num > num_vids_to_pull):
        i = num_vids_to_pull
        
        while i < rand_vid_num:
            next_page = playlist_response['nextPageToken']
        
            playlist_request = youtube.playlistItems().list(
                part="contentDetails",
                playlistId=upload_playlist_id,
                maxResults=num_vids_to_pull,
                pageToken=next_page
            )
            
            playlist_response = playlist_request.execute()
            
            for item in playlist_response['items']:
                vid_id = item['contentDetails']['videoId']
                vid_link = f"https://youtu.be/{vid_id}"
                all_vid_links.append(vid_link)
            
            i += num_vids_to_pull
    
    return(all_vid_links[rand_vid_num + 1])
    
    # i = 1
    # for item in playlist_response['items']:
        # vid_id = item['contentDetails']['videoId']
        # vid_link = f"https://youtu.be/{vid_id}"
        # print(vid_link)
        # if i == rand_vid_num:
            # print(" - the chosen one")
            # return vid_link
        # print()
        # i += 1
     
    # need to get nextPageToken and pass in as a pageToken to get next n results    

if __name__ == "__main__":
    main()