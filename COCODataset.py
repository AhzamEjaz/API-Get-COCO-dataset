import os
from tqdm import tqdm
import json
import requests

class COCODataset:
    def __init__(self):
        directory_items = os.listdir('.')

        root_dir = './data'
        folders_dict = {
                    'data':{
                        '2014':{
                            'train':{'imgs':'/', 'Annot': '/'},
                            'val':{'imgs':'/', 'Annot': '/'},
                            'test':{'imgs':'/', 'Annot': '/'}
                            },
                        '2015':{
                            'test':{'imgs':'/', 'Annot': '/'}
                            },
                        '2017':{
                            'train':{'imgs':'/', 'Annot': '/'},
                            'val': {'imgs':'/', 'Annot': '/'},
                            'test': {'imgs':'/', 'Annot': '/'}
                            }
                        }
                }

        data_paths = []
        for d in folders_dict.keys():
            
            
            for year in folders_dict[d].keys():
                root_path = os.path.join('.', d)
                yr_path = os.path.join(root_path, year)
                for split in folders_dict[d][year]:

                    split_path = os.path.join(yr_path, split)
                    for item in folders_dict[d][year][split]:
                        current_path = os.path.join(split_path, item)
                        data_paths.append(current_path)
        for data_path in data_paths:
            if os.path.exists(data_path):
                print('Path Exists! {}'.format(data_path))
            else:
                print("Does not exist! {}".format(data_path))
                os.makedirs(data_path)
                print("Path Created!")
    def get_COCO_img(self, split = 'test', year = '2014', n_examples = 40):
        if split == 'test':
            parent_folder = 'test_img_info'
            file_name = f'image_info_{split}{year}.json'
        else:
            parent_folder = 'all_person_Keypoints'
            file_name = f'person_keypoints_{split}{year}.json'
            self.get_annotations(split = split, year = year, n_examples=n_examples)
        root_path = os.path.join(os.path.join(os.path.join('.', 'data'), year), split)
        imgs_path = os.path.join(root_path, 'imgs')
        Annots_path = os.path.join(root_path, 'Annots')
        keypoints_path = os.path.join(os.path.join(os.path.join('.', 'data'), parent_folder), file_name)
        with open(keypoints_path, 'r') as file:
            person_keypoints = json.load(file)
        
        def download_img(url, save_path):
            try:
                response = requests.get(url)
                response.raise_for_status()
                with open(save_path, 'wb') as file:
                    file.write(response.content)
            except requests.RequestException as e:
                print(f'Failed to download {url}: {e}')
        print('Downloading...')
        for i in tqdm(range(n_examples)):
            cur_en = person_keypoints['images'][i]
            save_path = os.path.join(imgs_path, cur_en['file_name'])
            url = cur_en['coco_url']
            download_img(url, save_path)
        print(f'Download for {n_examples} complete.')
    def get_annotations(self, split, year, n_examples):
        file_name = f'instances_{split}{year}.json'
        file_path = os.path.join(os.path.join(os.path.join('.', 'data'), 'all_annotations'), file_name)
        save_path = os.path.join(os.path.join(os.path.join(os.path.join(os.path.join('.', 'data'), year), split), 'Annot'), file_name)
        print(file_path)
        
        with open(file_path, 'r') as file:
            annots = json.load(file)
        
        print(annots.keys())
        new_annots = {
                'info': annots['info'],
                'images': annots['images'][:n_examples],
                'licenses': annots['licenses'],
                'annotations': annots['annotations'][:n_examples],
                'categories': annots['categories']
                }
        new_annots = json.dumps(new_annots, indent = 4)
        with open(save_path, 'w') as file:
            file.write(new_annots)
        print('Annotation Saved!')

if __name__=='__main__':
    ccds = COCODataset()
    img_info_dict = ccds.get_COCO_img(split='train', n_examples=40)
