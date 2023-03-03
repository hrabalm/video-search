import pathlib

import av
from toolz import concat, tail


def max_pts(filepath: pathlib.Path) -> int:
    """Return pts of the last frame in the video file.

    Args:
        filepath (pathlib.Path): video file

    Returns:
        int: pts of the last frame
    """
    with av.open(str(filepath)) as container:
        stream = container.streams.video[0]
        # look into last 3 packets
        packets = tail(3, container.demux(stream))

        frames = concat(p.decode() for p in packets)
        return max(f.pts for f in frames)


def get_frame_by_pts(filepath: pathlib.Path, pts: int) -> av.VideoFrame:
    """Return frame indexed by exact `pts` from a given file.

    Args:
        filename (pathlib.Path): video file
        pts (int): Frame pts (time expressed in its stream's time base)

    Raises:
        KeyError: Raised when pts not found in a file.

    Returns:
        av.VideoFrame: Resulting VideoFrame
    """
    with av.open(str(filepath)) as container:
        stream = container.streams.video[0]
        container.seek(pts, backward=True, stream=stream)
        for packet in container.demux(stream):
            for frame in packet.decode():
                if frame.pts == pts:
                    return frame
                elif frame.pts > pts:
                    raise KeyError("Frame pts not found.")


def get_frame_by_pts_approximate(filepath: pathlib.Path, pts: int) -> av.VideoFrame:
    """Return frame with given pts or the previous one.

    Args:
        filename (pathlib.Path): video file
        pts (int): Frame pts (time expressed in its stream's time base)

    Raises:
        KeyError: Raised when pts not found in a file.

    Returns:
        av.VideoFrame: Resulting VideoFrame
    """
    with av.open(str(filepath)) as container:
        stream = container.streams.video[0]
        container.seek(pts, backward=True, stream=stream)
        for packet in container.demux(stream):
            for frame in packet.decode():
                if frame.pts >= pts:
                    return frame
        raise Exception(f"Unknown Error - Frame pts={pts} not found.")
