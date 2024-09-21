from pwd import getpwnam
import getpass
import tkinter as tk
from tarfile import TarFile
import sys


class Emulator:
    def __init__(self, filesystem: TarFile):
        self.current_dir = ""
        self.filesystem = filesystem

    def __del__(self):
        self.filesystem.close()

    def ls(self) -> str:
        output = ""
        for i in self.filesystem.getnames():
            output = output + i + "\n"
        output = output.strip()
        print(output)
        return output

    def whoami(self) -> str:
        # output = self.filesystem.name.split('/')[-1].split('.')[0]
        output = getpass.getuser()
        return output

    def cd(self, command: str) -> str:
        files = self.filesystem.getnames()
        files.append("")
        try:
            path = command.split()[1]
        except IndexError:
            return "cd: Provide additional arguments"

        if path[0] == '/':
            # Absolute
            to_path = path.removeprefix('/')
        else:
            # Relative
            to_path = (self.current_dir + "/" + path).removeprefix('/')

        if to_path not in files:
            output = "cd: No such file or directory: /" + to_path
        elif to_path.count('.') != 0:
            output = "cd: Not a directory: /" + to_path
        else:
            output = ""
            self.current_dir = to_path
        return output

    def chown(self, command) -> str:
        try:
            new_owner = command.split()[1]
            path_to_file = command.split()[2]
        except IndexError:
            return "chown: Provide additional arguments"
        output = ""
        try:
            file = self.filesystem.getmember(path_to_file.removeprefix("/"))
            file.uid = getpwnam(new_owner).pw_uid
        except KeyError:
            output = "Error reading a file: " + path_to_file

        return output

    def pwd(self) -> str:
        output = '/' + self.current_dir
        return output

    def command_parse(self, command: str) -> str:
        output = ""
        if command == 'ls':
            output = self.ls()

        elif command == "whoami":
            output = self.whoami()

        elif command.split()[0] == "cd":
            output = self.cd(command)

        elif command.split()[0] == "chown":
            output = self.chown(command)

        elif command == "pwd":
            output = self.pwd()

        elif command == "exit":
            sys.exit()
        else:
            output = "Unknown command: " + command
        return output


class ConsoleText(tk.Text):
    def __init__(self, master=None, **kw):
        tk.Text.__init__(self, master, **kw)
        self.insert('1.0', '$ ') # first prompt
        # create input mark
        self.mark_set('input', 'insert')
        self.mark_gravity('input', 'left')
        # create proxy
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)
        # binding to Enter key
        self.bind("<Return>", self.enter)

        self.emulator = Emulator(TarFile(sys.argv[1], 'a'))

    def _proxy(self, *args):
        largs = list(args)

        if args[0] == 'insert':
            if self.compare('insert', '<', 'input'):
                # move insertion cursor to the editable part
                self.mark_set('insert', 'end')  # you can change 'end' with 'input'
        elif args[0] == "delete":
            if self.compare(largs[1], '<', 'input'):
                if len(largs) == 2:
                    return # don't delete anything
                largs[1] = 'input'  # move deletion start at 'input'
        result = self.tk.call((self._orig,) + tuple(largs))
        return result

    def enter(self, event):
        command = self.get('input', 'end').strip()
        # execute code

        output = self.emulator.command_parse(command)

        # display result and next promp
        self.insert('end', f"\n{output}\n$ ")
        # move input mark
        self.mark_set('input', 'insert')
        return "break" # don't execute class method that inserts a newline


if __name__ == "__main__":
    root = tk.Tk()
    tfield = ConsoleText(root, bg='gray10', fg='white', insertbackground='white')
    tfield.pack()
    root.mainloop()
