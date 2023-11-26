import fiftyone.operators as foo
import fiftyone.operators.types as types
import fiftyone.core.labels as fol

IGNORE_ATTRS = ["id", "attributes", "tags"]

def get_label(samples, label_dict):
    view = samples.select_labels(ids=[label_dict[0]["labelId"]])
    sample = view.first()
    label = sample[label_dict[0]["field"]]
    if isinstance(label, fol._HasLabelList):
        label = getattr(label, label._LABEL_LIST_FIELD)[0]

    return sample, label


class EditLabelAttributes(foo.Operator):
    @property
    def config(self):
        return foo.OperatorConfig(
            name="edit_label_attributes",
            label="Edit label attributes",
            dynamic=True,
        )

    def resolve_placement(self, ctx):
        return types.Placement(
            types.Places.SAMPLES_VIEWER_ACTIONS,
            types.Button(
                label="Edit label attributes",
                prompt=True,
            ),
        )

    def resolve_input(self, ctx):
        inputs = types.Object()
        if len(ctx.selected_labels)==0:
            warning = types.Warning(label="No labels are selected")
            prop = inputs.view("warning", warning)
            prop.invalid = True  # so form's `Execute` button is disabled
            return types.Property(inputs, view=types.View(label="Edit label attributes"))

        if len(ctx.selected_labels) > 1:
            warning = types.Warning(label="Labels can only be edited one at a time but %d are selected" % len(ctx.selected_labels))
            prop = inputs.view("warning", warning)
            prop.invalid = True  # so form's `Execute` button is disabled
            return types.Property(inputs, view=types.View(label="Edit label attributes"))

        label_dict = ctx.selected_labels

        sample, label = get_label(ctx.dataset, label_dict)
        ctx.params["parse_values"] = {}
        for attr_name, attr_value in label.iter_fields():
            if attr_name not in IGNORE_ATTRS and isinstance(attr_value, (str, bool, int, float)):
                ctx.params["parse_values"][attr_name] = type(attr_value)
                getattr(inputs, type(attr_value).__name__)(attr_name, label=attr_name, default=attr_value)

        return types.Property(inputs, view=types.View(label="Edit label attributes"))


    def execute(self, ctx):
        label_dict = ctx.selected_labels
        sample, label = get_label(ctx.dataset, label_dict)
        for attr_name, attr_type in ctx.params.get("parse_values", {}).items():
            attr_value = attr_type(ctx.params[attr_name])
            label[attr_name] = attr_value
        sample.save()


def register(p):
    p.register(EditLabelAttributes)
