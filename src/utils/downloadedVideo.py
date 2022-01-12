from dataclasses import dataclass


@dataclass
class DownloadedVideo:
    title: str
    filename: str
    duration: int
    url: str

    def get_info(self):
        return '{}\nDuration: {}s\nUrl: {}'.format(self.title, self.duration, self.url)
