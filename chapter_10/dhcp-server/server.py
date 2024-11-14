import asyncio
import coloredlogs
import gc
import logging
import socket
import time
from models import UserLease
from packet import Header, DhcpDiscover, DhcpRequest, DhcpOffer, DhcpAck, Ip
from sqlalchemy import create_engine, func, desc
from sqlalchemy.orm import Session

engine = create_engine("mysql+pymysql://root@localhost/dhcp_service")


class CaptiveDhcpServer:
    async def get_free_ip(self, server_ip: str, mac: str) -> str:
        logging.info(f"Server IP: {server_ip}")
        with Session(engine) as session:
            result = session.query(UserLease).order_by(desc(func.INET_ATON(UserLease.ip_addr))).limit(1).first()
            if result:
                return Ip.next_ip(result.ip_addr)
        return Ip.next_ip(server_ip)

    def send_broadcast_reply(self, reply):
        udpb = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            udpb.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            udpb.setsockopt(socket.SOL_SOCKET, 0x20, 1)
            udpb.setblocking(False)
            broadcast_addr = socket.getaddrinfo("255.255.255.255", 68, socket.AF_INET, socket.SOCK_DGRAM)[0][4]
            logging.info(f"Broadcasting Response: {reply}")
            udpb.sendto(reply, broadcast_addr)
        except Exception as e:
            logging.error(f"Failed to broadcast reply {e}")
        finally:
            udpb.close()

    async def get_or_create_lease(self, server_ip, mac_address):
        with Session(engine) as session:
            result = session.query(UserLease).filter(mac_address == mac_address)
            if result.count() > 0:
                return result.first().ip_addr
            ip_addr = await self.get_free_ip(server_ip, mac_address)
            user_lease = UserLease(ip_addr=ip_addr, mac_address=mac_address)
            session.add(user_lease)
            session.commit()

    async def get_leases(self):
        with Session(engine) as session:
            lease_count = session.query(UserLease).count()
            logging.info(f"Lease count {lease_count}")

    async def run(self, server_ip: str, netmask: str):
        await self.get_leases()
        udps = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udps.setblocking(False)
        udps.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        bound = False
        while not bound:
            try:
                addr = socket.getaddrinfo("0.0.0.0", 67, socket.AF_INET, socket.SOCK_DGRAM)[0][-1]
                udps.bind(addr)
                logging.info("Starting server on port 67")
                bound = True
            except Exception as e:
                logging.error(f"Failed to bind to port {e}")
                time.sleep(0.5)

        while True:
            try:
                data, addr = udps.recvfrom(2048)
                logging.info("Incoming data...")
                logging.debug(data)

                request = Header.parse(data)
                logging.debug(request)

                if isinstance(request, DhcpDiscover):
                    logging.info("Creating Offer for Discover")
                    response = DhcpOffer()
                    client_ip = await self.get_or_create_lease(server_ip, request.header.chaddr)
                    logging.info(f"Found new ip: {client_ip}")
                    reply = response.answer(request, client_ip, server_ip, netmask)
                    logging.debug(response)

                    self.send_broadcast_reply(reply)

                elif isinstance(request, DhcpRequest):
                    logging.info("Creating Ack for Request")
                    response = DhcpAck()
                    reply = response.answer(request, server_ip, netmask)
                    logging.info(response)

                    self.send_broadcast_reply(reply)
                await asyncio.sleep(0.1)
            except OSError:
                await asyncio.sleep(0.5)

            except Exception as e:
                logging.error(f"Exception {e}")
                await asyncio.sleep(0.5)

        udps.close()


if __name__ == "__main__":
    coloredlogs.install(level=logging.DEBUG)
    run_app = CaptiveDhcpServer()
    asyncio.run(run_app.run("10.65.4.1", "255.255.0.0"))
