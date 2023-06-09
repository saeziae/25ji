#! /usr/bin/python3
import datetime
import asyncio
import os
import random
import time
HOST = ''
PORT = 2500
LYRICS_FILE = 'lyrics.txt'
LYRICS = []
FOLDER = './music'
ASCII = b"""               //                                                        //    <>
 _   _  _     //>    _      _                        _          _ \\\\>   //__   _____     ___    ___
| \\ | |(_)   //     | |    | |                      | |        | | \\\\  //__ \\ | ____|_  / _ \\  / _ \\
|  \\| | _   // __ _ | |__  | |_  ___  ___   _ __  __| |   __ _ | |_ \\\\//   ) || |__ (_)| | | || | | |
| . ` || | // / _` || '_ \\ | __|/ __|/ _ \\ | '__|/ _` |  / _` || __| //   / / |___ \\   | | | || | | |
| |\\  || |// | (_| || | | || |_| (__| (_) || |  | (_| | | (_| || |_ //\\\\ / /_  ___) |_ | |_| || |_| |
|_| \\_||_//]  \\__, ||_| |_| \\__|\\___|\\___/ |_|   \\__,_|  \\__,_| \\__//  \\\\____||____/(_) \\___/  \\___/
       <//>______/ |                                              //>   \\\\
       //  \\______/                                              //]
      //                                                        //
"""


async def handle(client_reader, client_writer):
    client_address = client_writer.get_extra_info('peername')
    print(f"Connection from {client_address} established nya")
    try:
        # Judge if now is 25-ji
        if datetime.datetime.utcnow().hour == 16:
            music = random.choice(os.listdir(FOLDER))
            print(f"Sending music {music} nya")
            with open(os.path.join(FOLDER, music), "rb") as f:
                client_writer.write(f.read())
            await client_writer.drain()
        else:
            client_writer.write(ASCII)
            await client_writer.drain()
            lyric = random.choice(LYRICS)
            for x in lyric:
                client_writer.write(x.encode())
                await client_writer.drain()
                time.sleep(0.05)
            client_writer.write(b'\n')
            await client_writer.drain()
            time.sleep(0.05)

    except ConnectionResetError:
        print(f"Connection from {client_address} reset by peer nya.")
    except:
        print(f"Unknown errors nya.")
    finally:
        client_writer.close()


async def main():
    server = await asyncio.start_server(handle, HOST, PORT)
    async with server:
        print(f"Listening on port {PORT} nya")
        await server.serve_forever()

if __name__ == '__main__':
    # Load lyrics
    with open(LYRICS_FILE, "r") as f:
        LYRICS = f.read().split("\n\n")
        pass
    asyncio.run(main())
