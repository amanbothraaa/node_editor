import dearpygui.dearpygui as dpg #importing as instructed in documentation

dpg.create_context() #context initiation as instructed in documentation

relations = [] #tracking node relations


''''Steps are directly followed from documentation of dearpygui'''

def on():
    with dpg.node(label="ON",parent="node_editor") as on:
        with dpg.node_attribute(attribute_type=1):
            dpg.add_text("1")


def off():
    with dpg.node(label="OFF",parent="node_editor") as off:
        with dpg.node_attribute(attribute_type=1):
            dpg.add_text("0")


def and_gate():
    with dpg.node(label="AND", parent="node_editor", tag="and") as and_gate:
        with dpg.node_attribute() as and_:
            dpg.add_text(default_value=0, tag="and_1")
            print(dpg.get_value(and_1))

        with dpg.node_attribute() as and_2:
            dpg.add_text(default_value=0, tag="and_2")
            print(dpg.get_value(and_2))

        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output) as and_out:
            for i in relations:
                node_attribute_requester = dpg.get_item_parent(i[0])
                node_attribute_sender = -1
                andinput = dpg.get_item_children(i[0],1)[0]
                dpg.configure_item(dpg.get_item_children(i[1], 1)[0], default_value=dpg.get_value(dpg.get_item_children(i[0]&1)[0])[-1])
                print("AND Gate")


def or_gate():
    with dpg.node(label="OR", parent="node_editor", tag="or"):
        with dpg.node_attribute(attribute_type=0) as or_in1:
            dpg.add_text(default_value="0",tag="or_1")

        with dpg.node_attribute(attribute_type=0) as or_in2:
            dpg.add_text(default_value="0",tag="or_2")
        
        with dpg.node_attribute(attribute_type=1):
            dpg.add_text(default_value="0",tag="or_out")

        or_out = (or_in1 | or_in2)

def xor_gate():
    with dpg.node(label="XOR", parent="node_editor", tag="xor"):
        with dpg.node_attribute(attribute_type=0) as xor_in1:
            dpg.add_text(default_value="0", tag="xor_1")
       
        with dpg.node_attribute(attribute_type=0) as xor_in2:
            dpg.add_text(default_value="0", tag="xor_2")

        with dpg.node_attribute(attribute_type=1) as xor_out:
            xor_out = (int(xor_in1)^int(xor_in2))
            dpg.add_text(default_value=xor_out,tag="xor_out")


def not_gate():
    with dpg.node(label="NOT", parent="node_editor", tag="not"):
        with dpg.node_attribute(attribute_type=0) as not_in:
            dpg.add_text(default_value="0", tag="not_1")
       
        with dpg.node_attribute(attribute_type=1) as not_out:
            dpg.add_text(default_value="0",tag="not_out")

        not_out = (~not_in)

def output():
    with dpg.node(parent="node_editor"):
        with dpg.node_attribute(attribute_type=1):
            dpg.add_text("")
        output = (update)

def update():
    for i in relations:
        node_attribute_requester = dpg.get_item_parent(i[0])
        node_attribute_sender = -1

        for link in dpg.get_item_children("node_editor", 0):
            # attr_1 is output, attr_2 is input
            attr_1, attr_2 = dpg.get_item_configuration(link)['attr_1'], dpg.get_item_configuration(link)['attr_2']
            if node_attribute_requester == attr_2:
                node_attribute_sender = attr_1
                break

        text_item = dpg.get_item_children(i[0],1)[0]
        print(dpg.get_value(text_item))

        # Setting the value in the input node when connected
        dpg.configure_item(dpg.get_item_children(i[1], 1)[0], default_value=dpg.get_value(text_item)[-1])


def link():

    def link_callback(sender, app_data):

        # app_data -> (link_id1, link_id2)
        dpg.add_node_link(app_data[0], app_data[1], parent=sender)
        relations.append(app_data)
        update()

    def delink_callback(sender, app_data):
        dpg.delete_item(app_data)
        relations.remove(
            (dpg.get_item_configuration(app_data)["attr_1"], dpg.get_item_configuration(app_data)["attr_2"]))
        dpg.delete_item(app_data)

    with dpg.window(label="Node Editor", width=1920, height=1080, pos=(250, 0), no_move=True, no_collapse=True):

        with dpg.node_editor(tag="node_editor", callback=link_callback, delink_callback=delink_callback):
            pass



def add_gate():

    if dpg.get_value("list") == "ON":
        on()
    if dpg.get_value("list") == "OFF":
        off()
    if dpg.get_value("list") == "AND":
        and_gate()
    if dpg.get_value("list") == "OR":
        or_gate()
    if dpg.get_value("list") == "XOR":
        xor_gate()
    if dpg.get_value("list") == "NOT":
        not_gate()

def delete_item():
    dpg.get_selected_nodes(node_editor)
    dpg.get_selected_links(node_editor)
    dpg.clear_selected_nodes(node_editor)
    dpg.clear_selected_links(node_editor)

gates = ["ON", "OFF", "AND", "OR", "NOT", "XOR"]
dpg.create_context()

with dpg.window(label="Gates and Values", height=1080, width=250):
    dpg.add_listbox(tag="list", items=gates)
    dpg.add_button(label="Add Gate", callback=add_gate)
    dpg.add_button(label="Delete", callback=delete_item) 
    dpg.add_button(label="Get", callback=update)


link()

dpg.create_viewport(title='LogicMaster-v1.0', width=1920, height=1080)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()