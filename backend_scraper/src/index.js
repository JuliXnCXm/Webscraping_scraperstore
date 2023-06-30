const express = require('express');
const cors = require('cors');
const morgan = require('morgan');
const IndexRouter = require( './routers/index');

class Server {
    constructor() {
        this.app = express();
        this.#config();
    }
    #config() {
        //midlewares
        this.app.use(morgan("dev"));
        this.app.use(cors());
        this.app.use(express.json());
        this.app.set('port', process.env.PORT || 3000);
        //creating routes
        const IndexR = new IndexRouter();
        //adding routes
        this.app.use("/", IndexR.router);

        this.app.listen(3000, () => {
        console.log("Server on port", this.app.get('port'));
        });
    }

}

new Server();