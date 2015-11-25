import argparse
import npyscreen

class TextEditor(npyscreen.NPSAppManaged):
    def onStart(self):
        self.registerForm("MAIN",MainForm())


class MainForm(npyscreen.Form):
    def create(self):
        self.add(npyscreen.TitleText, name="Text: ", value="Hello World!")

    def afterEditing(self):
        self.parentApp.setNextForm(None)

if __name__ == "__main__":
    TextEditor().run()
