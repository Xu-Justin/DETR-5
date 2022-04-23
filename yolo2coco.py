import argparse
import json
import os
from PIL import Image

def get_args_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-images', required=True, help='path to directory containing images')
    parser.add_argument('--source-annotations', required=True, help='path to directory containing YOLO annotations (.txt)')
    parser.add_argument('--source-obj', required=True, help='path to YOLO obj.names files')
    parser.add_argument('--target', required=True, help='path to save COCO annotations (.json)')
    return parser

class COCO():    
    def create_info(self, description="", url="", version="", year="", contributor="", date_created=""):
        return {
            "description"   : description,
            "url"           : url,
            "version"       : version,
            "year"          : year,
            "contributor"   : contributor,
            "date_created"  : date_created
        }
    
    def create_license(self, id, name="", url=""):
        return {
            "url"   : url,
            "id"    : id,
            "name"  : name
        }
    
    def create_category(self, id, name, supercategory=""):
        return {
            "id": id,
            "name": name,
            "supercategory": supercategory
        }
    
    def create_image(self, license, file_name, height, width, id, coco_url="", flickr_url="", date_captured=""):
        return {
            "license": license,
            "file_name": file_name,
            "coco_url": coco_url,
            "height": height,
            "width": width,
            "date_captured": date_captured,
            "flickr_url": flickr_url,
            "id": id
        }
    
    def create_annotation(self, id, image_id, category_id, bbox_x, bbox_y, bbox_width, bbox_height,segmentation=list(), iscrowd=0):
        return {
            "id": id,
            "image_id": image_id,
            "category_id": category_id,
            "area": bbox_width * bbox_height,
            "bbox": [
                bbox_x,
                bbox_y,
                bbox_width,
                bbox_height
            ],
            "segmentation": segmentation,
            "iscrowd": iscrowd
        }
    
    def __init__(self):
        self.coco = dict()
        self.coco['info'] = self.create_info()
        self.coco['licenses'] = [self.create_license(1)]
        self.coco['categories'] = list()
        self.coco['images'] = list()
        self.coco['annotations'] = list()
        
    def from_yolo(self, source_images, source_annotations, source_obj):
        print(f"Creating coco from yolo {source_images} {source_annotations} {source_obj}")
        
        with open(source_obj, 'r') as f:
            self.coco['categories'] = list()
            for i, name in enumerate(f.read().splitlines()):
                self.coco['categories'].append(self.create_category(i+1, name))
        
        images_file_names = [file_name for file_name in os.listdir(source_images)]
        annotations_file_names = [file_name for file_name in os.listdir(source_annotations)]
        assert len(images_file_names)==len(annotations_file_names)
        
        images_file_names.sort()
        annotations_file_names.sort()
        
        self.coco['images'] = list()
        self.coco['annotations'] = list()
        for image_file_name, annotation_file_name in zip(images_file_names, annotations_file_names):
            assert str(image_file_name[:-4])==str(annotation_file_name[:-4]), f"Files don't match: {image_file_name} {annotation_file_name}"
            image_id = len(self.coco['images']) + 1            
            image_width, image_height = Image.open(os.path.join(source_images, image_file_name)).size
            self.coco['images'].append(
                self.create_image(
                    license = 1,
                    file_name = image_file_name,
                    height = image_height,
                    width = image_width,
                    id = image_id
                )
            )
            with open(os.path.join(source_annotations, annotation_file_name), 'r') as f:
                for line in f.read().splitlines():
                    cls, x_center, y_center, width, height = list(map(float, line.split()))
                    cls = int(cls)
                    
                    x_center = x_center * image_width
                    y_center = y_center * image_height
                    width = width * image_width
                    height = height * image_height
                    
                    annotation_id = len(self.coco['annotations']) + 1
                    self.coco['annotations'].append(
                        self.create_annotation(
                            id = annotation_id,
                            image_id = image_id,
                            category_id = cls + 1,
                            bbox_x = x_center - (width//2),
                            bbox_y = y_center - (height//2),
                            bbox_width = width,
                            bbox_height = height
                        )
                    )
    
    def JSON(self):
        return json.dumps(self.coco)
    
def main(args):
    print(args)
    
    coco = COCO()
    coco.from_yolo(args.source_images, args.source_annotations, args.source_obj)
    
    with open(args.target, 'w') as f:
        print(f"Writing coco to {args.target}")
        f.write(coco.JSON())
    
    print("Done.")
    
if __name__ == '__main__':
    parser = get_args_parser()
    args = parser.parse_args()
    main(args)