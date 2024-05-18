import figlet from "figlet";

const server = Bun.serve({
    port: 9111,
    fetch(req) {
        const body = figlet.textSync("Hello Bun!");
        return new Response(body);
        // return new Response("Hello Bun!");
    },
  });
  
console.log(`Listening on http://localhost:${server.port} ...`);
console.log("Welcome to Bun HTTP server!");
