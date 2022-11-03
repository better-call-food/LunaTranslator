import functools 

from PyQt5.QtWidgets import  QWidget,QLabel, QComboBox,QDoubleSpinBox 
 
from PyQt5.QtWidgets import QWidget,QLabel,QFrame ,QPushButton,QColorDialog
from PyQt5.QtGui import QColor,QFont
import functools
from utils.config import globalconfig 
import qtawesome
from utils.config import globalconfig 

import importlib
from gui.inputdialog import GetUserPlotItems
import gui.switchbutton
import gui.attachprocessdialog  
import gui.selecthook  
def setTab6(self) :
     
        self.tab_6 = QWidget()
        self.tab_widget.addTab(self.tab_6, "OCR设置") 

        label = QLabel(self.tab_6)
        self.customSetGeometry(label, 20, 250,230, 20)
        label.setText("使用竖排OCR(效果不佳)")
 
        self.verticalocr =gui.switchbutton.MySwitch(self.tab_6, sign= globalconfig['verticalocr'] )
        self.customSetGeometry(self.verticalocr, 250, 250, 20,20)
        self.verticalocr.clicked.connect(lambda x:globalconfig.__setitem__('verticalocr',x)) 

        label = QLabel(self.tab_6)
        self.customSetGeometry(label, 20, 280,230, 20)
        label.setText("每隔一段时间必然进行一次OCR")
 
        self.verticalocr =gui.switchbutton.MySwitch(self.tab_6, sign= globalconfig['mustocr'] )
        self.customSetGeometry(self.verticalocr, 250, 280, 20,20)
        self.verticalocr.clicked.connect(lambda x:globalconfig.__setitem__('mustocr',x)) 

        label = QLabel(self.tab_6)
        self.customSetGeometry(label, 20, 310,200, 20)
        label.setText("OCR最长间隔时间(s)")
 
        maxinterval =QDoubleSpinBox(self.tab_6  )
        maxinterval.setSingleStep(0.1)
        maxinterval.setValue(globalconfig['mustocr_interval']) 
        maxinterval.setDecimals(1)
        maxinterval.setMinimum(0.1)
        self.customSetGeometry(maxinterval, 220, 310, 50,20)
        maxinterval.valueChanged.connect(lambda x:globalconfig.__setitem__('mustocr_interval',x)) 

        
        label = QLabel(self.tab_6)
        self.customSetGeometry(label, 20, 340,200, 20)
        label.setText("OCR最短间隔时间(s)")
 
        maxinterval =QDoubleSpinBox(self.tab_6  )
        maxinterval.setSingleStep(0.1)
        maxinterval.setMinimum(0.1)
        maxinterval.setValue(globalconfig['ocrmininterval']) 
        maxinterval.setDecimals(1)
        self.customSetGeometry(maxinterval, 220, 340, 50,20)
        maxinterval.valueChanged.connect(lambda x:globalconfig.__setitem__('ocrmininterval',x)) 

        self.ocrswitchs={}
        initocrswitchs_auto(self)

def initocrswitchs_auto(self):
        num=0
        
        for ocr in globalconfig['ocr']:
            y=70+30*(num//3)
            x=20+220*(num%3)
            initocrswitchs(self,ocr,(x, y, 120, 20),(x+120, y, 20,20),0,(x+150, y, 20,20))
            num+=1
def yuitsuocr(self,name,checked): 
    
    if checked : 
        for k in self.ocrswitchs:
            if globalconfig['ocr'][k]['use']==True:
                 
                self.ocrswitchs[k].setChecked(False) 
                globalconfig['ocr'][k]['use']=False
        globalconfig['ocr'][name]['use']=True
    else:
        globalconfig['ocr'][name]['use']=False  

import os
def initocrswitchs(self,name,namepos,switchpos,colorpos,settingpos):
        if os.path.exists('./userconfig')==False:
            os.mkdir('./userconfig')
        label = QLabel(self.tab_6)
        self.customSetGeometry(label, *namepos)
        label.setText(globalconfig['ocr'][name]['name']+":")
        p=gui.switchbutton.MySwitch(self.tab_6, sign=globalconfig['ocr'][name]['use'], textOff='关闭',textOn='使用')
        
        self.customSetGeometry(p, *switchpos)
        
        
        p.clicked.connect(functools.partial( yuitsuocr,self,name))
        self.ocrswitchs[name]=p
        
        if 'argsfile' in globalconfig['ocr'][name]:
            s1 = QPushButton( "", self.tab_6)
            self.customSetIconSize(s1, 20, 20)
            self.customSetGeometry(s1, *settingpos)
            s1.setStyleSheet("background: transparent;") 
            
            s1.setIcon(qtawesome.icon("fa.gear", color="#FF69B4"  ))
            df=importlib.import_module('otherocr.'+name).default()
            s1.clicked.connect(lambda x:GetUserPlotItems(self,globalconfig['ocr'][name]['argsfile'],df,globalconfig['ocr'][name]['name']+'设置'))
     
      