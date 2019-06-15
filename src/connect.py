from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
import threading
import sys
import os
import json
import sound


def resource_path(relative):  # build用
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)


# アプリの用意
ui_path = resource_path("static/ui_files")
config_path = resource_path("static/config.json")
result_path = resource_path("static/result.json")
page_status = [0, 10]  # 現在のページ, 総ページ(テスト)
history = []  # 画面遷移を履歴を記録していく
now_view = None
app = QtWidgets.QApplication([])
P = None
config = {
    "num_sounds": 10,
    "sounds": ["", ""],
}
dlgs = {}
dlgs["menu"] = uic.loadUi(f"{ui_path}/menu.ui")
dlgs["guide"] = uic.loadUi(f"{ui_path}/guide.ui")
dlgs["test"] = uic.loadUi(f"{ui_path}/test.ui")
dlgs["fin"] = uic.loadUi(f"{ui_path}/fin.ui")
dlgs["result"] = uic.loadUi(f"{ui_path}/result.ui")
dlgs["settings"] = uic.loadUi(f"{ui_path}/settings.ui")


# functions
def MessageBox(title, message):
    QMessageBox.information(None, title, message)


def changeView(bef_dlg, aft_dlg):
    pos = bef_dlg.pos()
    size = bef_dlg.size()
    aft_dlg.move(pos.x(), pos.y())
    aft_dlg.resize(size)
    aft_dlg.show()
    bef_dlg.hide()


def GoGuide():
    global now_view
    history.append(dlgs["menu"])
    now_view = dlgs["guide"]
    changeView(dlgs["menu"], dlgs["guide"])


def GoGuide2Test():
    global now_view, page_status
    history.append(dlgs["guide"])
    now_view = dlgs["test"]
    changeView(dlgs["guide"], dlgs["test"])
    page_status[0] += 1
    dlgs["test"].page_num.setText(f"{page_status[0]-1}/{page_status[1]-1}")
    set_player()


def GoTest2Test():
    global now_view, page_status
    history.append(dlgs["test"])
    now_view = dlgs["test"]
    page_status[0] += 1
    if page_status[0] == page_status[1]:
        # 次で終了
        changeView(dlgs["test"], dlgs["test"])
        dlgs["test"].page_num.setText(f"{page_status[0]-1}/{page_status[1]-1}")
        dlgs["test"].nextButtonT.setText("終了")
    elif page_status[0] > page_status[1]:
        changeView(dlgs["test"], dlgs["fin"])
        now_view = dlgs["fin"]
    else:
        changeView(dlgs["test"], dlgs["test"])
        dlgs["test"].page_num.setText(f"{page_status[0]-1}/{page_status[1]-1}")
    set_player()


def GoMenu():
    global now_view, history, page_status
    history = []
    page_status[0] = 0
    now_view = dlgs["menu"]
    changeView(dlgs["fin"], dlgs["menu"])


def GoResult():
    global now_view
    history.append(dlgs["menu"])
    now_view = dlgs["result"]
    changeView(dlgs["menu"], dlgs["result"])


def GoSettings():
    global now_view
    history.append(dlgs["menu"])
    now_view = dlgs["settings"]
    changeView(dlgs["menu"], dlgs["settings"])


def Back():
    global now_view, page_stauts
    if history != []:
        bef = history.pop()
        changeView(now_view, bef)
        if now_view is dlgs["test"]:
            page_status[0] -= 1
            dlgs["test"].page_num.setText(
                f"{page_status[0]-1}/{page_status[1]-1}")
            set_player()
        now_view = bef


def Apply():
    global config, page_status
    new_num_sounds = dlgs["settings"].NumFiles.text()
    if new_num_sounds.isdigit():
        config["num_sounds"] = int(new_num_sounds)
        page_status[1] = int(new_num_sounds)
    else:
        MessageBox("ERROR", "ファイル数は数字で入力してください.")
    dlgs["settings"].NumFiles.setText("")
    dlgs["settings"].NumFiles.setPlaceholderText(f"{page_status[1]}")
    with open(config_path, "w") as file:
        print("json writing")
        print(config)
        json.dump(config, file)


def SliderUpdate():
    value = dlgs["test"].speed_var.value()
    value = value2var(value)
    run_thread(P.setTask, args=["change_speed", float(value)])
    dlgs["test"].speed_value.setText(f"{value}")

def run_thread(func, args=[]):
    # argsは def hoge(*args) しておく
    thread = threading.Thread(target=func, args=args)
    thread.start()


def play():
    run_thread(P.setTask, args=["play", ])


def pause():
    run_thread(P.setTask, args=["pause", ])


def stop():
    run_thread(P.setTask, args=["stop", ])


def start_app():
    global page_status, config, now_view
    with open(config_path, "r") as file:
        config = json.load(file)
    page_status[1] = int(config["num_sounds"])
    connect_objects()
    dlgs["menu"].show()
    now_view = dlgs["menu"]
    app.exec()


def set_player():
    global P
    if P is not None:
        P.done()
    P = sound.Player()


def exit_app():
    sys.exit(app.exec_())


def value2var(value):
    return f"{0.5 + value / 100:.1f}"


# Connect OBJ <-> Functions
def connect_objects():
    # menu Objects
    dlgs["menu"].GoTestButton.clicked.connect(GoGuide)
    dlgs["menu"].GoResultButton.clicked.connect(GoResult)
    dlgs["menu"].GoSettingsButton.clicked.connect(GoSettings)
    dlgs["menu"].ExitButton.clicked.connect(exit_app)

    # guide Objects
    dlgs["guide"].backButtonG.clicked.connect(Back)
    dlgs["guide"].nextButtonG.clicked.connect(GoGuide2Test)

    # test Objects
    dlgs["test"].backButtonT.clicked.connect(Back)
    dlgs["test"].nextButtonT.clicked.connect(GoTest2Test)
    dlgs["test"].startButton.clicked.connect(play)
    dlgs["test"].pauseButton.clicked.connect(pause)
    dlgs["test"].stopButton.clicked.connect(stop)
    dlgs["test"].speed_value.setReadOnly(True)
    dlgs["test"].speed_var.sliderReleased.connect(SliderUpdate)
    dlgs["test"].speed_var.setValue(50)
    dlgs["test"].speed_value.setText(value2var(50))
    dlgs["test"].page_num.setText(f"{page_status[0]-1}/{page_status[1]-1}")

    # fin
    dlgs["fin"].GoMenuButton.clicked.connect(GoMenu)

    # Result
    dlgs["result"].backButtonR.clicked.connect(Back)
    # dlgs["result"].resetButton.clicked.connect()
    dlgs["result"].ResultTable.setRowCount(4)
    dlgs["result"].ResultTable.setColumnCount(2)
    dlgs["result"].ResultTable.setItem(0, 0, QTableWidgetItem("0"))
    dlgs["result"].ResultTable.setItem(0, 1, QTableWidgetItem("1.2"))
    dlgs["result"].ResultTable.setItem(1, 0, QTableWidgetItem("1"))
    dlgs["result"].ResultTable.setItem(1, 1, QTableWidgetItem("0.9"))
    dlgs["result"].ResultTable.setItem(2, 0, QTableWidgetItem("2"))
    dlgs["result"].ResultTable.setItem(2, 1, QTableWidgetItem("0.7"))
    dlgs["result"].ResultTable.setItem(3, 0, QTableWidgetItem("3"))
    dlgs["result"].ResultTable.setItem(3, 1, QTableWidgetItem("1.1"))
    # dlgs["result"].Selector

    # Settings
    dlgs["settings"].backButtonS.clicked.connect(Back)
    dlgs["settings"].ApplyButton.clicked.connect(Apply)
    dlgs["settings"].NumFiles.setPlaceholderText(f"{page_status[1]}")


# 実行
if __name__ == "__main__":
    start_app()
