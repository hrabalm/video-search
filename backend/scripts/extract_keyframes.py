import av
import click
from indexing import read_frames


@click.command()
@click.argument("input")
@click.argument("output")
def copy_keyframes(input: str, output: str):
    """Transcodes input to output only keeping keyframes."""
    with av.open(output, mode="w") as container:
        first_source_frame = next(read_frames(input))
        stream = container.add_stream("mpeg4", rate=0.5)

        stream.width = first_source_frame.width
        stream.height = first_source_frame.height
        stream.pix_fmt = "yuv420p"

        for frame in read_frames(input, keyframes_only=True):
            frame.pts = None
            frame.time_base = None
            for packet in stream.encode(frame):
                container.mux(packet)


if __name__ == "__main__":
    copy_keyframes()
