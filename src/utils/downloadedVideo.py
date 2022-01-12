from dataclasses import dataclass


@dataclass
class DownloadedVideo:
    title: str
    filename: str
    duration: int
    url: str

    def get_info(self):
        return '`Title`: {}\n`Duration`: {}s\n`Url`: {}'.format(self.title, self.duration, self.url)
