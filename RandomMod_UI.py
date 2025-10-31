from PySide2 import QtWidgets, QtCore, QtGui
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.cmds as cmds
from importlib import reload

try:
    from . import RandomMod_Util as util
    reload(util)
except (ImportError, SystemError):
    try:
        import RandomMod_Util as util
        reload(util)
    except ImportError as e:
        cmds.warning(f"Can't find 'RandomMod_Util' file! {e}")
        util = None

def get_maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    if main_window_ptr:
        return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)
    return None

class ToolWindow(QtWidgets.QDialog):
    def __init__(self, parent=get_maya_main_window()):
        super(ToolWindow, self).__init__(parent)
        
        self.setWindowTitle("Randomizer Tool")
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.Window)
        self.resize(320, 280) # A bit bigger

        self.setStyleSheet(COOL_STYLE_SHEET)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        # Use short variable names
        self.color_chk = QtWidgets.QCheckBox("Random Color")
        self.scale_chk = QtWidgets.QCheckBox("Random Scale")
        self.rot_chk = QtWidgets.QCheckBox("Random Rotation")
        self.pos_chk = QtWidgets.QCheckBox("Random Position")

        self.color_chk.setChecked(True)
        self.pos_chk.setChecked(True)
        
        self.separator = QtWidgets.QFrame()
        self.separator.setFrameShape(QtWidgets.QFrame.HLine)
        
        self.apply_chk = QtWidgets.QCheckBox("Apply to Selected Object")
        self.apply_chk.setChecked(True)

        self.go_btn = QtWidgets.QPushButton(" RANDOMIZE !")
        self.go_btn.setObjectName("RandomizeButton")
        self.go_btn.setIcon(QtGui.QIcon(":/SP_Rand.png"))
        self.go_btn.setIconSize(QtCore.QSize(20, 20))

    def create_layouts(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        options_group = QtWidgets.QGroupBox("OPTIONS")
        options_layout = QtWidgets.QVBoxLayout()
        options_layout.setSpacing(8) 
        options_layout.addWidget(self.color_chk)
        options_layout.addWidget(self.scale_chk)
        options_layout.addWidget(self.rot_chk)
        options_layout.addWidget(self.pos_chk)
        options_group.setLayout(options_layout)
        
        main_layout.addWidget(options_group)
        main_layout.addWidget(self.separator)
        main_layout.addWidget(self.apply_chk)
        main_layout.addStretch() # Push the button to the bottom
        main_layout.addWidget(self.go_btn)

    def create_connections(self):
        self.go_btn.clicked.connect(self.run_randomize)

    def run_randomize(self):
        # A "human" debug print
        print("!!! RANDOMIZE !!!")
        
        # Reload util in case we edited the backend
        try:
            reload(util)
        except Exception as e:
            cmds.warning(f"Couldn't reload util: {e}")
            return
            
        if not util:
            cmds.error("Can't call 'util'!")
            return
            
        # Read values from checkboxes
        c = self.color_chk.isChecked()
        s = self.scale_chk.isChecked()
        r = self.rot_chk.isChecked()
        p = self.pos_chk.isChecked()
        apply = self.apply_chk.isChecked()

        try:
            util.do_random(
                use_selection=apply,
                do_color=c,
                do_scale=s,
                do_rotation=r,
                do_position=p
            )
        except Exception as e:
            cmds.error(f"Crashed when running util: {e}")

class StartScreen(QtWidgets.QDialog):
    def __init__(self, parent=get_maya_main_window()):
        super(StartScreen, self).__init__(parent)
        
        self.setWindowTitle("Welcome")
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.Window)
        self.resize(350, 400)

        self.setStyleSheet(COOL_STYLE_SHEET)
        
        self.create_widgets()
        self.create_layouts()
        self.create_connections()
        
    def create_widgets(self):
        self.canvas_frame = QtWidgets.QFrame()
        self.canvas_frame.setObjectName("CanvasFrame")
        
        self.logo = QtWidgets.QLabel("RandomMod")
        self.logo.setObjectName("LogoText")
        
        canvas_layout = QtWidgets.QVBoxLayout(self.canvas_frame)
        canvas_layout.addStretch()
        canvas_layout.addWidget(self.logo)
        
        self.subtitle = QtWidgets.QLabel("Design is *inspired* by the sketch ;)")
        self.subtitle.setAlignment(QtCore.Qt.AlignCenter)
        self.subtitle.setStyleSheet("color: #888; font-style: italic;")
        canvas_layout.addWidget(self.subtitle)
        canvas_layout.addStretch()

        self.btn_start = QtWidgets.QPushButton("Start")
        self.btn_start.setObjectName("StartButton")
        self.btn_start.setIcon(QtGui.QIcon(":/taskManager.png"))
        
        self.btn_exit = QtWidgets.QPushButton("Exit")
        self.btn_exit.setObjectName("ExitButton")
        self.btn_exit.setIcon(QtGui.QIcon(":/cross.png"))

    def create_layouts(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        main_layout.addWidget(self.canvas_frame)
        
        # Horizontal layout for buttons
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.btn_exit)
        button_layout.addStretch(1) # Push buttons apart
        button_layout.addWidget(self.btn_start)
        
        main_layout.addLayout(button_layout)
        
    def create_connections(self):
        self.btn_start.clicked.connect(self.go_to_tool)
        self.btn_exit.clicked.connect(self.close)

    def go_to_tool(self):
        print("--- Start Button Pressed ---")
        open_tool_window()
        
        self.close()

splash_win = None
tool_win = None

def open_tool_window():
    global tool_win
    
    if tool_win is not None:
        try:
            tool_win.close()
            tool_win.deleteLater()
        except:
            pass 
            
    tool_win = ToolWindow()
    tool_win.show()

def run():
    global splash_win, tool_win
    
    if splash_win is not None:
        try:
            splash_win.close()
            splash_win.deleteLater()
        except:
            pass
            
    if tool_win is not None:
        try:
            tool_win.close()
            tool_win.deleteLater()
        except:
            pass
    
    splash_win = StartScreen()
    splash_win.show()