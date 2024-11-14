import json


class DhcpOptions:
    SUBNET = 1
    ROUTER = 3
    DNS = 6
    HOST_NAME = 12
    DOMAIN_NAME = 15
    REQUESTED_IP = 50
    LEASE_TIME = 51
    DHCP_MESSAGE_TYPE = 53
    DHCP_SERVER = 54
    PARAM_REQUEST_LIST = 55
    MAX_MESSAGE_SIZE = 57
    RENEWAL_T1 = 58
    RENEWAL_T2 = 59
    VENDOR_CLASS_ID = 60
    CAPTIVE_URI = 114


class DhcpMessageType:
    DISCOVER = 1
    OFFER = 2
    REQUEST = 3
    ACK = 5


class Ip:
    # Network byte order
    BYTE_ORDER = "big"

    @staticmethod
    def str_to_byte(ip: str):
        ip_data = ip.split(".")
        b = int.to_bytes(int(ip_data[0]), 1, Ip.BYTE_ORDER)
        b += int.to_bytes(int(ip_data[1]), 1, Ip.BYTE_ORDER)
        b += int.to_bytes(int(ip_data[2]), 1, Ip.BYTE_ORDER)
        b += int.to_bytes(int(ip_data[3]), 1, Ip.BYTE_ORDER)
        return b

    @staticmethod
    def str_to_int(ip: str):
        b = Ip.str_to_byte(ip)
        return int.from_bytes(b, Ip.BYTE_ORDER)

    @staticmethod
    def int_to_str(i):
        if i == 0:
            return "0.0.0.0"
        b = int.to_bytes(i, 4, Ip.BYTE_ORDER)

        ip = str(int.from_bytes(b[:1], Ip.BYTE_ORDER)) + "."
        ip += str(int.from_bytes(b[1:2], Ip.BYTE_ORDER)) + "."
        ip += str(int.from_bytes(b[2:3], Ip.BYTE_ORDER)) + "."
        ip += str(int.from_bytes(b[3:4], Ip.BYTE_ORDER))
        return ip

    @staticmethod
    def next_ip(ip: str):
        int_ip = Ip.str_to_int(ip)
        next_ip = Ip.int_to_str(int_ip + 1)
        return next_ip


class Header:
    """
    This class models a DHCP Header Packet

    """

    # Network byte order
    BYTE_ORDER = "big"

    @staticmethod
    def parse(data):
        header = Header()
        header.unpack(data)

        if DhcpOptions.DHCP_MESSAGE_TYPE not in header.options:
            print("Unknown header. Missing message type.")
        elif header.options[DhcpOptions.DHCP_MESSAGE_TYPE] == DhcpMessageType.DISCOVER:
            return DhcpDiscover(header)
        elif header.options[DhcpOptions.DHCP_MESSAGE_TYPE] == DhcpMessageType.OFFER:
            return DhcpOffer(header)
        elif header.options[DhcpOptions.DHCP_MESSAGE_TYPE] == DhcpMessageType.REQUEST:
            return DhcpRequest(header)
        elif header.options[DhcpOptions.DHCP_MESSAGE_TYPE] == DhcpMessageType.ACK:
            return DhcpAck(header)
        else:
            print("Unknown header: " + header.options[DhcpOptions.DHCP_MESSAGE_TYPE])

    def __init__(self):
        self.op: int = 0  # 1 octet. Operation Type
        self.htype: int = 0  # 1 octet
        self.hlen: int = 0  # 1 octet
        self.hops: int = 0  # 1 octet
        self.xid: int = 0  # 4 octets
        self.secs: int = 0  # 2 octets
        self.flags: int = 0  # 2 octets
        self.ciaddr: int = 0  # 4 octets. Client IP
        self.yiaddr: int = 0  # 4 octets. Your Ip
        self.siaddr: int = 0  # 4 octets. Server Ip
        self.giaddr: int = 0  # 4 octets. Gateway Ip
        self.chaddr: str = ""
        self.chaddr1: int = 0  # 4 octets. Client hardware
        self.chaddr2: int = 0  # 4 octets. Client hardware
        self.chaddr3: int = 0  # 4 octets. Client hardware
        self.chaddr4: int = 0  # 4 octets. Client hardware
        self.magic: int = 0x63825363  # 4 octets. magic cookie 0x63825363
        self.options: dict = {}  # variable options

    def unpack(self, data):
        self.op = int.from_bytes(data[:1], self.BYTE_ORDER)
        self.htype = int.from_bytes(data[1:2], self.BYTE_ORDER)
        self.hlen = int.from_bytes(data[2:3], self.BYTE_ORDER)
        self.hops = int.from_bytes(data[3:4], self.BYTE_ORDER)
        self.xid = int.from_bytes(data[4:8], self.BYTE_ORDER)
        self.secs = int.from_bytes(data[8:10], self.BYTE_ORDER)
        self.flags = int.from_bytes(data[10:12], self.BYTE_ORDER)
        self.ciaddr = int.from_bytes(data[12:16], self.BYTE_ORDER)
        self.yiaddr = int.from_bytes(data[16:20], self.BYTE_ORDER)
        self.siaddr = int.from_bytes(data[20:24], self.BYTE_ORDER)
        self.giaddr = int.from_bytes(data[24:28], self.BYTE_ORDER)

        self.chaddr = "{:02x}".format(int.from_bytes(data[28:29], self.BYTE_ORDER)) + ":"
        self.chaddr += "{:02x}".format(int.from_bytes(data[29:30], self.BYTE_ORDER)) + ":"
        self.chaddr += "{:02x}".format(int.from_bytes(data[30:31], self.BYTE_ORDER)) + ":"
        self.chaddr += "{:02x}".format(int.from_bytes(data[31:32], self.BYTE_ORDER)) + ":"
        self.chaddr += "{:02x}".format(int.from_bytes(data[32:33], self.BYTE_ORDER)) + ":"
        self.chaddr += "{:02x}".format(int.from_bytes(data[33:34], self.BYTE_ORDER))

        self.chaddr1 = int.from_bytes(data[28:32], self.BYTE_ORDER)
        self.chaddr2 = int.from_bytes(data[32:36], self.BYTE_ORDER)
        self.chaddr3 = int.from_bytes(data[36:40], self.BYTE_ORDER)
        self.chaddr4 = int.from_bytes(data[40:44], self.BYTE_ORDER)
        # bootp legacy 192 octets [sname 64 + file 128]
        self.magic = int.from_bytes(data[236:240], self.BYTE_ORDER)

        position = 240
        if len(data) < position + 1:
            return
        option_code = int.from_bytes(data[position : position + 1], self.BYTE_ORDER)
        position += 1
        while option_code != 255:
            option_len = int.from_bytes(data[position : position + 1], self.BYTE_ORDER)
            position += 1
            if option_code in [
                DhcpOptions.HOST_NAME,
                DhcpOptions.DOMAIN_NAME,
                DhcpOptions.VENDOR_CLASS_ID,
                DhcpOptions.CAPTIVE_URI,
            ]:
                option_value = data[position : position + option_len].decode("utf-8")
            elif option_code in [DhcpOptions.PARAM_REQUEST_LIST]:
                option_value = ""
                for i in range(option_len):
                    param = int.from_bytes(data[position + i : position + i + 1], self.BYTE_ORDER)
                    option_value += str(param) + ","
                option_value = option_value[:-1]
            else:
                option_value = int.from_bytes(data[position : position + option_len], self.BYTE_ORDER)
            position += option_len
            self.options[option_code] = option_value

            option_code = int.from_bytes(data[position : position + 1], self.BYTE_ORDER)
            position += 1

    def pack(self):
        packet = int.to_bytes(self.op, 1, self.BYTE_ORDER)
        packet += int.to_bytes(self.htype, 1, self.BYTE_ORDER)
        packet += int.to_bytes(self.hlen, 1, self.BYTE_ORDER)
        packet += int.to_bytes(self.hops, 1, self.BYTE_ORDER)
        packet += int.to_bytes(self.xid, 4, self.BYTE_ORDER)
        packet += int.to_bytes(self.secs, 2, self.BYTE_ORDER)
        packet += int.to_bytes(self.flags, 2, self.BYTE_ORDER)
        packet += int.to_bytes(self.ciaddr, 4, self.BYTE_ORDER)
        packet += int.to_bytes(self.yiaddr, 4, self.BYTE_ORDER)
        packet += int.to_bytes(self.siaddr, 4, self.BYTE_ORDER)
        packet += int.to_bytes(self.giaddr, 4, self.BYTE_ORDER)
        packet += int.to_bytes(self.chaddr1, 4, self.BYTE_ORDER)
        packet += int.to_bytes(self.chaddr2, 4, self.BYTE_ORDER)
        packet += int.to_bytes(self.chaddr3, 4, self.BYTE_ORDER)
        packet += int.to_bytes(self.chaddr4, 4, self.BYTE_ORDER)
        packet += int.to_bytes(0, 192, self.BYTE_ORDER)
        packet += int.to_bytes(self.magic, 4, self.BYTE_ORDER)
        for option_code in self.options:
            option_value = self.options[option_code]
            packet += int.to_bytes(option_code, 1, self.BYTE_ORDER)
            if option_code in [
                DhcpOptions.HOST_NAME,
                DhcpOptions.DOMAIN_NAME,
                DhcpOptions.VENDOR_CLASS_ID,
                DhcpOptions.CAPTIVE_URI,
            ]:
                packet += int.to_bytes(len(option_value), 1, self.BYTE_ORDER)
                packet += bytes(option_value, "utf-8")
            elif option_code in [DhcpOptions.PARAM_REQUEST_LIST]:
                param_request_list = option_value.split(",")
                packet += int.to_bytes(len(param_request_list), 1, self.BYTE_ORDER)
                for param_request in param_request_list:
                    packet += int.to_bytes(int(param_request), 1, self.BYTE_ORDER)
            elif option_code in [
                DhcpOptions.ROUTER,
                DhcpOptions.DHCP_SERVER,
                DhcpOptions.DNS,
                DhcpOptions.SUBNET,
                DhcpOptions.LEASE_TIME,
                DhcpOptions.RENEWAL_T1,
                DhcpOptions.RENEWAL_T2,
            ]:
                octet_size = 4
                packet += int.to_bytes(octet_size, 1, self.BYTE_ORDER)
                packet += int.to_bytes(option_value, octet_size, self.BYTE_ORDER)
            elif option_code in [DhcpOptions.MAX_MESSAGE_SIZE]:
                octet_size = 2
                packet += int.to_bytes(octet_size, 1, self.BYTE_ORDER)
                packet += int.to_bytes(option_value, octet_size, self.BYTE_ORDER)
            else:
                try:
                    octet_size = (int(option_value).bit_length() + 7) // 8
                except Exception:
                    # AttributeError: 'int' object has no attribute 'bit_length'
                    octet_size = 1

                packet += int.to_bytes(octet_size, 1, self.BYTE_ORDER)
                packet += int.to_bytes(option_value, octet_size, self.BYTE_ORDER)

        packet += int.to_bytes(255, 1, self.BYTE_ORDER)
        return packet

    def __str__(self):
        str_options = self.options.copy()
        if DhcpOptions.ROUTER in str_options:
            str_options[DhcpOptions.ROUTER] = Ip.int_to_str(str_options[DhcpOptions.ROUTER])
        if DhcpOptions.SUBNET in str_options:
            str_options[DhcpOptions.SUBNET] = Ip.int_to_str(str_options[DhcpOptions.SUBNET])
        if DhcpOptions.DNS in str_options:
            str_options[DhcpOptions.DNS] = Ip.int_to_str(str_options[DhcpOptions.DNS])
        if DhcpOptions.DHCP_SERVER in str_options:
            str_options[DhcpOptions.DHCP_SERVER] = Ip.int_to_str(str_options[DhcpOptions.DHCP_SERVER])
        if DhcpOptions.REQUESTED_IP in str_options:
            str_options[DhcpOptions.REQUESTED_IP] = Ip.int_to_str(str_options[DhcpOptions.REQUESTED_IP])

        return json.dumps(
            {
                "op": self.op,
                "htype": self.htype,
                "hlen": self.hlen,
                "hops": self.hops,
                "xid": hex(self.xid),
                "secs": self.secs,
                "flags": self.flags,
                "ciaddr": Ip.int_to_str(self.ciaddr),
                "yiaddr": Ip.int_to_str(self.yiaddr),
                "siaddr": Ip.int_to_str(self.siaddr),
                "giaddr": Ip.int_to_str(self.giaddr),
                "chaddr": self.chaddr,
                "chaddr1": hex(self.chaddr1),
                "chaddr2": hex(self.chaddr2),
                "chaddr3": self.chaddr3,
                "chaddr4": self.chaddr4,
                "magic": hex(self.magic),
                "options": str_options,
            }
        )

    def answer(self, header):
        self.xid = header.xid
        self.chaddr1 = header.chaddr1
        self.chaddr2 = header.chaddr2
        self.chaddr3 = header.chaddr3
        self.chaddr4 = header.chaddr4


class DhcpDiscover:
    """
    This class models a DHCP Discover Packet
    """

    def __init__(self, header: Header = None):
        if header:
            self.header = header
        else:
            self.header: Header = Header()
            self.header.op = 1
            self.header.htype = 1
            self.header.hlen = 6
            self.header.options[DhcpOptions.DHCP_MESSAGE_TYPE] = DhcpMessageType.DISCOVER

    def unpack(self, packet):
        self.header.unpack(packet)

    def pack(self):
        packet = self.header.pack()

        return packet

    def __str__(self):
        return "DhcpDiscover: " + str(self.header)


class DhcpOffer:
    """
    This class models a DHCP Offer Packet
    """

    def __init__(self, header: Header = None):
        if header:
            self.header = header
        else:
            self.header: Header = Header()
            self.header.op = 2
            self.header.htype = 1
            self.header.hlen = 6
            self.header.options[DhcpOptions.DHCP_MESSAGE_TYPE] = DhcpMessageType.OFFER

    def answer(self, discover: DhcpDiscover, client_ip: str, server_ip: str, netmask: str):
        self.header.answer(discover.header)

        self.header.yiaddr = Ip.str_to_int(client_ip)

        sIp = Ip.str_to_int(server_ip)
        self.header.siaddr = sIp
        self.header.options[DhcpOptions.ROUTER] = sIp
        self.header.options[DhcpOptions.DHCP_SERVER] = sIp
        self.header.options[DhcpOptions.DNS] = sIp

        self.header.options[DhcpOptions.SUBNET] = Ip.str_to_int(netmask)
        self.header.options[DhcpOptions.LEASE_TIME] = 86400  # 1 day

        return self.pack()

    def unpack(self, packet):
        self.header.unpack(packet)

    def pack(self):
        packet = self.header.pack()

        return packet

    def __str__(self):
        return "DhcpOffer: " + str(self.header)


class DhcpRequest:
    """
    This class models a DHCP Request Packet
    """

    def __init__(self, header: Header = None):
        if header:
            self.header = header
        else:
            self.header: Header = Header()
            self.header.op = 1
            self.header.htype = 1
            self.header.hlen = 6
            self.header.options[DhcpOptions.DHCP_MESSAGE_TYPE] = DhcpMessageType.REQUEST

    def unpack(self, packet):
        self.header.unpack(packet)

    def pack(self):
        packet = self.header.pack()

        return packet

    def __str__(self):
        return "DhcpRequest: " + str(self.header)


class DhcpAck:
    """
    This class models a DHCP Ack Packet
    """

    def __init__(self, header: Header = None):
        if header:
            self.header = header
        else:
            self.header: Header = Header()
            self.header.op = 2
            self.header.htype = 1
            self.header.hlen = 6
            self.header.options[DhcpOptions.DHCP_MESSAGE_TYPE] = DhcpMessageType.ACK

    def answer(self, request: DhcpRequest, server_ip: str, netmask: str):
        self.header.answer(request.header)

        self.header.yiaddr = request.header.options[DhcpOptions.REQUESTED_IP]

        sIp = Ip.str_to_int(server_ip)
        self.header.siaddr = sIp
        self.header.options[DhcpOptions.ROUTER] = sIp
        self.header.options[DhcpOptions.DHCP_SERVER] = sIp
        self.header.options[DhcpOptions.DNS] = sIp

        self.header.options[DhcpOptions.SUBNET] = Ip.str_to_int(netmask)
        self.header.options[DhcpOptions.LEASE_TIME] = 86400  # least time

        self.header.options[DhcpOptions.CAPTIVE_URI] = "http://" + server_ip

        return self.pack()

    def unpack(self, packet):
        self.header.unpack(packet)

    def pack(self):
        packet = self.header.pack()

        return packet

    def __str__(self):
        return "DhcpAck: " + str(self.header)
