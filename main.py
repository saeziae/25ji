# /usr/bin/python3
import datetime
import asyncio
import os
import random
HOST = ''
PORT = 2500
LYRICS_FILE = 'lyrics.txt'
LYRICS = []
FOLDER = './music'


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
            lyric = random.choice(LYRICS)
            client_writer.write(lyric.encode())
            await client_writer.drain()

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
