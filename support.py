import taipy.gui.builder as tgb
from taipy.gui import Gui, invoke_callback, get_state_id, Html
from threading import Thread
import gevent
import datetime
import pandas as pd
import tickets, aircall
import time

state_id_list = []
stop_requested = False


def Aircall():
    available = aircall.GetAvailable()
    rows = len(available.index)
    online = []
    if (rows == 1):
        online.append([available["id"].squeeze(), available["name"].squeeze()])
    elif (rows > 1):
        for index, row in available.iterrows():
            online.append([row["id"], row["name"]])

    return online


def TaipyGui():

#    data = pd.read_excel("dataset.xlsx")
    data = tickets.Structure()
    online = Aircall()
    onlineid = f"images/{online[0][0]}.jpg" 
    onlinename = online[0][1]
    timetoken = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    chart_data = (
        data
        .sort_values(by=['total'],ascending=True)
        .reset_index()
    )

    def read_data(state, id):
        state.data = tickets.Structure()
        state.timetoken = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        state.online = Aircall()
        state.onlineid = f"images/{online[0][0]}.jpg" 
        state.onlinename = online[0][1]
#        state.data = pd.read_excel("dataset.xlsx")
        state.chart_data = (
            state.data
            .sort_values(by=['total'],ascending=True)
            .reset_index()
        )
        

    layout = {"barmode": "stack", 
              "yaxis": {"title" : "Number of tickets"},
                }

    with tgb.Page() as page:
        with tgb.part(class_name="card"):
            with tgb.layout(columns="1"):
                with tgb.part():
                    tgb.text("# **Support and Service**", mode="md")
        with tgb.part(class_name="card mycard"):
            with tgb.layout(columns="1 5"):
                
                with tgb.part(class_name="container"):
                    tgb.text("# **24/7 support**", mode="md")
                    tgb.image("{onlineid}", class_name="onlineimage")
                    tgb.text("{onlinename}", class_name="onlinename")
                with tgb.part(class_name="container"):
                    tgb.chart(
                    data="{chart_data}",
                    title="Assigned tickets",
                    class_name="my_bar",
                    type="bar", 

                    x="Technichian",
                    y = ["In progress","On hold","New"], 
                    color=["rgb(99, 182, 230)","rgb(133, 235, 164)","rgb(226, 155, 155)"],
                    orientation='v',
                    layout="{layout}"
                )
        with tgb.part(class_name="card"):
             with tgb.layout(columns="1"):
                with tgb.part():
                    tgb.text("Last update - {timetoken}", class_name="onlinename")



    def on_init(state, id):
        state_id = get_state_id(state)
        if (state_id := get_state_id(state)) is not None:
            state_id_list.append(state_id)

    def update_data(state, data):
        state.data = data
        state.timetoken = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        state.online = Aircall()
        state.onlineid = f"images/{online[0][0]}.jpg" 
        state.onlinename = online[0][1]
        state.chart_data = (
            state.data
            .sort_values(by=['total'],ascending=True)
            .reset_index()
        )

    def refresh(gui: Gui):
        gevent.sleep(10)
        global stop_requested
        global state_id_list
        while not stop_requested:
            data = tickets.Structure()
            timetoken = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
#            data = pd.read_excel("dataset.xlsx")
            for state_id in state_id_list:
                print(f"Ticket: {datetime.datetime.now()}")
                invoke_callback(gui, state_id, update_data, args=[data])
            gevent.sleep(60)

    def refreshAircall(gui: Gui):
        gevent.sleep(10)
        global stop_requested
        global state_id_list
        while not stop_requested:
            online = Aircall()
            onlineid = f"images/{online[0][0]}.jpg" 
            onlinename = online[0][1]
            for state_id in state_id_list:
                print(f"Aircall: {datetime.datetime.now()}")
                invoke_callback(gui, state_id, update_data, args=[data])
            gevent.sleep(600)

    gui = Gui(page=page)

    refresh_th = Thread(
        target=refresh,
        args=[gui]
    )
    refresh_th.start()

    refresh_aircall = Thread(
        target=refreshAircall,
        args=[gui]
    )
    refresh_aircall.start()

    try:
        gui.run(title="Support", run_browser=True, use_reloader=True, port=5048, margin="1.2em", watermark="Henrik Bækhus")
    except KeyboardInterrupt as e:
        pass
    finally:
        global stop_requested
        stop_requested = True
        refresh_th.join()
        refresh_aircall.join()


if __name__ == "__main__":
    TaipyGui()
#    Aircall()
