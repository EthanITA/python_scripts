import os

from pytube import YouTube, Playlist
from rich import print


class YTDownloader:
    home_path = os.path.expanduser("~")
    base_path = f"{os.path.join(home_path, 'Music')}"

    def __init__(self, path: str):
        """
        :param path: relative or absolute path, cross-platform, eg. /home/marco/Music or a subfolder
        """
        if os.path.isabs(path):
            self.path = path
        else:
            self.path = os.path.join(self.base_path, path)

    def download(self, url: str):
        if "playlist?list=" in url:
            playlist = Playlist(url)
            print("Starting index of the playlist: ", end="")
            index = input()
            index = 0 if index == "" else int(index)
            for i, url_video in enumerate(playlist, start=1):
                if i >= index:
                    print(f"{i}/{len(playlist)}", end="\t")
                    self.__download_audio(url_video)
        else:
            self.__download_audio(url)

    def __download_audio(self, url):
        try:
            video = YouTube(url)
            title = video.title
            video.streams.get_audio_only().download(self.path)
            print(f"[bold green]{title}[/bold green]")
        except Exception as e:
            print(f"[bold red]{e} [/bold red]")


def get_download_info():
    print("YouTube link (video or playlist): ", end="")
    url = input()
    print(f"Save to ({YTDownloader.base_path}): ", end="")
    path = input()
    return path, url


if __name__ == '__main__':
    save_path, yt_link = get_download_info()
    yt = YTDownloader(save_path)
    print(f"Downloading to {yt.path}")
    yt.download(yt_link)
