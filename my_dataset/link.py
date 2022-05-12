import argparse
parser = argparse.ArgumentParser(description='Link dataset')
parser.add_argument('--source', type=str, required=True, help='Path to dataset.')
args = parser.parse_args()

import os
def link(source, target):
    os.makedirs(target, exist_ok=True)
    print(f"Create symbolic link from {source} to {target}")
    os.system(f"ln -s -r {source}* {target}")
    
root = args.source

link(os.path.join(root, 'mixed/train/images/'), 'train/images/')
link(os.path.join(root, 'mixed/val/images/'), 'val/images/')

link(os.path.join(root, 'mixed/train/annotations.json'), 'train/')
link(os.path.join(root, 'mixed/val/annotations.json'), 'val/')