# coding: utf-8
import os
import abc

history = []


class Command(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def execute(self):
        pass

    @abc.abstractmethod
    def undo(self):
        pass


class LSCommand(Command):

    def __init__(self, receiver):
        self.receiver = receiver

    def execute(self):
        self.receiver.show_current_dir()

    def undo(self):
        pass


class LSReceiver(object):

    def show_current_dir(self):
        current_dir = './'

        filenames = []
        for name in os.listdir(current_dir):
            path = os.path.join(current_dir, name)
            if os.path.isfile(path):
                filenames.append(path)
        print 'Content of dirs %s' % (' '.join(filenames))


class TouchCommand(Command):

    def __init__(self, receiver):
        self.receiver = receiver

    def execute(self):
        self.receiver.create_file()

    def undo(self):
        self.receiver.delete_file()


class TouchReceiver(object):
    def __init__(self, name):
        self.name = name

    def create_file(self):
        with file(self.name, 'a'):
            os.utime(self.name, None)

    def delete_file(self):
        os.remove(self.name)


class RMCommand(Command):

    def __init__(self, receiver):
        self.receiver = receiver

    def execute(self):
        self.receiver.delete_file()

    def undo(self):
        self.receiver.undo()


class RMReceiver(object):
    def __init__(self, name):
        self.name = name
        self.backup_name = None

    def delete_file(self):
        self.backup_name = '.' + self.name
        os.rename(self.name, self.backup_name)

    def undo(self):
        name = self.backup_name[1:]
        os.rename(self.backup_name, name)
        self.backup_name = None


class Invoker(object):

    def __init__(self, create_file_commands, delete_file_commands):
        self.create_file_commands = create_file_commands
        self.delete_file_commands = delete_file_commands
        self.history = []

    def create_file(self):
        print 'Create file...'

        for command in self.create_file_commands:
            command.execute()
            self.history.append(command)
        print 'File created.\n'

    def delete_file(self):
        print 'Deleting file...'

        for command in self.delete_file_commands:
            command.execute()
            self.history.append(command)
        print 'File deleted.\n'

    def undo_all(self):
        print 'Undo all...'
        for command in reversed(self.history):
            command.undo()

        print 'Undo all finished.'


if __name__ == "__main__":
    ls_receiver = LSReceiver()
    ls_command = LSCommand(ls_receiver)

    touch_receiver = TouchReceiver('test_file')
    touch_command = TouchCommand(touch_receiver)
    rm_recevier = RMReceiver('test_file')
    rm_command = RMCommand(rm_recevier)

    create_file_commands = [ls_command, touch_command, ls_command]
    delete_file_commands = [ls_command, rm_command, ls_command]

    invoker = Invoker(create_file_commands, delete_file_commands)
    invoker.create_file()
    invoker.delete_file()
    invoker.undo_all()
