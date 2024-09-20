import pwd
import tkinter as tk
from tarfile import TarFile
import sys


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

        self.current_dir = ""

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

        output = ""
        with TarFile(sys.argv[1], 'a') as filesystem:
            if command == 'ls':
                output = ""
                for i in filesystem.getnames():
                    output = output + i + "\n"
                output.removesuffix("\n")

            elif command == "whoami":
                output = filesystem.name.split('/')[-1].split('.')[0]

            elif command.startswith('cd '):
                path = command.split()[1]
                files = filesystem.getnames()
                files.append("")
                to_path = ""
                # Absolute
                if path[0] == '/':
                    to_path = path.removeprefix('/')
                # Relative
                else:
                    to_path = (self.current_dir + "/" + path).removeprefix('/')

                if to_path not in files:
                    output = "cd: No such file or directory: /" + to_path
                elif to_path.count('.') != 0:
                    output = "cd: Not a directory: /" + to_path
                else:
                    self.current_dir = to_path
            elif command.startswith('chown '):
                new_owner = command.split()[1]
                path_to_file = command.split()[2]
                try:
                    file = filesystem.getmember(path_to_file.removeprefix("/"))
                    file.uid = pwd.getpwnam(new_owner).pw_uid
                except KeyError:
                    output = "Error reading a file: " + path_to_file

                print(file)

            elif command == "pwd":
                output = '/' + self.current_dir

            elif command == "exit":
                self.quit()
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
