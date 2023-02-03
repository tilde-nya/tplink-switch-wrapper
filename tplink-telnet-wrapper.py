import telnetlib

class tpswitch():
    def __init__(self):
        self.con = telnetlib.Telnet()
        self.state = "CLOSED"
    
    def open(self, host, port, username, password):
        self.con.open(host, port)

        self.con.read_until(b"User:")
        self.write((username + "\r\n").encode("utf-8"))

        self.con.read_until(b"Password:")
        self.con.write((password + "\r\n").encode("utf-8"))

        self.con.read_until(b">")
        self.write(b"enable\r\n")

        self.con.read_until(b"#")
        self.state = "ENABLED"
        
    def close(self):
        self.con.close()

    def address_table_find_mac(self, mac):
        if (self.state != "ENABLED"):
            raise Exception()
        else:
            self.con.write(("show mac address-table address " + mac + "\r\n").encode("utf-8"))
            response = self.con.expect([b"Total MAC Addresses for this criterion: ", b"Specified entry is NULL"])
            if response[0] == 0:
                response = response[2].decode().split("\n")[6:-2:]
                self.results = []
                for i in response:
                    i = i.split()
                    self.results.append({
                        "address": i[0],
                        "vlan": i[1],
                        "port": i[2],
                        "type": i[3],
                        "aging": i[4]
                    })
                self.con.read_eager().decode()
                return response
            elif response[0] == 1:
                raise Exception("Address not found")
                return            
            