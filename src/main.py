import os
from .utils import authenticate, model_types_lister, get_model_type_info
import names  # requires
import supervisely as sly
from dotenv import load_dotenv
from supervisely.app.widgets import *

from clarifai.client.user import User
import requests

# for convenient debug, has no effect in production
load_dotenv("local.env")
load_dotenv(os.path.expanduser("./supervisely.env"))
api = sly.Api.from_env()

sweep_inputs = []
non_sweep_inputs = []
hyperparam_input_values = {}

stub, userDataObject = authenticate()
print("###########")
print(stub)
print(userDataObject)

model_types = model_types_lister()
model_types_items = [Select.Item(value=mt_id, label=mt_id) for mt_id in model_types]
select_model_type = Select(items=[Select.Item(value="Select", label="Select")]+model_types_items,filterable=True)
print("&&&&&&&&&&&&&&&&&&")

note_box = NotificationBox(
    title="Model Type Info",
    description="",
    box_type="info"
)
note_box.hide()

# sweepable hyperparams
for i in range(3):
    hypm_name = "Hyperparam " + str(i)
    hypm_id = "hypm_" + str(i)
    title = Text(text=hypm_name, status="text", widget_id=hypm_id)
    inp_num = InputNumber(value=7)
    hyperparam_input_values[hypm_id] = inp_num.value
    input = Input(value="Start input value")
    # input._hide = True
    input.hide()
    checkbox = Checkbox(
        content="Enable",
        checked=False,
        widget_id=None,
    )
    card = Card(title="Sweepable Hyperparams", content=Container([title, inp_num, input, checkbox]))
    card.hide()
    # print(card._content._widgets[2]._hide)
    sweep_inputs.append(card)

print(sweep_inputs)

submit_btn = Button(text="Submit")
submit_btn.hide()

layout_widgets = [select_model_type, note_box] + sweep_inputs + [submit_btn]
layout = Container(
    widgets=layout_widgets,
    direction="vertical"
)
app = sly.Application(layout=layout)
# layout._widgets[0].hide()

for i in range(len(sweep_inputs)):
    @sweep_inputs[i]._content._widgets[3].value_changed
    def show_change(value, i=i):
        if value:
            sweep_inputs[i]._content._widgets[1].disable()
            sweep_inputs[i]._content._widgets[1].hide()
            sweep_inputs[i]._content._widgets[2].show()
            hyperparam_input_values[sweep_inputs[i]._content._widgets[0].widget_id] = sweep_inputs[i]._content._widgets[2].get_value()
        else:
            sweep_inputs[i]._content._widgets[1].enable()
            sweep_inputs[i]._content._widgets[1].show()
            sweep_inputs[i]._content._widgets[2].hide()
            hyperparam_input_values[sweep_inputs[i]._content._widgets[0].widget_id] = sweep_inputs[i]._content._widgets[1].get_value()

    @sweep_inputs[i]._content._widgets[1].value_changed
    def change_value(value, i=i):
        hyperparam_input_values[sweep_inputs[i]._content._widgets[0].widget_id] = value

    @sweep_inputs[i]._content._widgets[2].value_changed
    def change_value(value, i=i):
        hyperparam_input_values[sweep_inputs[i]._content._widgets[0].widget_id] = value
    

@submit_btn.click
def submit():
    print(hyperparam_input_values)

@select_model_type.value_changed
def change_model_type(value):
    print(value)
    if value != "Select":
        info = get_model_type_info(value)
        note_box.description = info.model_type.description
        for x in range(len(layout._widgets)):
            if x==0:
                continue
            layout._widgets[x].show()
    else:
        for x in range(len(layout._widgets)):
            if x==0:
                continue
            layout._widgets[x].hide()