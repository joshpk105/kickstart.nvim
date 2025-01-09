import pynvim
import os
import platform
import re
import subprocess

class MacController:
    def __init__(self):
        script = """
set appName to "hackmud"
set termName to "Terminal"
if application appName is running then
    tell application id (id of application appName)
        activate
    end tell
    delay 0.5
    tell application "System Events"
        keystroke "{}"
        delay 0.5
        keystroke return
    end tell
    delay 0.5
    tell application id (id of application termName)
        activate
    end tell
end if
""".split("\n")
        self.script = ["osascript"]
        for l in script:
            self.script.append("-e")
            self.script.append("{}".format(l))

    def run(self, cmd: str, stay=False):
        cmds = self.script.copy()
        cmds[20] = cmds[20].format(cmd)
        if stay:
            cmds = cmds[0:27]+cmds[-4:-2]
        return subprocess.run(cmds, capture_output=True, text=True)

@pynvim.plugin
class Hackmud(object):
    def __init__(self, vim: pynvim.Nvim):
        self.vim = vim
        self.controller = MacController()

    @pynvim.command("Hackmud", nargs="*", sync=False)
    def hackmud_command(self, args: list):
        result = None
        if args[-1] == "stay":
            result = self.controller.run(" ".join(args[0:-1]), stay=True)
        else:
            result = self.controller.run(" ".join(args))
        if result.returncode != 0:
            raise RuntimeError(result)

    @pynvim.autocmd("BufRead", pattern="*/hackmud/chat.txt", eval='expand("<afile>")', sync=True)
    def hackmud_chat_autocmd(self, filename):
        self.vim.command("set noreadonly")
        self.vim.command("set ma")
        self.vim.command("set mod")
        for i in range(len(self.vim.current.buffer)):
            self.vim.current.buffer[i] = re.sub("<[^>]+>", "", self.vim.current.buffer[i])
        self.vim.command("set readonly")
        self.vim.command("set noma")
        self.vim.command("set nomod")

    @pynvim.autocmd("BufRead", pattern="*/hackmud/shell.txt", eval='expand("<afile>")', sync=True)
    def hackmud_shell_autocmd(self, filename):
        self.vim.command("set noreadonly")
        self.vim.command("set ma")
        self.vim.command("set mod")
        for i in range(len(self.vim.current.buffer)):
            self.vim.current.buffer[i] = re.sub("<[^>]+>", "", self.vim.current.buffer[i])
        self.vim.command("set readonly")
        self.vim.command("set noma")
        self.vim.command("set nomod")
