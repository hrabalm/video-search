# TODO

- [ ] write utility function to visualize video tags (webpage, pdf, ODF, whatever)
    - [ ] can be useful for reports
    - [ ] embed the images and table with results, metadata, statistics, etc.
- [ ] prediction.py
    - [ ] finish VideoTag, WrappedImage
    - [ ] add convertor for grouped predictions to VideoTag
    - [ ] try to serialize it to JSON and save to MongoDB
- [ ] Store in MongoDB
- [ ] Add test data (video/image) to LFS
- [ ] end-to-end video tagging/indexing function
- [ ] Store full frame for the best tag result


- [ ] Object detection -> multiple tags
- [ ] use `dramatiq`
- [ ] basic web UI
- [ ] hashing, (md5, size) ?
- [ ] basic similarity search
    - Python libraries, OpenCV, Elasticsearch


- [ ] ??? try porting to C# + `Blazor`
- [ ] ??? try porting to F# + `Fable`

https://huggingface.co/kiheh85202/yolo
https://huggingface.co/facebook/detr-resnet-50-panoptic
https://huggingface.co/microsoft/beit-base-finetuned-ade-640-640

## Done

- [x] setup `redis` in `docker-compose`
- [x] Store frame timestamp/index
- [x] Multiple output tags for a single frame
- [x] speak with Skopal, questions:
    - [x] exam?
    - [x] project terms?
    - [x] resend specification email
