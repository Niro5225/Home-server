import subprocess
from rich.panel import Panel
from rich import print as rprint
import colorama
colorama.init(autoreset=True)


class serv_conf():
    def __init__(self):
        self.CONFIGS=[]

    def read_conf(self):
        self.CONFIGS.clear()
        with open("configs/conf.scfg",'r') as f:
            for params in f:
                self.CONFIGS.append(params)
        return self.CONFIGS
    def set_conf(self,**kwargs):
        try:
            settings=kwargs['usr_set']
        except:
            pass
        else:
            new_setings={"Admin_pass":"1","Admin_password":"1234","global_path":"0"}
            counter=0
            for set in new_setings:
                if settings[counter]=="dev":
                    pass
                else:
                    new_setings[set]=settings[counter]
                counter+=1
            print(new_setings)
            with open("configs/conf.scfg", 'w') as f:
                for setting in new_setings:
                    f.write(new_setings[setting] + "\n")
                f.close()
            return
        settings={"Admin_pass":"1","Admin_password":"1234","global_path":"0"}
        while True:
            rprint(Panel('''
1:Admin user password
2:Set admin password
3:Set global path
0:exit
            ''',title="CHOOSE PARAM",title_align="left"))
            choose=input(colorama.Fore.RED+">>")
            if choose=="1":
                settings["Admin_pass"]=input(colorama.Fore.GREEN+"Admin_pass"+colorama.Fore.RED+">>"+colorama.Fore.WHITE)
            elif choose=="2":
                settings["Admin_password"]=input(colorama.Fore.RED+"NEW Password >>")
            elif choose=="3":
                settings["global_path"]=input(colorama.Fore.RED+"Set global_path? >>")
            elif choose=="0":
                break
        with open("configs/conf.scfg",'w') as f:
            for setting in settings:
                f.write(settings[setting]+"\n")
            f.close()



if __name__=="__main__":
    cfg=serv_conf()
    print(cfg.read_conf())
    print(cfg.set_conf())
    print(cfg.read_conf())
