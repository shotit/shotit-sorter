# Shotit-sorter


[![License](https://img.shields.io/github/license/shotit/shotit-sorter.svg?style=flat-square)](https://github.com/shotit/shotit-sorter/blob/master/LICENSE)
[![Coverage](https://img.shields.io/codecov/c/github/shotit/shotit-sorter/main.svg?style=flat)](https://app.codecov.io/gh/shotit/shotit-sorter/branch/main)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/shotit/shotit-sorter/docker-image.yml?branch=main&style=flat-square)](https://github.com/shotit/shotit-sorter/actions)
[![Docker](https://img.shields.io/docker/pulls/lesliewong007/shotit-sorter?style=flat-square)](https://hub.docker.com/r/lesliewong007/shotit-sorter)
[![Docker Image Size](https://img.shields.io/docker/image-size/lesliewong007/shotit-sorter/latest?style=flat-square)](https://hub.docker.com/r/lesliewong007/shotit-sorter)



Sort the search results of Shotit to increase the correctness of Top1 result by using Keras and Faiss.

Development Guide:

> \> python -m venv venv 
>
> \> cd venv/Scripts
>
> \> activate
>
> \> cd ../..
>
> \> python -m pip install -r requirements.txt
>
> \> python -m uvicorn main:app --port 19532

The restful endpoint:

```shell
curl --location 'http://127.0.0.1:19532/sort' \
--form 'candidates="{
    \"candidates\": [
        {
            \"image\": \"https://i.ibb.co/JCj5T41/big-buck-bunny-1.png\"
        },
        {
            \"image\": \"https://i.ibb.co/JCj5T41/big-buck-bunny-2.png\"
        },
        {
            \"image\": \"https://i.ibb.co/JCj5T41/big-buck-bunny-3.png\"
        },
        {
            \"image\": \"https://i.ibb.co/JCj5T41/big-buck-bunny-4.png\"
        },
        {
            \"image\": \"https://i.ibb.co/JCj5T41/big-buck-bunny-5.png\"
        },
        {
            \"image\": \"https://i.ibb.co/JCj5T41/big-buck-bunny-6.png\"
        },
        {
            \"image\": \"https://i.ibb.co/JCj5T41/big-buck-bunny-7.png\"
        },
        {
            \"image\": \"https://i.ibb.co/JCj5T41/big-buck-bunny-8.png\"
        },
        {
            \"image\": \"https://i.ibb.co/JCj5T41/big-buck-bunny-9.png\"
        },
        {
            \"image\": \"https://i.ibb.co/JCj5T41/big-buck-bunny-10.png\"
        },
        {
            \"image\": \"https://i.ibb.co/JCj5T41/big-buck-bunny-11.png\"
        }
    ]
}";type=application/json' \
--form 'target=@"/D:/yourpath/big-buck-bunny-10.png"'
```

The sorted result:

```shell
{
    result: [
        {
            \"image\": \"https://i.ibb.co/KGwVkqy/big-buck-bunny-10.png\"
        },        
        {
            \"image\": \"https://i.ibb.co/KGwVkqy/big-buck-bunny-4.png\"
        },
        {
            \"image\": \"https://i.ibb.co/KGwVkqy/big-buck-bunny-2.png\"
        },
        {
            \"image\": \"https://i.ibb.co/KGwVkqy/big-buck-bunny-9.png\"
        },
        {
            \"image\": \"htthttps://i.ibb.co/KGwVkqy/big-buck-bunny-7.png\"
        },        
        {
            \"image\": \"https://i.ibb.co/KGwVkqy/big-buck-bunny-8.png\"
        },
        {
            \"image\": \"https://i.ibb.co/KGwVkqy/big-buck-bunny-3.png\"
        },
        {
            \"image\": \"https://i.ibb.co/KGwVkqy/big-buck-bunny-11.png\"
        },
        {
            \"image\": \"https://i.ibb.co/KGwVkqy/big-buck-bunny-5.png\"
        },
        {
            \"image\": \"https://i.ibb.co/KGwVkqy/big-buck-bunny-6.png\"
        },
        {
            \"image\": \"https://i.ibb.co/KGwVkqy/big-buck-bunny-1.png\"
        }        
    ]
}
```
