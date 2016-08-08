__author__ = 'Mark'

import socket
import user


class TwitchBot:
    def __init__(self, nickname, password, channel, host="irc.chat.twitch.tv", port=6667):
        """Creates an instance of a TwitchBot

        Keyword arguments:
        HOST -- the url of the a Twitch IRC API (irc.chat.twitch.tv)
        PORT -- port of the Twitch API (non SSL 6667)
        NICK -- username of the bot
        PASS -- authorization token for user KVarjanBot
        CHANNEL -- name of the channel whos chat shall be mderated (the name should be written in lower case)
        MODT -- set to false, bot will only start once massege of the day is recieved

        """
        self.HOST = host
        self.NICK = nickname
        self.PORT = port
        self.PASS = password
        self.CHANNEL = channel
        self.MODT = False
        self.s = socket.socket()
        self.readbuffer = ""

    def join_channel(self):
        self.s.connect((self.HOST, self.PORT))
        passw = "PASS " + self.PASS + "\r\n"
        nick = "NICK " + self.NICK + "\r\n"
        join_str = "JOIN #" + self.CHANNEL + " \r\n"
        self.s.send(passw.encode('utf-8'))
        self.s.send(nick.encode('utf-8'))
        self.s.send(join_str.encode('utf-8'))

    def send_message(self, message):
        msg = "PRIVMSG #" + self.CHANNEL + " :" + message + "\r\n"
        self.s.send(msg.encode('utf-8'))
        print(message)

    def run(self):
        self.join_channel()
        while True:
            self.readbuffer = self.readbuffer + self.s.recv(1024).decode()
            temp = self.readbuffer.split("\n")
            self.readbuffer = temp.pop()

            for line in temp:
                # Checks whether the message is PING because its a method of Twitch to check if you're afk
                if line[0] == "PING":
                    pong = "PONG %s\r\n" % line[1]
                    self.s.send(pong.encode('utf-8'))
                else:
                    # Splits the given string so we can work with it better
                    parts = line.split(":")

                    if "QUIT" not in parts[1] and "JOIN" not in parts[1] and "PART" not in parts[1]:
                        try:
                            # Sets the message variable to the actual message sent
                            message = parts[2][:len(parts[2]) - 1]

                        except:
                            message = ""
                        # Sets the username variable to the actual username
                        usernamesplit = parts[1].split("!")
                        username = usernamesplit[0]

                        # Only works after twitch is done announcing stuff (MODT = Message of the day)
                        if self.MODT:
                            if message != "":
                                print(username + ": " + message)

                            if message.startswith("!"):
                                if message == "!welcome":
                                    self.send_message("Welcome to Kvarjans stream, best stream in the world " + username)

                                elif message == "!game":
                                    game = user.return_game(self.CHANNEL)
                                    self.send_message("Kvarjan is currently playing " + game)

                            elif message == "kletvica s presledki":
                                self.send_message(".timeout " + username)

                        for l in parts:
                            if "End of /NAMES list" in l:
                                self.MODT = True


if __name__ == "__main__":
    bot = TwitchBot(channel="", nickname="kvarjanbot", password="oauth:6r3ccbq3dxqsj46r4u6xseae0sx8rg") # add channel name of the user whos chat is to be moderated
    bot.run()
