from Quartz import (
    CGEventTapCreate, kCGEventKeyDown, 
    kCGEventTapOptionListenOnly, kCFRunLoopDefaultMode,
    CGEventMaskBit, CFRunLoopAddSource, CFRunLoopRun
)
import Quartz
import requests
import json
import pyperclip

class Keylogger:

    def callback(self, proxy, event_type, event, refcon):
        if event_type == kCGEventKeyDown:
            key_code = Quartz.CGEventGetIntegerValueField(event, Quartz.kCGKeyboardEventKeycode)
            flags = Quartz.CGEventGetFlags(event)
            command_down = flags & Quartz.kCGEventFlagMaskCommand

            if key_code == 8 and command_down:  # Command+C was pressed
                clipboard_content = pyperclip.paste()
                if clipboard_content and "!" in clipboard_content and "." in clipboard_content:
                    command_start = clipboard_content.index("!") + 1
                    command_end = clipboard_content.index(".")
                    command = clipboard_content[command_start:command_end].strip()
                    text = clipboard_content.replace('!' + command + '.', '').strip()
                    self.process_input(text, command)

        return event

    def process_input(self, text, command):
        print("processing input")
        full_text = self.send_to_llm(text, command)
        print(full_text)

        # Add the response to the clipboard
        pyperclip.copy(full_text)

    def send_to_llm(self, text, command):
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "prompt": f"{command}: {text}",
                "model": "llama3",
                "stream": False,
                "context": [0],
                "system": "You are an advanced language model configured to assist with text input. When the user types a phrase, you should process the text between performing the requested action. You should not reply, converse, comment, or provide any feedback to the user unless explicitly requested in the command. Do not acknowledge receipt of the message or provide any explanation unless asked to do so. Any additional output is strictly prohibited. \n ### Example #1: Translate to French: I like apples \n J'aime des pommes \n #2 Rewrite using other words: Hello, people! \n Hey, guys!\n"
            }
        )
        response.raise_for_status()  # Raise an exception if the request failed
        json_responses = [json.loads(line) for line in response.content.decode().splitlines()]
        return json_responses[0]["response"]


    def run(self):
        event_mask = (CGEventMaskBit(kCGEventKeyDown))
        event_tap = CGEventTapCreate(
            Quartz.kCGSessionEventTap, Quartz.kCGTailAppendEventTap,
            kCGEventTapOptionListenOnly, event_mask, self.callback, None
        )
        run_loop_source = Quartz.CFMachPortCreateRunLoopSource(None, event_tap, 0)
        CFRunLoopAddSource(
            Quartz.CFRunLoopGetCurrent(), run_loop_source, kCFRunLoopDefaultMode
        )
        Quartz.CGEventTapEnable(event_tap, True)
        CFRunLoopRun()

if __name__ == "__main__":
    keylogger = Keylogger()
    keylogger.run()