import sys
import gtk

import Login
import gui
import utils
import MainWindow
import MainConversation

class Window(gtk.Window):
    
    def __init__(self, cb_on_close, height=450, width=250):
        gtk.Window.__init__(self)

        self.set_default_size(width, height)
        self.set_title("emesene")
        self.set_icon(gui.theme.logo)

        self.cb_on_close = cb_on_close

        self.connect("delete-event", self._on_delete_event)
        self.connect('key-press-event', self._on_key_press)
        self.content = None

        self.content_type = 'empty'

    def set_icon(self, icon):
        '''set the icon of the window'''
        if utils.file_readable(icon):
            gtk.Window.set_icon(self, 
                utils.safe_gtk_image_load(icon).get_pixbuf())

    def clear(self):
        if self.get_child():
            self.remove(self.get_child())
            self.content = None

    def go_login(self, callback, account=None):
        # TODO: load the mails from a file
        self.content = Login.Login(['foo@bar.com', 'bar@bar.com'], 
            callback, account)
        self.add(self.content)
        self.content.show()
        self.content_type = 'login'

    def go_main(self, session, on_new_conversation, on_close):
        '''change to the main window'''
        self.content = MainWindow.MainWindow(session, on_new_conversation,
            on_close)
        self.add(self.content)
        self.content.show()
        self.content_type = 'main'

    def go_conversation(self, session):
        '''change to a conversation window'''
        self.content = MainConversation.MainConversation(session)
        self.add(self.content)
        self.content.show()
        self.content_type = 'conversation'

    def _on_delete_event(self, widget, event):
        '''call the cb_on_close callback, if the callback return True
        then dont close the window'''
        return self.cb_on_close()

    def _on_key_press(self, widget, event):
        '''called when a key is pressed on the window'''
        if self.content_type == 'main':
            self.content._on_key_press(widget, event)

def test():
    def callback(account, remember):
        print account.account
        print account.password
        print remember

    def on_close():
        sys.exit(0)

    window = Window(on_close)
    window.go_login(callback)
    window.show()
    gtk.main()

if __name__ == "__main__":
    test()
