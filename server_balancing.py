import os
import uuid
import logging as logger


logger.basicConfig(
    filename="log.log",
    level=logger.DEBUG,
    format="%(asctime)s:%(levelname)s:%(message)s",
)


class ServerBalancing(object):
    def __init__(self, ttask=5, umax=10, output_file_path="output.txt"):
        self.ttask = ttask
        self.umax = umax
        self.output_file_path = output_file_path
        self.servers = []
        self.count = 0

    def execute(self, input_file):
        input_file = self.read_file_lines(input_file)
        output_file = open(self.output_file_path, "w")

        for qtd_user in input_file:
            self.persistent_user()
            self.persistent_servers()

            try:
                usr = int(qtd_user)
                self.add_users(usr)
            except ValueError as e:
                message ='Invalid value {qtd_user} in file'
                logger.error(message)
                raise BaseException(message)
            self.count += len(self.servers)
            self.add_line(self.get_servers_snapshot(), output_file)
        while self.get_qtd_servers():
            self.persistent_user()
            self.persistent_servers()
            self.count += len(self.servers)
            self.add_line(self.get_servers_snapshot(), output_file)

        self.add_line(f'${self.count}', output_file)
        print(self.count)
        output_file.close()

    def read_file_lines(self, file):
        if os.path.isfile(file):
            file = open(file)
            lines = file.readlines()
            file.close()
            return lines
        else:
            message = f"File {file} dont exist"
            logger.error(message)
            raise BaseException(message)

    def get_free_server(self):
        server_num = 1
        for i, server in enumerate(self.servers):
            if len(self.servers[i]["users"]) < self.umax:
                return self.servers[i]["uid"]

        sid = uuid.uuid1()
        self.servers.append({"uid": sid, "users": []})
        return sid

    def add_user(self, uid, sid):
        for server in self.servers:
            if server["uid"] == sid:
                user = {"uid": uid, "tasks": self.ttask}
                logger.info(f"add user {user}")
                server["users"].append(user)

    def persistent_servers(self):
        server_no_users = []

        for server in self.servers:
            if len(server["users"]) == 0:
                logger.info(f"add server {server}")
                server_no_users.append(server)
        for server in server_no_users:
            logger.info(f"remove server {server}")
            self.servers.remove(server)

    def persistent_user(self):

        for i, server in enumerate(self.servers):
            user_zero_procs = []

            for k, user in enumerate(self.servers[i]["users"]):
                self.servers[i]["users"][k]["tasks"] -= 1
                if self.servers[i]["users"][k]["tasks"] == 0:
                    user_zero_procs.append(self.servers[i]["users"][k])
            for user in user_zero_procs:
                logger.info(f"remove user {user}")
                self.servers[i]["users"].remove(user)

    def add_users(self, qtd_user):
        for x in range(0, qtd_user):
            self.add_user(uuid.uuid1(), self.get_free_server())

    def get_servers_snapshot(self):
        output = []
        for server in self.servers:
            output.append(str(len(server["users"])))
        if len(output):
            return ",".join(output) + "\n"
        return "\n"

    def get_qtd_servers(self):
        return len(self.servers)

    def add_line(sel, line, file):
        file.write(line)
