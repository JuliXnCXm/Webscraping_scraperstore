const axios = require('axios');
const fs = require('fs');


class IndexController {

    getApi  = (lat, lon, idx) => {

        var data = JSON.stringify({
            "supported-headers": ["OPERATION_HEADER"],
        });
        var settings = {
            method: "post",
            url: "",
            headers: {
            "Content-Type": "application/json",
            },
            data: data,
        };

        axios(settings)
            .then(function (response) {
                let resp = JSON.stringify(response.data.sections[0].cards);
                fs.writeFileSync(
                    `src/data/data${idx}.json`,
                    resp,
                    {
                        encoding: 'utf8',
                        flag: 'w+'
                    },
                    (err, data) => {
                        if (!err) {
                            console.log("file saved");
                        } else {
                            console.log(err);
                        }
                    }
                );
                console.log('saved')
            }).catch(function (error) {
                console.log(error);
            });

    }
}

module.exports = IndexController;