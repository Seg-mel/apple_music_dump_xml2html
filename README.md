# Apple Music Dump converter from XML to HTML

If you want to see your music library from Apple Music on a pretty compact human-readable HTML page,
this is what you need.

This util generates an HTML file where you can see:
1. Artists -> Albums -> Tracks
2. Playlists -> Tracks

This is not a site, just a single file without any interactive stuff, except collapsable blocks.

I decided to write it in case of streaming death or bloking it. 
The main purpose is to have the ability to restore my library offline.

## Usage

Here are several steps to make it work

### Apple Music library dump

Please export your full Apple Music library from your Mac (yes, only macOS client can do that).
The official docs of how to do this: https://support.apple.com/en-gb/guide/music/mus27cd5060f/mac.

### Run the util with Docker

This is the preferralble way as you don't need to care about the Python environment.

1. (optional) Install [Docker](https://docs.docker.com/desktop/)
2. Clone this repo
3. Go to the cloned directory
4. Run command
    ```shell
    make convert-docker i=<path_to_your_dump>/Library.xml o=<path_to_output_html>/Library.html
    ```
5. Open the resulting file in your browser
That's all!

If you want to clean up after this util, just run the command
```shell
make rm-all
```

### Run with your local system python

If you want to make it in a raw way, here the instruction
1. (optional) Install [Python](https://www.python.org/downloads/)
2. Install UV `pip install uv`
3. Create venv `uv sync --all-groups`
4. Activate venv `source .venv/bin/activate`
5. Run command
    ```shell
    python am_xml2html -i <path_to_your_dump>/Library.xml -o <path_to_output_html>/Library.html
    ```
6. Open the resulting file in your browser
Congrats again!

To clean up:
1. Remove repo with venv inside it
2. Remove installed Python (if you did that)

