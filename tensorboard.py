import win32clipboard
import os
import socket
import subprocess


class Tensorboard(object):

    def make(paths, names=None, host='127.0.0.1', port='6006', output=True, start=False, sep=' '):
        assert isinstance(paths, list), 'Paths not type list'
        assert isinstance(names, list) or isinstance(names, type(None)), 'Names not type list or None'
        command = 'tensorboard'
        command += ' '

        if not names:
            names = [None for _ in range(len(paths))]

        is_first = True
        for name, path in zip(names, paths):
            if is_first:
                command += '--logdir' + sep
                is_first = False
            else:
                command += ','
            if name:
                command += name + ':'
            command += path

        if host:
            command += ' '
            command += '--host' + sep + host

        if port:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            is_port_open = sock.connect_ex((host, int(port)))
            new_port = port
            while not is_port_open:
                if output:
                    print('> Port {} in use'.format(new_port))
                new_port = str(int(new_port)+1)
                is_port_open = sock.connect_ex((host, int(new_port)))
            if port not in new_port and output:
                print('> Using port {}'.format(new_port))

            command += ' '
            command += '--port' + sep + new_port

        if output:
            print('> {}'.format(command))

        if start:
            Tensorboard.start(command)

        return command

    def start(command):
        host = Tensorboard._find(command, 'host')
        port = Tensorboard._find(command, 'port')

        print('> Starting Tensorboard at: {}:{}'.format(host, port))

        tb = subprocess.Popen(command,
                              stdout=subprocess.PIPE)
        # os.system(command)

    def _find(input, what):
        what += ' '
        pos1 = input.find(what) + len(what)
        length = input[pos1:].find(' ')
        return input[pos1:] if length is -1 else input[pos1:pos1+length]


if __name__ == '__main__':

    tensorboard_paths = [r'C:\Users\parth\Documents\GitHub\Facial-Recognition\tmp\tensorboard\013',
                         r'C:\Users\parth\Documents\GitHub\Facial-Recognition\tmp\tensorboard\014']
    tensorboard_names = ['full-images', 'augment-images']
    cmd = Tensorboard.make(paths=tensorboard_paths,
                           names=tensorboard_names,
                           host='127.0.0.1',
                           port='6006',
                           output=True,
                           start=False)
    print(cmd)
