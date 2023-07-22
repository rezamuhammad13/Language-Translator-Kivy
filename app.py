import os
from kivy import Config
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.core.window import Window
import googletrans
from googletrans import Translator
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.core.clipboard import Clipboard
from gtts import gTTS
from playsound import playsound
from pathlib import Path


class ReTranslate(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        self.window = GridLayout(spacing=10)
        self.window.cols = 1
        self.window.size_hint = (0.8, 0.85)
        self.window.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        Window.set_icon('retranslate.ico')
        Config.set('kivy', 'window_icon', 'retranslate.ico')

        # # create a logo
        # self.logo = Image(source="images/retranslate.png", size_hint= [1,2.5], pos_hint ={'x':-0.05, 'y':.001 })

        # create language list
        self.languages = googletrans.LANGUAGES
        self.language_list = ["indonesian", "english", "french", "filipino", "dutch",
                              "thai", "russian", "portuguese", "myanmar", "malay", "korean",
                              "khmer", "italian", "japanese", "hindi", "german"]

        # create dropdown in length of language list
        dropdown = DropDown()
        for index in range(len(self.language_list)):
            # adding button in drop down list
            btn = Button(text=str(self.language_list[index].capitalize()), size_hint_y=None, height=40)
            btn.background_color = 255, 255, 255
            btn.color = 'grey'

            # binding the button to show the text when selected
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))

            # add the button inside the dropdown
            dropdown.add_widget(btn)

        # create a source language button
        self.source_language = Button(text='Indonesian', size_hint =(1, 0.3), height=40, pos_hint ={'x':-0.45, 'y':.1 })
        self.source_language.background_color = 0, 0, 0, 0
        self.source_language.color = 'black'
        self.source_language.underline = True
        self.source_language.bold = True

        # show the dropdown menu when the source button is release
        self.source_language.bind(on_release=dropdown.open)

        # dropdown list assign the data to source language button text
        dropdown.bind(on_select=lambda instance, x: setattr(self.source_language, 'text', x))

        # create float layout for source button
        self.source_layout = FloatLayout()
        self.source_layout.add_widget(self.source_language)

        # create text input widget
        self.input = TextInput(size_hint =(.2, 2.7))
        self.input.hint_text = "Select any text on the page, or type it right here.."
        self.input.hint_text_color = "grey"
        self.input.background_color = 0, 0, 0, 0.025
        self.input.font_name = "Arial"

        # create a translate button
        self.translate = Button(text="Translate", size_hint_y=None, height=40,
                                bold=True,
                                background_color='#bf2121',
                                background_normal="",
                                markup=True,
                                )

        # bind translate button to translate the text
        self.translate.bind(on_press=self.translate_text)

        # create dropdown in length of language list
        dropdown_d = DropDown()
        for index in range(len(self.language_list)):
            # adding button in drop down list
            btn = Button(text=str(self.language_list[index].capitalize()), size_hint_y=None, height=40, )
            btn.background_color = 255, 255, 255
            btn.color = 'grey'

            # binding the button to show the text when selected
            btn.bind(on_release=lambda btn: dropdown_d.select(btn.text))

            # add the button inside the dropdown
            dropdown_d.add_widget(btn)

        # create a dropdown to destination language
        self.dest_language = Button(text='English', size_hint =(1, 0.3), height=40, pos_hint ={'x':-0.45, 'y':.1 } )
        self.dest_language.background_color = 0, 0, 0, 0
        self.dest_language.color = 'black'
        self.dest_language.underline = True
        self.dest_language.bold = True

        # show the dropdown menu when the destination button is release
        self.dest_language.bind(on_release=dropdown_d.open)

        # dropdown list assign the data to destination button text
        dropdown_d.bind(on_select=lambda instance, x: setattr(self.dest_language, 'text', x))

        # create float layout for destination language
        self.destination_layout = FloatLayout()
        self.destination_layout.add_widget(self.dest_language)

        # create text output widget
        self.output = TextInput(size_hint =(.2, 2.7))
        self.output.readonly = True
        self.output.hint_text = "...then press translate to see the translation"
        self.output.hint_text_color = "grey"
        self.output.background_color = 0, 0, 0, 0.025
        self.output.font_name = "Arial"

        # create copy button
        self.copy_button = Button(text='copy', size_hint =(.01, 0.3), height=20, pos_hint ={'x':.001, 'y':.7 },)
        self.copy_button.background_color = 0, 0, 0, 0
        self.copy_button.color = 'grey'
        self.copy_button.bind(on_press=self.copy_text)
        self.copy_button.bind(on_release=self.copied_text)

        # create voice button
        self.voice_button = Button(text="voice",size_hint =(.012, 0.3), height=20, pos_hint ={'x':.1, 'y':.7 },)
        self.voice_button.background_color = 0, 0, 0, 0
        self.voice_button.color = 'grey'
        self.voice_button.bind(on_press=self.voice_text)

        # create clear button
        self.clear_button = Button(text="clear", size_hint =(.013, 0.3), height=20, pos_hint ={'x':.2, 'y':.7 }, )
        self.clear_button.background_color = 0, 0, 0, 0
        self.clear_button.color = 'grey'
        self.clear_button.bind(on_press=self.clear_all)

        # create box layout for copy,voice,and clear button
        button_lay = BoxLayout(orientation='horizontal',size_hint =(.01, .3))
        button_lay.add_widget(self.copy_button)
        button_lay.add_widget(self.voice_button)
        button_lay.add_widget(self.clear_button)

        # add widgets to window
        # self.window.add_widget(self.logo)
        self.window.add_widget(self.source_layout)
        self.window.add_widget(self.input)
        self.window.add_widget(self.translate)
        self.window.add_widget(self.destination_layout)
        self.window.add_widget(self.output)
        self.window.add_widget(button_lay)

        return self.window

    # create a function to translate text after button translate clicked
    def translate_text(self, event):
        source = self.source_language.text
        source = source.lower()
        destination = self.dest_language.text
        destination = destination.lower()
        user_input = self.input.text

        try:
            # Get the languages from dictionary keys
            # get the from language key
            for key, value in self.languages.items():
                if (value == source):
                    from_language_key = key
                    print(from_language_key)

            for key, value in self.languages.items():
                if (value == destination):
                    self.to_language_key = key
                    print(self.to_language_key)

            translator = Translator()
            output = translator.translate(text=user_input, src=from_language_key, dest=self.to_language_key)

            print(output)

            self.output.text = output.text

        except:
            print("cant connect ")

    # create a function to copy text to clipboard
    def copy_text(self, event):
        copy_text = self.output.text
        self.copy_button.text = "copied"
        Clipboard.copy(copy_text)

    # create a release function after text success copied
    def copied_text(self, event):
        self.copy_button.text = "copy"

    # create a function to clear input and outpun line edit
    def clear_all(self, event):
        self.output.text = ""
        self.input.text = ""

    # creata a function to convert output text to voice
    def voice_text(self, event):
        # try:
        mytext = self.output.text
        language = self.to_language_key
        text_speech = gTTS(text=mytext, lang=language, slow=False)
        text_speech.save("ReTranslateVoice.mp3")
        audio = str(Path().cwd() / "ReTranslateVoice.mp3")
        playsound(audio,True)
        print("after")
        os.remove(audio)

        # except:
        #     print("error text to voice")


if __name__ == "__main__":
    ReTranslate().run()
