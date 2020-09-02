import cv2, signal
import numpy as np


class ImageRenderer:
    def __init__(self, scene):
        self.scene = scene

    def render(self, output_file):
        image = self.scene.to_image()
        image.save(output_file)


class VideoRenderer:
    def __init__(self, scene):
        self.scene = scene

    def render(self, output_file, step_count, do_scene_update, fps = 24):
        step = 1

        image = self.scene.to_image()
        video_writer = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*'MP4V'), fps, image.size)

        user_stop = False
        def on_user_stop(_1, _2):
            nonlocal user_stop
            user_stop = True
            print('Stopping...')

        signal.signal(signal.SIGINT, on_user_stop)

        print('Rendering video, press Ctrl-C to finish early')
        while step <= step_count and not user_stop:
            print('Calculating frame {}'.format(step))
            video_writer.write(cv2.cvtColor(np.asarray(image), cv2.COLOR_BGR2RGB))
            do_scene_update(self.scene)
            image = self.scene.to_image()
            step += 1

        video_writer.release()

