import os
import sys
import time
from sqlite3 import connect, Error


def welcome_screen() -> str:
    print("""\033[5;37;40m
    $$$$$$$\                                                     $$\          
    $$  __$$\                                                    $$ |         
    $$ /  $$ | $$$$$$$\  $$$$$$$\  $$$$$$\  $$\   $$\ $$$$$$$\ $$$$$$\        
    $$$$$$$$ |$$  _____|$$  _____|$$  __$$\ $$ |  $$ |$$  __$$\\\\_$$_|       
    $$  __$$ |$$ /      $$ /      $$ /  $$ |$$ |  $$ |$$ |  $$ | $$ |         
    $$ |  $$ |$$ |      $$ |      $$ |  $$ |$$ |  $$ |$$ |  $$ | $$ |$$\      
    $$ |  $$ |\$$$$$$$\ \$$$$$$$\ \$$$$$$  |\$$$$$$  |$$ |  $$ | \$$$$  |     
    \__|  \__| \_______| \_______| \______/  \______/ \__|  \__|  \____/      
    
    $$$$$$\$$$$\   $$$$$$\  $$$$$$$\   $$$$$$\   $$$$$$\   $$$$$$\   $$$$$$\  
    $$  _$$  _$$\  \____$$\ $$  __$$\  \____$$\ $$  __$$\ $$  __$$\ $$  __$$\ 
    $$ / $$ / $$ | $$$$$$$ |$$ |  $$ | $$$$$$$ |$$ /  $$ |$$$$$$$$ |$$ |  \__|
    $$ | $$ | $$ |$$  __$$ |$$ |  $$ |$$  __$$ |$$ |  $$ |$$   ____|$$ |      
    $$ | $$ | $$ |\$$$$$$$ |$$ |  $$ |\$$$$$$$ |\$$$$$$$ |\$$$$$$$\ $$ |      
    \__| \__| \__| \_______|\__|  \__| \_______| \____$$ | \_______|\__|      
    find -username <value>                      $$\   $$ |  v1.0.0 Beta                  
    find -username <value>                      \$$$$$$  |  made with                  
    change -password -url e.x  <value>           \______/   l♥‿♥ e                
    change -url <old_url> <new_url>                         github:
    type 'cls' to clear screen.                             islam-kamel
                                                            
    This is Beta Version Thank you.
    01101101 01100001 01100100 01100101  01110111 01101001 01110100 01101000 0                                           
    \033[0;37;40m\n""")


def input_line(msg=' '):
    return input("\033[1;35;40m💀:{}".format(msg))


def print_line_emoji(msg=' ', end='\n'):
    print("\033[1;35;40m💀:{}".format(msg), end=end)


def connect_db() -> object:
    path = r"{}\account_manager.db".format(os.environ['USERPROFILE'])
    db = connect(path, uri=True)
    return db


def success(msg):
    print("\033[1;32;40m{}".format(msg))


def failed(msg=None):
    default = "Your account not exists or There is a mistake\n" \
              "in connecting with the database."
    if not msg:
        print("\033[0;31;47m{}".format(default).strip())
    print("\033[0;31;47m{}".format(msg).strip())


class Account:
    __db = connect_db()
    __cursor = __db.cursor()


    def __init__(self):
        self.__username = None
        self.__email = None
        self.__password = None
        self.__url = None


    @classmethod
    def close_db(cls):
        cls.__cursor.close()
        cls.__db.close()


    @classmethod
    def create_tabel(cls):
        cls.__cursor.execute("""
        CREATE TABLE IF NOT EXISTS account (username text, email text, 
        password text, url text)
        """)
        cls.__db.commit()


    def create_account(self):
        self.__username = input_line("Enter username: ")
        self.__email = input_line("Enter email: ")
        self.__password = input_line("Enter password: ")
        self.__url = input_line("Enter url: ")
        print_line_emoji("Saving in DataBase", end='')

        for _ in range(4):
            print('.', end='')
            time.sleep(0.2)
        print('')
        if self.save():
            print_line_emoji("Account has ben created.")


    def save(self):
        Account.create_tabel()
        Account.__cursor.execute("""
        INSERT INTO account (username, email, password, url) VALUES (?, ?, 
        ?, ?)
        """, (self.__username, self.__email, self.__password, self.__url))
        self.__db.commit()
        return True


    @staticmethod
    def get_account_messages(status="Found"):
        banner = "\033[1;32;40m{}".format("""
  __ _  ___ ___ ___  _   _ _ __ | |_ 
 / _` |/ __/ __/ _ \| | | | '_ \| __|
| (_| | (_| (_| (_) | |_| | | | | |_ 
 \__,_|\___\___\___/ \__,_|_| |_|\__|
        """)
        msg = "\033[1;32;40m{:{align}{width}}".format(
            status,
            align="-^",
            width=str(len(status) + 32)
        )
        print(banner)
        print(msg)


    @staticmethod
    def print_data(account):
        print("username: {}".format(account[0]))
        print("email: {}".format(account[1]))
        print("password {}".format(account[2]))
        print("url: {}".format(account[3]))


    @classmethod
    def get_account(cls, username):
        try:
            account = cls.__cursor.execute("""
            SELECT * FROM account where username=?
            """, (username,)).fetchone()
            if account:
                cls.get_account_messages()
                cls.print_data(account)
                return account
            raise Error
        except (TypeError, Error):
            cls.get_account_messages("Not Found")
            failed()


    @classmethod
    def change_password(cls, prompt):
        # prompt[1]=password_value prompt[0]=url_value
        try:
            cls.__cursor.execute("""
            UPDATE account SET password=? WHERE url=?
            """, (prompt[1], prompt[0]))
            cls.__db.commit()
            success("Password has ben changed.")
            return True
        except Error:
            failed("There is a mistake in connecting with the database")


    @classmethod
    def change_email(cls, prompt):
        try:
            cls.__cursor.execute("""
            UPDATE account SET email=? WHERE url=?
            """, (prompt[1], prompt[0]))
            cls.__db.commit()
            success("Email has ben changed.")
            return True
        except Error:
            failed("There is a mistake in connecting with the database")


    @classmethod
    def change_url(cls, prompt):
        try:
            cls.__cursor.execute("""
            UPDATE account SET url=? WHERE url=?
            """, (prompt[1], prompt[0]))
            cls.__db.commit()
            success("Url has ben changed.")
            return True
        except Error:
            failed("There is a mistake in connecting with the database")


    @staticmethod
    def get_all(prompt):
        try:
            result = Account.__cursor.execute("""
            SELECT * FROM account where url=?
            """, (prompt,)).fetchall()

            if result:
                for row in result:
                    print("""\033[1;32;40m
                    Username: {} Email: {} Password: {} Url: {}
                    """.format(*row))
            return result
            raise Error
        except (Error, TypeError):
            failed("There are no accounts registered for this site")


class CommandManager(Account):
    __prompt_list = ["create", "find", "change", "cmd", "exit", "all", "cls"]


    def __init__(self):
        welcome_screen()
        while True:
            try:
                # command -option value
                # change -option -url url_value new_password
                prompt = input_line("\033[1;35;40m").split()
                self.is_valid_prompt(prompt[0])

                if prompt[0] == "cls":
                    os.system("cls")

                if prompt[0] == "create":
                    self.create_account()

                elif prompt[0] == "find":
                    self.find(prompt[1:])

                elif prompt[0] == "change":
                    self.change(prompt[1:])

                elif prompt[0] == "cmd":
                    self.cmd()

                elif prompt[0] == "exit":
                    Account.close_db()
                    sys.exit(0)

            except (ValueError, IndexError):
                print("\033[1;31;40m Enter valid command")


    @staticmethod
    def cmd():
        while True:
            command = input_line("~BETA Mod - cmd: ")
            if command == "exit":
                return True
            print(os.system(command))


    def find(self, prompt):
        # -option value
        if prompt[0] == "-all":
            self.get_all(prompt[1])
            return
        self.get_account(prompt[1])


    def change(self, prompt):
        if prompt[0] == "-password":
            return self.change_password(prompt[2:])
        if prompt[0] == "-email":
            return self.change_email(prompt[2:])
        if prompt[0] == "-url":
            return self.change_url(prompt[1:])
        raise ValueError


    @staticmethod
    def is_valid_prompt(prompt):
        if prompt in CommandManager.__prompt_list:
            return True
        raise ValueError


if __name__ == "__main__":
    CommandManager()
