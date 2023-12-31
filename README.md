## Label attribute editor 

This plugin allows you to edit the attributes of selected labels in the
FiftyOne App.

![image](https://github.com/ehofesmann/edit_label_attributes/assets/21222883/cb345e94-71a0-49c9-b782-dd484ed9f0d6)
<!-- ![image](https://github.com/ehofesmann/edit_label_attributes/assets/21222883/2a80457a-6eb1-4c07-a9f6-46db4d0398d1) -->


## Installation

```shell
fiftyone plugins download https://github.com/ehofesmann/edit_label_attributes
```

Refer to the [main README](https://github.com/voxel51/fiftyone-plugins) for
more information about managing downloaded plugins and developing plugins
locally.

## Run Example

After installing this plugin, you can try the example yourself on the `quickstart` dataset.
```python
import fiftyone as fo
import fiftyone.zoo as foz

dataset = foz.load_zoo_dataset("quickstart")
session = fo.launch_app(dataset)
```


Click on the first image to expand it in the sample modal, select one of the
labels, then click the `Edit label attributes` button.

## TODO:

- [ ] Support video and frame label editing
- [ ] Support editing list and dict attributes like `bounding_box`
