import subprocess


video_title = "My Song Title"

def convert_audio_to_video(input_image, input_audio, output_video):
    ffmpeg_cmd = [
        """
        ffmpeg -loop 1 -i {} -i {} -filter_complex "
        [0:v]scale=1920:1080,boxblur=20:10[bg];
        [0:v]scale=540:540,split=2[fg][shadow];

        [shadow]format=rgba,
        colorchannelmixer=aa=0.35,
        boxblur=15:5[shadowblur];

        [bg][shadowblur]overlay=150:(H-h)/2[tmp];
        [tmp][fg]overlay=150:(H-h)/2[main];

        [1:a]aformat=channel_layouts=mono,
        showwaves=s=1920x200:mode=line:rate=30:colors=white[wave];

        [main][wave]overlay=0:H-220[textbg];

        [textbg]drawtext=
        text={video_title}:
        fontcolor=white:
        fontsize=60:
        x=750:
        y=300
        " \
        -c:v libx264 \
        -preset ultrafast \
        -tune stillimage \
        -crf 28 \
        -movflags +faststart \
        -pix_fmt yuv420p \
        -c:a aac \
        -shortest \
        {}
        """.format(input_image, input_audio, output_video)
    ]

    try:
        subprocess.run(ffmpeg_cmd, check=True, shell=True)
        print("Video created successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")


