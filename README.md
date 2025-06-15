# M3U8 Marauder 🌶️

## About

Download stupid m3u8 segmented videos.

## Setup

Set your environment variables:

### API

This is the API endpoint videos are fetched from. You can find this by opening the page containing the source video and inspecting the network with dev tools (`F12` in Chrome).

Re-load the page containing the video you want to download and search for the network request with `.m3u8`. Inspect this request to get the API your webpage requested it from. Enter this API in the `API` variable.

```bash
# If the example API URL is https://api.mywebsite.com/v2/videos/vid180282/sd.m3u8 then we set the API_URL variable to 
API_URL=https://api.mywebsite.com/v2/videos/
```

(Note: Sometimes, old videos may just be raw `.mp4` files. This usually will result in a 404 error when attempting to download the video, even if you can view the video on the webpage.)

### M3U8_PREFIX

This is the prefix (if one exists) to the `.m3u8` file requested via the webpage.

```bash
# If the example API URL is https://api.mywebsite.com/v2/videos/vid180282/sd.m3u8 then we set the M3U8_PREFIX variable to 
M3U8_PREFIX=sd
```

### OUTPUT PATH

This is the output path for downloaded videos, defaults to `/downloads` in the current directory.

### DELIMITER

When using a full URL for requests, this splits the full URL to get the video ID. If using just IDs, leave this blank.
Note, this is the website URL, *not* the API URL.

```bash
# If the URL is
https://mywebsite/view/vid180282

# Then the Video ID is
vid180282

# And the DELIMITER is
view/
```

### INPUT_FILE

Use for batch requests, this allows you to provide a list of video IDs or URLs to parse through.

URLS (remember to set the `DELIMITER`)

```txt
https://mywebsite/view/vid123412
https://mywebsite/view/vid155682
https://mywebsite/view/vid197362
https://mywebsite/view/vid184685
```

Video IDs

```txt
vid123412
vid155682
vid197362
vid184685
```

**NOTE: You can only use full URLs OR video IDs at one time.**

## Execution

If using batch requests, create and populate an `inputs.txt` file in the [`./data`](./data/) directory. Additionally, specify the `DELIMITER` if using full URLS

If using single requests, just run the script.

```bash
# E.g. using UV

uv run fetch
```
