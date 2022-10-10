import os
import sys
import shutil
from sampler.src.null_device import null_device

if __name__ == "__main__":

    if len(sys.argv) < 2:

        print("--------------------------------")
        print("This script uses ffmpeg to sample frames from a specified video at a specified sample rate.")
        print("")
        print("Usage: ")
        print("python sampler/tests/ffmpegtest.py 'samplerate' 'videofile'")
        print("ie: python sampler/tests/ffmpegtest.py 5 frames_1s.avi")
        print("--------------------------------")

    else:

        base_dir = os.path.dirname(os.path.realpath(__file__))
        output_dir = base_dir + "/output"

        # clean output dir
        if os.path.exists(output_dir):
            for f in [f for f in os.listdir(output_dir) if f.endswith(".jpg")]:
                os.remove(f"{output_dir}/{f}")
            os.rmdir(output_dir)
        os.mkdir(output_dir)

        # samplerate
        samplerate = int(sys.argv[1])
        print("samplerate: " + str(samplerate))

        # do sampling from test video
        video_file = base_dir + "/" + sys.argv[2]
        command = f'ffmpeg -i {video_file} -vf fps={samplerate} {output_dir}/%d.jpg > {null_device()} 2>&1'
        #print(command)
        os.system(command)

        # prepare to iterate sampled frames
        frames_per_sample = round(30 / samplerate)
        print("frames per sample: " + str(frames_per_sample))
        frames = [f for f in os.listdir(output_dir) if f.endswith(".jpg")]

        # rename sampled frames so their offset matches the frame number
        for frame in frames:
            offset = round(frames_per_sample / 2) + (int(frame.split('.')[0]) - 1) * frames_per_sample
            shutil.copy(f"{output_dir}/{frame}", f"{output_dir}/{offset}_out.jpg")
            os.remove(f"{output_dir}/{frame}")
