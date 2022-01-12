import os
import shutil
import string

from src.utils.mediaplayer import MediaPlayer


class FileQueue:
    """
    We will feed this queue object with youtube URLs,
    download the audio and store in the array 'data' the filenames so we can reproduce
    """

    def __init__(self):
        self.data = []

    async def add_url(self, url: string):
        video = await MediaPlayer.from_url(url, loop=False)
        self.data.append(video)
        return video.title

    def get_next(self):
        return self.data.pop(0)  # queue definition XD

    def clear(self):
        folder = 'downloaded'
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
        self.data = []

    def is_empty(self):
        return not self.data

    def size(self):
        return len(self.data)

    def get_queue_info(self):
        if self.is_empty():
            return "**Queue is empty**"
        songs = "\n".join(map(lambda x: x.title, self.data))
        return '**{} songs in queue:**\n{}'.format(self.size(), songs)
