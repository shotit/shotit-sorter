# trace.moe-rearranger 

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
curl --location 'http://127.0.0.1:19532/rearrange' \
--form 'candidates="{
    \"candidates\": [
        {
            \"image\": \"https://example.com/a.png\"
        },
        {
            \"image\": \"https://example.com/b.png\"
        },
        {
            \"image\": \"https://example.com/c.png\"
        },
        {
            \"image\": \"https://example.com/d.png\"
        },
        {
            \"image\": \"https://example.com/e.png\"
        },
        {
            \"image\": \"https://example.com/f.png\"
        },
        {
            \"image\": \"https://example.com/g.png\"
        },
        {
            \"image\": \"https://example.com/h.png\"
        },
        {
            \"image\": \"https://example.com/i.png\"
        },
        {
            \"image\": \"https://example.com/j.png\"
        }
    ]
}";type=application/json' \
--form 'target=@"/D:/yourpath/example.png"'
```

The sorted result:

```shell
{
    result: [
        {
            \"image\": \"https://example.com/f.png\"
        },        
        {
            \"image\": \"https://example.com/b.png\"
        },
        {
            \"image\": \"https://example.com/c.png\"
        },
        {
            \"image\": \"https://example.com/d.png\"
        },
        {
            \"image\": \"https://example.com/a.png\"
        },        
        {
            \"image\": \"https://example.com/e.png\"
        },
        {
            \"image\": \"https://example.com/i.png\"
        },
        {
            \"image\": \"https://example.com/j.png\"
        },
        {
            \"image\": \"https://example.com/h.png\"
        },
        {
            \"image\": \"https://example.com/g.png\"
        }        
    ]
}
```
