#!/usr/bin/env python3
"""Read local source metadata without editing or uploading the media."""
import argparse
from fractions import Fraction
import json
import math
from pathlib import Path
import shutil
import subprocess
import sys


def number(value):
    try:
        result = float(value)
        return result if math.isfinite(result) else None
    except (TypeError, ValueError):
        return None


def ratio(value):
    try:
        result = Fraction(str(value).replace(":", "/"))
        return result if result > 0 else None
    except (ValueError, ZeroDivisionError):
        return None


def summarize(data):
    streams = data.get("streams", [])
    video = next((x for x in streams if x.get("codec_type") == "video"
                  and not x.get("disposition", {}).get("attached_pic")), None)
    duration = number(data.get("format", {}).get("duration"))
    result = {"ok": True, "hasVideo": video is not None,
              "hasAudio": any(x.get("codec_type") == "audio" for x in streams),
              "durationSeconds": duration, "codedWidth": None, "codedHeight": None,
              "displayWidth": None, "displayHeight": None, "rotationDegrees": None,
              "sampleAspectRatio": None, "fps": None, "frameRate": None,
              "needsVisualCheck": video is None}
    if video is None:
        result["note"] = "没有可用主画面；只有音频时需要确认成片画幅。"
        return result

    width, height = video.get("width"), video.get("height")
    if not isinstance(width, int) or not isinstance(height, int) or width <= 0 or height <= 0:
        raise ValueError("invalid_video_dimensions")
    rotation = None
    for side in video.get("side_data_list", []):
        if "rotation" in side:
            rotation = number(side["rotation"])
            break
    if rotation is None:
        rotation = number(video.get("tags", {}).get("rotate"))
    rotation = rotation if rotation is not None else 0.0
    sar = ratio(video.get("sample_aspect_ratio"))
    fps = ratio(video.get("avg_frame_rate")) or ratio(video.get("r_frame_rate"))
    result.update(codedWidth=width, codedHeight=height, rotationDegrees=rotation,
                  sampleAspectRatio=str(sar) if sar else None,
                  fps=float(fps) if fps else None,
                  frameRate=str(fps) if fps else None)
    if duration is None:
        result["durationSeconds"] = number(video.get("duration"))

    # A missing SAR is not reported as a verified square-pixel display size.
    if sar is None or abs(rotation / 90 - round(rotation / 90)) > 1e-6:
        result["needsVisualCheck"] = True
        result["note"] = "像素比例或旋转元数据不足以可靠推导显示尺寸；结合源帧或ChatCut素材信息确认。"
        return result
    dw, dh = max(1, round(width * float(sar))), height
    if round(rotation / 90) % 2:
        dw, dh = dh, dw
    result.update(displayWidth=dw, displayHeight=dh, needsVisualCheck=False)
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description="只读探测主口播尺寸、旋转、帧率和时长")
    parser.add_argument("media", help="本机素材路径，不接受网络URL")
    args = parser.parse_args(argv)
    source = Path(args.media).expanduser()
    if not source.is_file():
        print(json.dumps({"ok": False, "error": "local_file_not_found"}, ensure_ascii=False))
        return 2
    binary = shutil.which("ffprobe")
    if not binary:
        print(json.dumps({"ok": False, "error": "ffprobe_not_found", "hint": "可先用ChatCut inspect_asset读取素材信息；需要本地探测时再准备ffprobe。"}, ensure_ascii=False))
        return 2
    try:
        proc = subprocess.run([binary, "-v", "error", "-show_streams", "-show_format",
                               "-of", "json", str(source.resolve())],
                              capture_output=True, text=True, timeout=30)
        if proc.returncode:
            raise ValueError("media_probe_failed")
        result = summarize(json.loads(proc.stdout))
        result["filename"] = source.name
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError, subprocess.TimeoutExpired):
        print(json.dumps({"ok": False, "error": "media_probe_failed", "hint": "检查本机文件可读性与格式，或使用ChatCut素材信息继续核对。"}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    sys.exit(main())
