# Copyright 2018-2020 Streamlit Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import io
import streamlit as st
import numpy as np
import wave
from scipy.io import wavfile

st.title("Audio test")

st.header("Local file")
sample_sounds = """
For samples of sounds in different formats, see
https://docs.espressif.com/projects/esp-adf/en/latest/design-guide/audio-samples.html
"""
st.write(f"{sample_sounds}")

# These are the formats supported in Streamlit right now.
AUDIO_EXTENSIONS = ["wav", "flac", "mp3", "aac", "ogg", "oga", "m4a", "opus", "wma"]



def get_audio_files_in_dir(directory):
    out = []
    for item in os.listdir(directory):
        try:
            name, ext = item.split(".")
        except:
            continue
        if name and ext:
            if ext.lower() in AUDIO_EXTENSIONS:
                out.append(item)
    return out


sample_dir = os.path.expanduser("~/Music/Samples")
files = get_audio_files_in_dir(sample_dir)

if len(files) == 0:
    st.write(
        "Put some audio files in your home directory (%s) to activate this player."
        % sample_dir
    )

else:
    filename = st.selectbox(
        "Select an audio file from your home directory (%s) to play" % sample_dir,
        files,
        0,
    )
    audiopath = os.path.join(sample_dir, filename)
    st.audio(audiopath)


st.header("Generated audio (440Hz sine wave)")


def note(freq, length, amp, rate):
    t = np.linspace(0, length, length * rate)
    data = np.sin(2 * np.pi * freq * t) * amp
    return data.astype(np.int16)


frequency = 440  # hertz
nchannels = 1
sampwidth = 2
sampling_rate = 44100
duration = 89  # Max size, given the bitrate and sample width
comptype = "NONE"
compname = "not compressed"
amplitude = 10000
nframes = duration * sampling_rate

x = st.text("Making wave...")
sine_wave = note(frequency, duration, amplitude, sampling_rate)

fh = wave.open(os.path.join(sample_dir, "sound.wav"), "w")
fh.setparams((nchannels, sampwidth, int(sampling_rate), nframes, comptype, compname))

x.text("Converting wave...")
fh.writeframes(sine_wave)

fh.close()

with io.open(os.path.join(sample_dir, "sound.wav"), "rb") as f:
    x.text("Sending wave...")
    x.audio(f)

st.header("Audio from a Remote URL")


def shorten_audio_option(opt):
    return opt.split("/")[-1]


song = st.selectbox(
    "Pick an MP3 to play",
    (
        "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
        "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3",
        "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-8.mp3",
    ),
    0,
    shorten_audio_option,
)

st.audio(song)

st.title("Streaming audio and Internet Radio:")
st.write("[https://www.hiresaudio.online/cd-quality-internet-radio/](https://www.hiresaudio.online/cd-quality-internet-radio/)")

station_list = """
http://nthmost.net:8000/mutiny-studio
https://stream.440hz-radio.de/440hz-main.mp3?start=1597517799
https://440hz-radio.de/webplayer/player.php
http://nthmost.net:8000/mutiny-studio
https://95bfm.com/
https://www.wdav.org/
http://sectorradio.com/nota/
https://www.h2oradio.fr/index.php#
"""

for url in [i for i in station_list.split('\n') if i ]:
    st.write(f"[{url}]({url})")
    st.audio(f"{url}")
