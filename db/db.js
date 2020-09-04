const { Pool } = require('pg');

const pool = new Pool({
    user: 'postgres',
    host: 'phantomdb.cstig7wsxqtk.us-west-2.rds.amazonaws.com',
    database: 'knorrstats',
    password: 'gayisabsolutelynotokay',
    port: 5432,
});

// Gets data from player table necessary for client functionality
const getClientPlayerData = async () => {
    // Saves rows of query
    let data = (await pool.query("SELECT player_id, name, ismainroster FROM player")).rows;
    // Appends each row as an object into a list
    let new_rows = [];
    data.forEach((item) => {
        new_rows.push({
            player_id: item.player_id,
            player_name: item.name,
            is_main_roster: item.ismainroster
        });
    }); 
    
    return new_rows;
};

const getClientMapData = async () => {
    // Saves rows of query
    let data = (await pool.query("SELECT map_id, map_name FROM maps")).rows;
    // Appends each row as an object into a list
    let new_rows = [];
    data.forEach((item) => {
        new_rows.push({
            player_id: item.player_id,
            player_name: item.name,
            is_main_roster: item.ismainroster
        });
    }); 
    
    return new_rows;
}

module.exports = {
    query: (text, params) => pool.query(text, params),
    getClientPlayerData: () => getClientPlayerData(),
    getClientMapData: () => getClientMapData()
};
