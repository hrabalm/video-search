export interface ObjectId {
  _id: string;
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
  tags: Array<VideoTag>;
}
