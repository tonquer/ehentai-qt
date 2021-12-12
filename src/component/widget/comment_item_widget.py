import re

from PySide2 import QtWidgets
from PySide2.QtCore import QEvent, Qt, QSize, QFile
from PySide2.QtGui import QPixmap, QIcon

from interface.ui_comment_item import Ui_CommentItem
from qt_owner import QtOwner
from tools.log import Log
from tools.str import Str


class CommentItemWidget(QtWidgets.QWidget, Ui_CommentItem):
    def __init__(self, parent):
        super(self.__class__, self).__init__(parent)
        Ui_CommentItem.__init__(self)
        self.setupUi(self)
        self.linkId = ""
        self.id = ""
        self.url = ""
        self.path = ""
        self.isGame = False

        self.picIcon.setCursor(Qt.CursorShape.PointingHandCursor)
        self.picIcon.setScaledContents(True)
        self.picIcon.setWordWrap(True)

        f = QFile(u":/png/icon/logo_round.png")
        f.open(QFile.ReadOnly)
        self.picIcon.SetPicture(f.readAll())
        f.close()

        self.pictureData = None
        self.headData = None
        self.picIcon.installEventFilter(self)
        self.commentLabel.setWordWrap(True)
        self.nameLabel.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
        self.commentLabel.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)

    def SetLike(self, isLike=True):
        p = QPixmap()
        if isLike:
            p.load(":/png/icon/icon_comment_liked.png")
        else:
            p.load(":/png/icon/icon_comment_like.png")
        nums = re.findall("\d+", self.starButton.text())
        if nums:
            num = int(nums[0]) + 1 if isLike else int(nums[0]) - 1
            self.starButton.setText("({})".format(str(num)))
        self.starButton.setIcon(QIcon(p.scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)))
        self.starButton.setChecked(isLike)

    def SetPicture(self, data):
        self.pictureData = data
        self.picIcon.SetPicture(self.pictureData, self.headData)

    def SetPictureErr(self):
        self.picIcon.setText(Str.GetStr(Str.LoadingFail))

    def SetHeadData(self, data):
        self.headData = data
        self.picIcon.SetPicture(self.pictureData, self.headData)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.MouseButtonPress:
            if event.button() == Qt.MouseButton.LeftButton:
                if obj == self.picIcon:
                    if self.pictureData:
                        QtOwner().OpenWaifu2xTool(self.pictureData)
                elif obj == self.linkLabel and self.linkId:
                    if self.isGame:
                        QtOwner().OpenGameInfo(self.linkId)
                    else:
                        QtOwner().OpenBookInfo(self.linkId)
                return True
            else:
                return False
        else:
            return super(self.__class__, self).eventFilter(obj, event)

    def OpenComment(self):
        QtOwner().OpenSubComment(self.id, self)

    def KillComment(self):
        try:
            if self.parent().parent().KillBack:
                self.parent().parent().KillBack(self.id)
        except Exception as es:
            Log.Error(es)
        return
