import av
import click

from indexing import read_frames


@click.command()
@click.argument("input", help="Input video file.")
@click.argument("output", help="Output video file.")
def copy_keyframes(input: str, output: str):
    """Transcodes input to output only keeping keyframes."""
    with av.open(output, mode="w") as container:
        stream = container.add_stream("mpeg4", rate=0.5)
        for frame in read_frames(input, keyframes_only=True):
            frame.pts = None
            frame.time_base = None
            for packet in stream.encode(av.VideoFrame.reformat(frame)):
                container.mux(packet)


if __name__ == "__main__":
    copy_keyframes()
