import getpass

from main import Emulator
from tarfile import TarFile


def test_ls():
    sample = """filesys
filesys/2.txt
filesys/1.txt
filesys/vfg
filesys/vfg/conf.conf"""

    ls = Emulator(TarFile("archive.tar", 'a')).command_parse("ls")
    assert ls == sample


def test_pwd_cd():
    emulator = Emulator(TarFile("archive.tar", 'a'))

    pwd1 = emulator.command_parse("pwd")
    emulator.command_parse("cd filesys")
    pwd2 = emulator.command_parse("pwd")
    emulator.command_parse("cd vfg")
    emulator.command_parse("cd /")
    pwd3 = emulator.command_parse("pwd")
    assert pwd1 == "/"
    assert pwd2 == "/filesys"
    assert pwd3 == "/"


def test_whoami():
    whoami = Emulator(TarFile("archive.tar", 'a')).command_parse("whoami")
    assert whoami == getpass.getuser()
