import numpy as np
from tensorflow import keras
from fastapi import FastAPI, File, Form, UploadFile
from PIL import Image
from urllib import request
from io import BytesIO
import faiss
import json
import copy
import asyncio
import concurrent.futures
import nest_asyncio
nest_asyncio.apply()


class Rearranger:
    '''
    Keras-Faiss section, to rearrange the incoming images according to their VGG16 similarity to the target image
    '''

    def __init__(self) -> None:
        self.model = None
        self.index = None
        self.candidates = None
        self.length = None

    def init_model(self) -> None:
        vgg16_model = keras.applications.vgg16.VGG16(
            weights='imagenet', include_top=True)
        model = keras.Sequential()

        # Remove the last softmax layer. Only use VGG16 to extract feature vector
        for layer in vgg16_model.layers[:-1]:
            model.add(layer)

        # Freeze the layers
        for layer in model.layers:
            layer.trainable = False

        self.model = model

    def faiss_index(self, candidates) -> None:
        dimension = 4096
        index = faiss.IndexFlatL2(dimension)
        self.candidates = copy.deepcopy(candidates)
        self.length = len(candidates)
        candidateVectors = np.empty([self.length, 4096])

        def vectorize_remote_image(index):
            url = candidates[index]["image"]
            res = request.urlopen(url).read()
            img = Image.open(BytesIO(res)).resize((224, 224))
            x = keras.preprocessing.image.img_to_array(img)
            x = np.expand_dims(x, axis=0)
            x = keras.applications.vgg16.preprocess_input(x)
            features = self.model.predict(x)
            candidateVectors[index] = features

        async def asynchronous_requests():
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.length) as executor:
                loop = asyncio.get_event_loop()
                futures = [
                    loop.run_in_executor(
                        executor,
                        vectorize_remote_image,
                        i
                    )
                    for i in range(self.length)
                ]
                for _ in await asyncio.gather(*futures):
                    pass

        loop = asyncio.new_event_loop()
        loop.run_until_complete(asynchronous_requests())

        index.add(candidateVectors)

        self.index = index

    def faiss_search(self, target: bytes) -> None:
        targetVector = np.empty([1, 4096])
        img = Image.open(BytesIO(target)).resize((224, 224))
        x = keras.preprocessing.image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = keras.applications.vgg16.preprocess_input(x)
        features = self.model.predict(x)
        targetVector[0] = features

        D, I = self.index.search(targetVector, self.length)

        # drop faiss index
        self.index = None

        results = []
        for item in I[0]:
            results.append(self.candidates[int(item)])

        # drop candidates
        self.candidates = None
        self.length = None

        return results


rearranger = Rearranger()
rearranger.init_model()


'''
FastAPI section, to provide http service
'''

app = FastAPI()


@app.post("/rearrange")
async def rearrange(
    candidates: str = Form(),
    target: UploadFile = File()
):
    candidates = json.loads(candidates)
    rearranger.faiss_index(candidates["candidates"])
    target_content = await target.read()
    result = rearranger.faiss_search(target_content)

    return {
        "result": result,
    }
