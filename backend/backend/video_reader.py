import pathlib

import av


def max_pts(filepath: pathlib.Path) -> int:
    """Return pts of the last frame in the video file.

    Args:
        filepath (pathlib.Path): video file

    Returns:
        int: pts of the last frame
    """
    with av.open(str(filepath)) as container:
        stream = container.streams.video[0]
        pts = filter(
            lambda x: x is not None, map(lambda x: x.pts, container.demux(stream))
        )
        return max(pts)


def get_frame_by_pts(
    filepath: pathlib.Path, pts: int, keyframe_only=False
) -> av.VideoFrame:
    """Return frame indexed by exact `pts` from a given file.

    Args:
        filename (pathlib.Path): video file
        pts (int): Frame pts (time expressed in its stream's time base)
        keyframe_only (bool): If True, returns the previous keyframe rather
        than the closest following frame.

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
                if keyframe_only:
                    return frame
                elif frame.pts >= pts:
                    return frame
                elif frame.pts > pts:
                    raise KeyError("Frame pts not found.")


def get_frame_by_pts_approximate(
    filepath: pathlib.Path, pts: int, keyframes_only=False
) -> av.VideoFrame:
    """Return frame with given pts or the previous one.

    Args:
        filename (pathlib.Path): video file
        pts (int): Frame pts (time expressed in its stream's time base)
        keyframes_only (bool): If True, returns the previous keyframe rather
        than the closest following frame.

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
                if keyframes_only:
                    return frame
                elif frame.pts >= pts:
                    return frame
        raise Exception(f"Unknown Error - Frame pts={pts} not found.")


def get_frames_by_pts_approximate(
    filepath: pathlib.Path, pts_list: list[int], keyframes_only=False
) -> av.VideoFrame:
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
        for pts in pts_list:

            def get_frame(pts):
                container.seek(pts, backward=True, stream=stream)
                for packet in container.demux(stream):
                    for frame in packet.decode():
                        if keyframes_only:
                            return frame
                        elif frame.pts >= pts:
                            return frame
                raise Exception(f"Unknown Error - Frame pts={pts} not found.")

            yield get_frame(pts)
