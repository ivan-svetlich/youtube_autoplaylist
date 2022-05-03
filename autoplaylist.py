import argparse
import datetime
from get_ids import get_video_ids, get_playlist_ids
from get_videos_from_playlist import get_videos_from_playlist
from youtube_client import YoutubeClient


def startup(days=0, keyword="歌", results_per_channel=2):
    if results_per_channel < (days + 1):
        results_per_channel = days + 1

    print("Authenticating....")

    youtube_client = YoutubeClient()

    print("Searching playlists...")

    subs_responses = youtube_client.get_subscriptions()
    playlist_ids = []
    video_ids = []
    for sub_response in subs_responses:
        playlist_ids.extend(get_playlist_ids(sub_response))

    num_playlists = len(playlist_ids)

    print(f"Done. {num_playlists} playlist{'s' if num_playlists != 1 else ''} found.")
    print("Searching videos...")

    for playlist_id in playlist_ids:
        videos_response = get_videos_from_playlist(playlist_id, max_results=results_per_channel)
        if videos_response is not None:
            ids = get_video_ids(videos_response, days, keyword)
            video_ids.extend(ids)

    num_videos = len(video_ids)

    print(f"Done. {num_videos} video{'s' if num_videos != 1 else ''} found.")

    if num_videos > 0:
        print(f"Creating new playlist...")

        playlist_title = f"{keyword} Auto Playlist ({datetime.datetime.now()})"
        playlist_id = youtube_client.create_playlist(playlist_title)

        print(f"Done. New playlist: {playlist_title}")
        print(f"Adding videos to playlist...")

        for video_id in video_ids:
            youtube_client.add_video_to_playlist(playlist_id, video_id)

        print(f"Done. {num_videos} video{'s' if num_videos != 1 else ''} added to playlist.")
    else:
        print("Try increasing the number of results per channel "
              "and/or the number of days for the search")
        print("Use --help command to get info about the optional arguments.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--days', nargs='?', type=int, const=0, default=0,
                        help='number of previous days to search in '
                             '(default: 0 (only videos published today), disable: -1)')
    parser.add_argument('-k', '--keyword', nargs='?', const="歌", default="歌",
                        help='video titles must contain this term (default: "歌" (song in Japanese))')
    parser.add_argument('-r', '--results', dest='results_per_channel', nargs='?', type=int, const=2,
                        default=2, help='max number of results to retrieve from each channel/playlist '
                                        '(default: 2, min: 1 result per day)')

    args = parser.parse_args()
    startup(args.days, args.keyword, args.results_per_channel)


if __name__ == '__main__':
    main()
