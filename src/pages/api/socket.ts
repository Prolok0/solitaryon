import { NextApiRequest } from "next";
import { NextApiResponseServerIO } from "src/types/socket";
import { Server as ServerIO } from "socket.io";
import { Server as NetServer } from "http";

export default async (req: NextApiRequest, res: NextApiResponseServerIO) => {
  if (!res.socket.server.io) {
    console.log("Starting socket server...");

    const httpServer: NetServer = res.socket.server as any;
    const io = new ServerIO(httpServer, {
      path: "/api/socket",
    });

    io.on('connection', socket => {
      console.log("[!] connection " + socket.id);
    })

    res.socket.server.io = io;
  }
  res.end();
};
