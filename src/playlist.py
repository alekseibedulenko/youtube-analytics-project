import isodate as isodate

from src.channel import Channel
from  datetime import timedelta

class PlayList:
    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        youtube = Channel.get_service().playlistItems().list(
            playlistId=self.playlist_id,
            part='snippet,contentDetails,id,status',
            maxResults=10,
        ).execute()
        playlist_data = youtube.get('items')[0]
        self.title = playlist_data.get('snippet').get('title').split(".")[0]
        self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'

        video_ids = [video['contentDetails']['videoId'] for video in youtube['items']]
        videos = Channel.get_service().videos().list(
            part='contentDetails,statistics',
            id=','.join(video_ids)
        ).execute()
        self.__videos = videos.get('items')

    @property
    def total_duration(self):
        total_duration = timedelta()
        for video in self.__videos:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            total_duration += isodate.parse_duration(iso_8601_duration)
        return total_duration
    def show_best_video(self):
        best_video = max(self.__videos, key=lambda x:x["statistics"]["likeCount"])
        return f"https://youtu.be/{best_video['id']}"

