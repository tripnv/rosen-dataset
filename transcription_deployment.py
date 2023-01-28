from whisper import load_model, load_audio
from starlette.requests import Request
import tempfile
import ray
from ray import serve

@serve.deployment(num_replicas=2, ray_actor_options={"num_cpus": .25, "num_gpus": .5})
class Transcriber:
    def __init__(self):
        self.model = load_model('large-v1')

    def _transcribe(self, prepped_audio) -> object:
        # Save file temporarily
        transcription = self.model.transcribe(
            prepped_audio, 
            language = 'Romanian',
            condition_on_previous_text = True,
            verbose = False,
            )

        return transcription

    async def __call__(self, http_request: Request) -> object:
        audio_file = await http_request.json()
        with tempfile.NamedTemporaryFile() as audio_file:
            prepped_audio_array = load_audio(audio_file)
        return self._transcribe(prepped_audio_array)

if __name__ == '__main__':

    translator = Transcriber.bind()
