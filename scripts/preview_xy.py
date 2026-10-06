"""Video XY con audio a partir del WAV directo del script; no captura del host.

python3 scripts/preview_xy.py recordings/003-orbitas.wav recordings/003-orbitas.mp4
Requiere Pillow y ffmpeg. El WAV original conserva la señal XY sin compresión.
"""
import argparse
from array import array
from pathlib import Path
import subprocess
import sys
import wave

from PIL import Image, ImageDraw


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("wav", type=Path)
    parser.add_argument("video", type=Path)
    args = parser.parse_args()
    if args.video.exists():
        parser.error("El video ya existe; elegí otro nombre para conservarlo")
    with wave.open(str(args.wav)) as source:
        if (source.getnchannels(), source.getsampwidth()) != (2, 2):
            parser.error("Se requiere WAV estéreo PCM de 16 bits")
        rate = source.getframerate()
        samples = array("h", source.readframes(source.getnframes()))
    if sys.byteorder != "little":
        samples.byteswap()
    fps, size = 30, 640
    frames = (len(samples)//2*fps + rate-1)//rate
    command = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-n", "-f", "rawvideo",
               "-pix_fmt", "rgb24", "-s", f"{size}x{size}", "-r", str(fps), "-i", "-",
               "-i", str(args.wav), "-map", "0:v", "-map", "1:a", "-c:v", "libx264",
               "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
               "-shortest", "-movflags", "+faststart", str(args.video)]
    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    try:
        for frame in range(frames):
            start = frame*rate//fps
            stop = min(len(samples)//2, (frame+1)*rate//fps)
            image = Image.new("RGB", (size, size), (4, 10, 15))
            draw = ImageDraw.Draw(image)
            points = [(size/2 + samples[i*2]/32768*size*0.57,
                       size/2 - samples[i*2+1]/32768*size*0.57)
                      for i in range(start, stop)]
            if len(points) > 1:
                draw.line(points, fill=(85, 245, 190), width=2)
            draw.text((16, 16), args.wav.stem, fill=(220, 240, 240))
            draw.text((16, size-28), f"{frame/fps:05.1f} s | XY directo, sin efectos del host",
                      fill=(160, 185, 195))
            process.stdin.write(image.tobytes())
    finally:
        process.stdin.close()
        result = process.wait()
    if result:
        raise SystemExit(f"ffmpeg terminó con código {result}")
    print(args.video)


if __name__ == "__main__":
    main()
