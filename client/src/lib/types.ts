export interface ObjectId {
  $oid: string;
}

export interface VideoTag {
  model: string;
  tag: string;
  frame_pts: Array<number>;
  conf: number;
}

export interface VideoRecord {
  _id: ObjectId;
  filenames: Array<string>;
  filehash: string;
  thumbnails: Array<string>;
  tags: Array<VideoTag>;
}
