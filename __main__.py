import os
from Quartz import (
    CGEventTapCreate, kCGHeadInsertEventTap, kCGEventKeyDown, 
    kCGEventTapOptionListenOnly, kCFRunLoopDefaultMode,
    CGEventMaskBit, CFRunLoopAddSource, CFRunLoopRun, CFRunLoopSourceInvalidate
)
import Quartz
import requests
import json
import pyautogui

class Keylogger:
    def __init__(self):
        self.input_buffer = ""

    def callback(self, proxy, event_type, event, refcon):
        if event_type == kCGEventKeyDown:
            key_code = Quartz.CGEventGetIntegerValueField(event, Quartz.kCGKeyboardEventKeycode)
            _, key_string = Quartz.CGEventKeyboardGetUnicodeString(event, 10, None, None)

            if key_string == ".":
                self.process_input(self.input_buffer)
                self.input_buffer = ""
            else:
                self.input_buffer += key_string

        return event



    def process_input(self, input_text):
        full_text = self.send_to_llm(input_text)
        print(full_text)

        # AppleScript to delete the typed text and type the response from the server
        script = f'''
        tell application "System Events"
            repeat {len(input_text)} times
                key code 51  -- Simulate pressing the delete key
            end repeat
            keystroke "{full_text}"  -- Type the response from the server
        end tell
        '''

        # Run the AppleScript
        os.system(f"osascript -e '{script}'")

    def send_to_llm(self, input_text):
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "prompt": input_text,
                "model": "llama3",
                "stream": False,
                "system": "You are an advanced language model configured to expand text input where users type a few letters of each word in a phrase. If the input has x number of words, your response should have x number of words. Words that are smaller might have fewer words than longer ones. Under no circumstances should you reply, converse, comment, or provide any feedback to the user. Do not acknowledge receipt of the message or provide any explanation. Any additional output is strictly prohibited. Use common completions to attempt to understand what the user wants to type. \n ### Example #1: I wnt to the bkry ystdy to buy brd. \n I went to the bakery yesterday to buy bread. \n #2 Tht ws rlly gd! \n That was really good!\n"
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