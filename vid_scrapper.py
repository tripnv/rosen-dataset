import os
import shutil
import requests
import validators
import yt_dlp as ytdl
from utils import pop_log


class VideoScrapper:
    def __init__(self, list_of_urls):
        self.videos_urls = self._keep_supported_urls(list_of_urls)

    @staticmethod
    def _valid_yt_url(url: str) -> bool:
        """
        Validate from multiple possibilities of a youtube link name.
        :param url: URL to a youtube video.
        :return:
            true: if we identify at least one variation
            false: if the provided URL is a non-yt one
        """
        yt_link_variations = [
            "y2u.be",
            "youtu.be",
            "m.youtu.be",
            "youtube.com",
            "m.youtube.com"
        ]

        return any([True if variation in url else False for variation in yt_link_variations])

    def _keep_supported_urls(self, list_of_urls: list[str]) -> list[str]:
        """
        Keep only the valid URLs provided by user.

            1. The URL should be a valid URL format.
            2. The URL should be a valid yt link.
            3. Verify if we get any response by sending a request to the yt URL.

        :param list_of_urls: list of URLs as strings
        :return:
            [list] - list which only contains the valid URLs from the original list
        """
        pop_log("Checking provided URLs ...", "LOG")

        valid_url_keeped = []

        for current_url in list_of_urls:

            # current url is a valid link?
            if not validators.url(current_url):
                pop_log(f"Current URL passed. Not a valid link: {current_url}", "WARNING")
                continue

            # current url is a valid youtube link?
            elif not self._valid_yt_url(current_url):
                pop_log(f"Current URL passed. Not a valid link: {current_url}", "WARNING")
                continue

            # do we get a response for the url?
            elif requests.get(current_url).status_code != 200:
                pop_log(f"Current URL passed. Couldn't get a response for this link: {current_url}", "WARNING")
                continue

            pop_log(f"Valid URL: {current_url}", 'LOG')
            valid_url_keeped.append(current_url)

        return valid_url_keeped

    def download_wav(self) -> None:
        """
        Download wav files based on list of URLs.

            1. Create a "wav_outputs" directory for the wav files.
            2. Create configuration for ytdl
            3. Start getting the wav files out inside output directory.
        """

        current_folder_path = os.path.dirname(os.path.realpath(__file__))
        folder_wav_output = os.path.join(current_folder_path, "wav_outputs")

        if not os.path.exists(folder_wav_output):
            os.makedirs(folder_wav_output)
        else:
            shutil.rmtree(folder_wav_output)
            os.makedirs(folder_wav_output)

        ydl_opts = {
            'format': 'bestaudio/best',                     # format
            'yes-playlist': 'true',                         # accept playlist
            'ignore-errors': 'true',                        # ignore errors
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',                # extractor
                'preferredcodec': 'wav',                    # file type
                'preferredquality': '192',                  # quality

            }],
            'outtmpl': folder_wav_output + '/%(title)s%(autonumber)s.%(ext)s', # title, auto-num (for same title
                                                                               # videos), ext
        }

        with ytdl.YoutubeDL(ydl_opts) as ydl:
            ydl.download(self.videos_urls)
