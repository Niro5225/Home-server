import os,socket,pyautogui,time,subprocess,multiprocessing,sys,tqdm,argparse
from rich import print as rprint
from rich.panel import Panel
import colorama
from server_config import serv_conf
from pymsgbox import prompt
from sys import argv
colorama.init(autoreset=True)


class server():
    def __init__(self,back_dor_mode=False):
        self.server_run=True
        self.back_dor_mode=back_dor_mode
        self.user_root=False
        self.settings=serv_conf()
        self.settings.read_conf()
        self.SEPARATOR="<SEPARATOR>"
        self.BUFFER_SIZE=1024*4
        self.file_path="files/doc/"
        if self.settings.CONFIGS[2]=="1":
            self.g_path="G:\\"
        if len(sys.argv)>1:
            if sys.argv[1]=="server":
                self.__start_server()
                return
        while True:
            rprint(Panel('''
[1]:Edit serv conf
[2]:Start server
[0]:exit
            ''',title="CHOSE OPTION"))

            choose=input(colorama.Fore.RED+">>")
            if choose=='1':
                self.settings.set_conf()
                self.settings.read_conf()
            elif choose=="2":
                self.__start_server()
                break
            elif choose=="0":
                return


    def __perm_den(self):
        self.client.send("Permitions denide".encode('utf-8'))

    def __send_file(self):
        if self.user_root:
            self.client.send(f"start_acc_file {self.filename}".encode())
            # mes=self.client.recv(1024).decode()
            # if mes=="get my ip":
            #     self.client.send(self.client_ip[0])
            file_client=socket.socket()
            #self.send_ip="192.168.0.107"
            file_client.connect((self.client_ip[0],9696))

            try:
                with open(self.filename,'rb') as f:
                    file_data=f.read(1024)

                    while file_data:
                        file_client.send(file_data)
                        file_data=f.read(1024)
                    f.close()
            except:
                file_client.close()
                self.client.send("File not found".encode())
                return
            file_client.close()
        else:
            self.__perm_den()


    def __acc_file(self):
        self.client.send(f'start file get {self.filename}'.encode())
        filnam=self.filename.split(sep="\\")
        clear_filename=filnam[-1]
        file_server=socket.socket()
        file_server.bind((self.IP,6556))
        file_server.listen(1)
        file_client, file_client_addr=file_server.accept()
        print("connect")

        with open(self.file_path+clear_filename,'wb') as f:
            file_data=file_client.recv(1024)

            while file_data:
                f.write(file_data)
                file_data=file_client.recv(1024)
            f.close()
        file_server.close()

        self.client.send("file get done".encode())



    def __command_work(self,command):
        if command=="exit" or command=="ex":
            self.user_root=False
            self.client.send(command.encode('utf-8'))
            print(colorama.Fore.GREEN+"Client "+colorama.Fore.RED+str(self.client_ip[0])+" exit")
            self.__start_server()
            #self.server_run=False
        elif command=="root" or command=="rt":
            if self.settings.CONFIGS[0]=="1\n":
                self.client.send("enter_root_password".encode('utf-8'))
            elif self.settings.CONFIGS[0]=="0\n":
                self.client.send("set_root_user".encode('utf-8'))
                self.user_root=True
        elif command==self.settings.CONFIGS[1][0:8]:
            self.user_root=True
            self.client.send("set_root_user".encode('utf-8'))
        elif command=="shutdown" or command=="sh":
            self.client.send("exit".encode('utf-8'))
            self.sock.close()
            self.server_run=False
            os.system('shutdown /s /t 0')
        elif command=="help":
            if not self.user_root:
                help='''
[1]:help
[2]:root/rt
[3]:Read fil filename
[4]:serv off / server off
[0]:exit
                
                '''
                self.client.send(help.encode('utf-8'))
            elif self.user_root:
                help = '''
ROOT
[1]:help
[2]:root/rt
[3]:CR_F filepath filename
[4]:Read fil filepath filename
[5]:Rm file filepath filename \\beta
[6]:Edit configs / Ed cfg \\beta
[7]:root exit /exr
[8]:chk cfg
[9]:serv off / server off
[10]:get file filepath filename

[0]:exit
                
                '''
                self.client.send(help.encode('utf-8'))
        elif command=="root exit" or command=="exit root" or command=="exr":
            self.user_root=False
            self.client.send("not root".encode('utf-8'))
        elif command[0:4]=="CR_F":
            if self.user_root:
                self.filename=command[5:]
                self.client.send(("wr_f "+self.filename).encode('utf-8'))
            else:
                self.__perm_den()
        elif command[0:7]=="fil_txt":
            print(self.filename)
            file_text=command[8:]
            with open(self.filename,'w') as f:
                f.write(file_text)
                f.close()
            self.client.send(('file '+self.filename+" created").encode('utf-8'))
        elif command[0:9]=="Read file":
            self.filename=command[10:]
            try:
                with open(self.filename,'r') as f:
                    file_text=f.read()
                    f.close()
            except:
                self.client.send("file not found".encode('utf-8'))
            else:
                self.client.send(("show_file "+file_text).encode('utf-8'))
        elif command=="Edit configs" or command=="Edit config" or command=="Ed cfg":
            if self.user_root:
                self.client.send('''set_nw_cfg
Write new configs in a line (1,2,3,4)
if you want save deafault seting write dev (1,dev,3)
CONFIGS ORDER
1:Admin_pass
2:Admin_password
3:Set global path? (1 or 0)
                '''.encode('utf-8'))
            elif not self.user_root:
                self.__perm_den()
        elif command[0:7]=="Rm file":
            print("im here")
            self.filename=command[8:]
            subprocess.run(["DEL",'/Q','/F',self.filename])
        elif command[0:2]=="ls":
            try:
                path=command[3:]
                if len(path)>0:
                    l_files_arr=os.listdir(path)
                    l_files="\n"
                    for file in l_files_arr:
                        l_files+=file+"\n"
                    self.client.send(str(l_files).encode('utf-8'))
                else:
                    l_files_arr = os.listdir("G:\\programming\\python\\pycharm_proj\\server\\files\\doc")
                    l_files = "\n"
                    for file in l_files_arr:
                        l_files += file + "\n"
                    self.client.send(str(l_files).encode('utf-8'))
            except:
                self.client.send("Path Error".encode())


        elif command=="server off" or command=="off server" or command=="serv off":
            self.client.send("exit".encode('utf-8'))
            self.server_run=False
        elif command[0:8]=="upgr_cfg":
            upd_usr_cfg_str=command[9:]
            upd_usr_cfg_arr=upd_usr_cfg_str.split(sep=',')
            self.settings.set_conf(usr_set=upd_usr_cfg_arr)
            print(self.settings.CONFIGS)
            self.settings.read_conf()
            print(self.settings.CONFIGS)
        elif command=="chk cfg":
            if self.user_root:
                self.client.send(str(self.settings.CONFIGS).encode('utf-8'))
            else:
                self.__perm_den()
        elif command[0:8]=="get file":
            self.filename=command[9:]
            self.__send_file()
            self.client.send("OK".encode())
        elif command=="cls":
            for i in range(35):
                self.client.send("\n".encode())
        elif command=="":
            pass
        elif command[0:9]=="send file":
            print("im here")
            self.filename=command[10:]
            print(self.filename)
            self.__acc_file()
        elif command[0:5]=="mkdir":
            path=command[6:]
            spl_path=path.split(sep="\\")
            folder_name=spl_path[-1]
            os.system(f'mkdir {path}')
            self.client.send("Folder created".encode())





        else:
            self.client.send("Uncnown command".encode('utf-8'))



    def __start_server(self):
        if not self.back_dor_mode:
            hostname=socket.gethostname()
            self.IP=socket.gethostbyname(hostname)
        else:
            self.IP='127.0.0.1'
        print(colorama.Fore.GREEN+self.IP)
        PORT=6996
        self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.bind((self.IP,PORT))
        self.sock.listen(1)
        try:
            self.client, self.client_ip=self.sock.accept()
        except:
            return
        print(f'''
\tNEW CONECT
IP-{self.client_ip[0]}

        ''')
        #self.send_ip=prompt(title="Enter send serv ip",text="Enter ip")
        while self.server_run:
            user_mass=self.client.recv(1024).decode('utf-8')
            print(colorama.Fore.GREEN+"Client"+colorama.Fore.RED+">>"+user_mass)
            self.__command_work(user_mass)


if __name__ == '__main__':
    if len(argv)>1:
        print(argv[1])
        server(argv[1])
    else:
        server()
