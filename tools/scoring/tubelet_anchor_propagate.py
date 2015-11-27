#!/usr/bin/env python

import argparse
import sys
import os
sys.path.insert(1, '.')
from vdetlib.utils.protocol import proto_load, proto_dump, track_proto_from_annot_proto
from vdetlib.vdet.dataset import imagenet_vdet_class_idx, imagenet_det_200_class_idx
from vdetlib.vdet.tubelet_cls import anchor_propagate, score_proto_interpolation

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Max pooling on detections around tubelet boxes.')
    parser.add_argument('vid_file')
    parser.add_argument('track_file')
    parser.add_argument('det_file')
    parser.add_argument('save_file')
    parser.add_argument('--cls')
    args = parser.parse_args()

    if os.path.isfile(args.save_file):
        print "{} already exists.".format(args.save_file)
        sys.exit(0)

    vid_proto = proto_load(args.vid_file)
    det_proto = proto_load(args.det_file)
    track_proto = proto_load(args.track_file)

    vid_name = vid_proto['video']
    assert vid_name == track_proto['video']
    cls_index = imagenet_vdet_class_idx[args.cls]

    # spatial max pooling
    score_proto = anchor_propagate(vid_proto, track_proto, det_proto, cls_index)

    # interpolation
    interpolated_score_proto = score_proto_interpolation(score_proto)

    # save score proto
    save_dir = os.path.dirname(args.save_file)
    if not os.path.isdir(save_dir):
        try:
            os.makedirs(save_dir)
        except:
            pass
    proto_dump(interpolated_score_proto, args.save_file)