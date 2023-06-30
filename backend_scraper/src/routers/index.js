const { Router } = require("express");
const IndexController = require( "../controllers" );

class IndexRouter {

    constructor() {
        this.router = Router();
        this.#config();

    }
    #config() {

        const locations = [];

        let idx = 0
        for (let i = 0; i < locations.length; i++) {
            const objIndex = new IndexController()
                objIndex.getApi(locations[i][0], locations[i][1], idx);
            idx++;
        }

        setTimeout(() => {
            process.exit(0);
        },10000)
    }
}

module.exports = IndexRouter;
