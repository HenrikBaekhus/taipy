import taipy.gui.builder as tgb
from taipy.gui import Gui, invoke_callback, get_state_id, Html
import time
import pandas as pd
import numpy as np

datalist = [0, 0.45, 0.23, -0.58, 0.99, -0.01]
data = datalist
# Create the processor

# Define the page with real-time chart
real_time_page = """
# Real-time Data Monitoring

<|chart|data={data}|type=line|>
"""

def on_init(state, id):
    state_id = get_state_id(state)
    print("Hello World")
    if (state_id := get_state_id(state)) is not None:
        state_id_list.append(state_id)
        print(state_id_list)

def on_change(state):
    state.data = state.datalist

def on_page_load(state):
    new_value = np.random.randn()
    print(new_value)
    datalist.append(new_value)
    datalist = data[-50:]  # Keep last 50 points
    
    for i in range(10):
        state.data = datalist
        time.sleep(2)

Gui(real_time_page).run(use_reloader=True, run_browser=False)
