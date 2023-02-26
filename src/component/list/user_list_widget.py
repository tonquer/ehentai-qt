from functools import partial

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QListWidgetItem

from component.list.base_list_widget import BaseListWidget
from component.widget.comment_item_widget import CommentItemWidget
from config import config
from tools.status import Status
from tools.str import Str
from tools.tool import ToolUtil


class UserListWidget(BaseListWidget):
    def __init__(self, parent):
        BaseListWidget.__init__(self, parent)
        self.resize(800, 600)
        # self.setMinimumHeight(400)
        # self.setFrameShape(self.Shape.NoFrame)  # 无边框
        self.setFlow(self.Flow.TopToBottom)
        # self.setWrapping(True)
        # self.setResizeMode(self.ResizeMode.Adjust)
        # self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        # self.customContextMenuRequested.connect(self.SelectMenuBook)
        # self.doubleClicked.connect(self.OpenBookInfo)
        # self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setFrameShape(self.Shape.NoFrame)  # 无边框
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setStyleSheet("QListWidget::item { border-bottom: 1px solid black; }")

    def AddUserItem(self, name, content, floor, hideKillButton=False, likeCallBack=None):

        index = self.count()
        iwidget = CommentItemWidget(self)
        iwidget.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        iwidget.commentLabel.setText(content)
        iwidget.nameLabel.setText(name)

        iwidget.indexLabel.setText("{}".format(str(floor))+Str.GetStr(Str.Floor))
        iwidget.adjustSize()
        item = QListWidgetItem(self)
        item.setSizeHint(iwidget.sizeHint())
        item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
        self.setItemWidget(item, iwidget)

    def AddUserKindItem(self, info, floor):
        content = info.get("slogan", "")
        name = info.get("name")
        avatar = info.get("avatar", {})
        commnetId = info.get('_id', "")
        title = info.get("title", "")
        level = info.get("level", 1)
        character = info.get("character", "")
        if not avatar:
            url = ""
            path = ""
        elif isinstance(avatar, str):
            url = avatar
            path = ""
        else:
            url = avatar.get("fileServer", "")
            path = avatar.get("path", "")

        index = self.count()
        iwidget = CommentItemWidget(self)
        iwidget.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        iwidget.killButton.hide()
        iwidget.nameLabel.setCursor(Qt.CursorShape.PointingHandCursor)
        iwidget.nameLabel.installEventFilter(iwidget)
        iwidget.setToolTip(info.get("slogan", ""))
        iwidget.id = commnetId
        iwidget.dateLabel.hide()
        iwidget.starButton.setCheckable(False)
        iwidget.commentButton.hide()
        iwidget.commentLabel.setText(content)
        iwidget.nameLabel.setText(name)
        iwidget.starButton.setText("({})".format(info.get('comicsUploaded')))
        iwidget.levelLabel.setText(" LV" + str(level) + " ")
        iwidget.titleLabel.setText(" " + title + " ")
        iwidget.url = url
        iwidget.path = path
        iwidget.indexLabel.setText(Str.GetStr(Str.The)+"{}".format(str(floor)))

        item = QListWidgetItem(self)
        item.setSizeHint(iwidget.sizeHint())
        self.setItemWidget(item, iwidget)
        if url and config.IsLoadingPicture:
            self.AddDownloadTask(url, path, None, self.LoadingPictureComplete, True, index, True)
        if "pica-web.wakamoment.tk" not in character and config.IsLoadingPicture:
            self.AddDownloadTask(character, "", None, self.LoadingHeadComplete, True, index, True)

    def LoadingPictureComplete(self, data, status, index):
        if status == Status.Ok:
            item = self.item(index)
            widget = self.itemWidget(item)
            widget.SetPicture(data)
            pass
        else:
            item = self.item(index)
            widget = self.itemWidget(item)
            widget.SetPictureErr(status)
        return

    def LoadingHeadComplete(self, data, status, index):
        if status == Status.Ok:
            item = self.item(index)
            widget = self.itemWidget(item)
            widget.SetHeadData(data)
            pass
        else:
            pass
        return