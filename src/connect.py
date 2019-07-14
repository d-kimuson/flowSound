import bug_fix
from PyQt5 import QtCore, QtWidgets, uic
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
result_path = f"{os.getcwd()}/{os.path.dirname(__file__)}/result.json"
history = []  # 画面遷移を履歴を記録していく
sounds = []  # パス
result = {}
result_integrated = {}
now_view = None
now_user = 0
app = QtWidgets.QApplication([])
P = None
config = {
    "num_sounds": 0,
    "now_page": 0
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
    global now_view
    history.append(dlgs["guide"])
    now_view = dlgs["test"]
    changeView(dlgs["guide"], dlgs["test"])
    dlgs["test"].page_num.setText(
        f"{config['now_page']}/{config['num_sounds']}"
        )
    set_player()
    config['now_page'] += 1


def GoTest2Test():
    global now_view, result, P
    if P is not None:
        pause()
        P.done()
    value = value2var(
        dlgs["test"].speed_var.value()
    )
    result[config['now_page']-1] = value
    history.append(dlgs["test"])
    now_view = dlgs["test"]
    if config['now_page'] == config["num_sounds"]:
        # 次で終了
        dlgs["test"].page_num.setText(
            f"{config['now_page']}/{config['num_sounds']}"
            )
        dlgs["test"].nextButtonT.setText("終了")
    elif config['now_page'] > config["num_sounds"]:
        changeView(dlgs["test"], dlgs["fin"])
        now_view = dlgs["fin"]
        return True
    else:
        dlgs["test"].page_num.setText(
            f"{config['now_page']}/{config['num_sounds']}"
            )
    set_player()
    config['now_page'] += 1


def GoMenu():
    global now_view, history, result, P
    history = []
    config['now_page'] = 0
    now_view = dlgs["menu"]
    save2result(result)
    table_update()
    result = {}
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
        if now_view is dlgs["test"] and config['now_page'] != 1:
            config['now_page'] -= 1
            dlgs["test"].page_num.setText(
                f"{config['now_page']}/{config['num_sounds']}"
                )
            dlgs["test"].nextButtonT.setText("次へ")
            if P is not None:
                pause()
                P.done()
            set_player()
        else:
            if now_view is dlgs["test"]:
                config['now_page'] -= 1
            bef = history.pop()
            changeView(now_view, bef)
            now_view = bef


def ResetResults():
    global result_integrated
    # 結果のリセット(削除)
    result_integrated = {}
    with open(result_path, "w") as f:
        json.dump(result_integrated, f)
    table_update()


def SliderUpdate():
    value = dlgs["test"].speed_var.value()
    value = value2var(value)
    run_thread(P.setTask, args=["change_speed", float(value)])
    dlgs["test"].speed_value.setText(f"{value}")


def table_update():
    keys = list(result_integrated.keys())
    columns_len = 0
    row_len = 0
    if keys != []:
        columns_len = len(keys) + 1
        row_len = len(result_integrated[keys[0]]) + 1
    dlgs["result"].ResultTable.setRowCount(row_len)
    dlgs["result"].ResultTable.setColumnCount(columns_len)
    for i in range(row_len):
        for j in range(columns_len):
            item = QTableWidgetItem("")
            if i == 0 and j == 0:
                pass
            elif i == 0:
                item = QTableWidgetItem(
                    keys[j-1]
                    )
            elif j == 0:
                item = QTableWidgetItem(f"{i}")
            else:
                try:
                    item = QTableWidgetItem(
                        result_integrated[keys[j-1]][i-1]
                        )
                except Exception:
                    pass
            dlgs['result'].ResultTable.setItem(i, j, item)


def run_thread(func, args=[]):
    # threadは1つまでにする❢
    # argsは def hoge(*args) しておく
    thread = threading.Thread(target=func, args=args)
    thread.setDaemon(True)
    thread.start()


def play():
    run_thread(P.setTask, args=["play", ])


def pause():
    run_thread(P.setTask, args=["pause", ])


def stop():
    run_thread(P.setTask, args=["stop", ])


def start_app():
    global config, now_view
    load_sounds()
    load_result()
    table_update()
    connect_objects()
    dlgs["menu"].show()
    now_view = dlgs["menu"]
    app.exec()


def load_sounds():
    global config, sounds
    cwd = os.getcwd()
    files = os.listdir(f"{cwd}/{os.path.dirname(__file__)}/sounds")
    sounds = []
    for file in files:
        if ".wav" in file:
            sounds.append(f"{cwd}/{os.path.dirname(__file__)}/sounds/{file}")
            dlgs["settings"].listWidget.addItem(f"{file}")
    config["num_sounds"] = len(sounds) - 1


def set_player():
    global P
    # if P is not None:
    #     stop()
    #     P.done()
    P = sound.Player(
        path=sounds[config['now_page']]
        )


def exit_app():
    global P
    if P is not None:
        P.done()
    sys.exit()


def value2var(value):
    return f"{0.5 + value / 100:.1f}"


def save2result(result):
    global result_integrated
    loads = {}
    with open(result_path, "r") as f:
        loads = json.load(f)
    saves = {}
    for key in result.keys():
        sound = sounds[key].split('/')[-1][:-4]
        if sound in loads.keys():
            saves[sound] = loads[sound]
        else:
            saves[sound] = []
        saves[sound].append(result[key])

    with open(result_path, "w") as f:
        json.dump(saves, f)
    result_integrated = saves


def load_result():
    global result_integrated
    with open(result_path, "r") as f:
        loads = json.load(f)
    result_integrated = loads


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
    dlgs["test"].page_num.setText(
        f"{config['now_page']}/{config['num_sounds']}"
        )

    # fin
    dlgs["fin"].GoMenuButton.clicked.connect(GoMenu)

    # Result
    dlgs["result"].backButtonR.clicked.connect(Back)
    dlgs["result"].ResetButton.clicked.connect(ResetResults)

    # Settings
    dlgs["settings"].backButtonS.clicked.connect(Back)
    dlgs["settings"].NumFiles.setText(str(config["num_sounds"] + 1))
    dlgs["settings"].NumFiles.setReadOnly(True)


# 実行
if __name__ == "__main__":
    start_app()
