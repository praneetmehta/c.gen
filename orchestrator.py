import json
import os
import time
from types import SimpleNamespace
from content_provider.config.content_provider_type import ContentProviderType
from image_generator.entities.font_enum import Font
from image_generator.entities.image_config import ImageConfig
from content_provider.config.content import Content
from content_provider.config.content_provider_request import ContentProviderRequest
from content_provider.config.default_content_provider_config import ContentProviderConfig
from content_provider.content_provider_factory import ContentProviderFactory
from image_generator.entities.request import Request
from image_generator.entities.text_config import TextConfig
from image_generator.generator import generate_image
from orchestrator_config import OrchestrationRequest


class Orchestrator:

    def __init__(self):
        self._init_dependencies()

    def _init_dependencies(self):
        self._content_provider_factory = ContentProviderFactory()

    def run(self, request : OrchestrationRequest):
        dir_to_use = '/Users/praneet/c.gen_content/'+str(request.run_id)
        os.mkdir(dir_to_use)
        os.mkdir(dir_to_use + '/frames')
        os.mkdir(dir_to_use + '/tmp_bg_frames')
        content_provider = self._content_provider_factory.get_content_provider(request.content_provider_type)
        if (content_provider != None):
            content : Content = content_provider.generate_content(ContentProviderRequest(request.request_topic), ContentProviderConfig())
            print(content.content)
            if content.use_segmented and content.content_segmented != None:
                for i, segment in enumerate(content.content_segmented):
                    generate_image(Request(segment, dir_to_use + '/frames/{}.png'.format(i)), request.text_config, request.image_config)

        os.system("./ffmpeg -framerate 0.2 -i " + dir_to_use + "/frames/%1d.png -vf fps=10 -pix_fmt yuv420p " + dir_to_use +"/output_without_audio.mp4")
        output = os.popen("./ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {}/output_without_audio.mp4".format(dir_to_use))
        duration = int(float(output.read().strip('\n')))
        os.system('./ffmpeg -i {}/output_without_audio.mp4 -i /Users/praneet/Downloads/music_ncs.mp3 -af "afade=t=in:st=0:d=10,afade=t=out:st={}:d=10" -shortest -c:v copy -c:a aac {}/output.mp4'.format(dir_to_use, str(duration-10), dir_to_use))

if __name__ == "__main__":
    orch : Orchestrator = Orchestrator()
    run_id = time.time()
    img_config_json = open('config/default_image_config.json', 'r').read()
    txt_config_json = open('config/default_text_config.json', 'r').read()
    
    img_config : ImageConfig = json.loads(img_config_json, object_hook=lambda d: SimpleNamespace(**d))
    txt_config : TextConfig = json.loads(txt_config_json, object_hook=lambda d: SimpleNamespace(**d))
    txt_config.font = Font.CHALK
    orch.run(OrchestrationRequest(request_topic="amsterdam", run_id=run_id, image_config=img_config, text_config=txt_config, content_provider_type=ContentProviderType.DAY_FACT))