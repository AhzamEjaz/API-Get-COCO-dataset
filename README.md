# API-Get-COCO-dataset
I've created an API to get COCO dataset.

Usage:

```
from COCODataset import COCODataset

ccds = COCODataset()

ccds.get_COCO_img(self, split = 'val', year = '2017', n_examples = 40)
```
Current version contains following download capability:
- split = `'val'`, year = `'2014'`
- split = `'test'`, year = `'2014'`
- split = `'test'`, year = `'2015'`
- split = `'test'`, year = `'2017'`

You have to pull the repository and in `./data` folder it will download the first n_examples and in scope of other parameters.

Further Improvements & bug fixes:
- Enable the repository to download the annotations data from cocowebsite directly and extract images for all splits and n_examples.
- Bug fixes
