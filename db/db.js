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

// Gets map names and ids for client
const getClientMapData = async () => {
    // Saves rows of query
    let data = (await pool.query("SELECT map_id, map_name FROM maps")).rows;
    // Appends each row as an object into a list
    let new_rows = [];
    data.forEach((item) => {
        new_rows.push({
            map_id: item.map_id,
            map_name: item.map_name
        });
    }); 
    
    return new_rows;
};

// Uploads a game and returns the id
const uploadGame = async (date, map_id, enemy_rounds, team_rounds) => {
    let game_id = (await pool.query("insert into game (date, map_id, enemy_rounds, team_rounds) values ($1, $2, $3, $4) returning game_id", 
                                    [date, map_id, enemy_rounds, team_rounds])).rows[0].game_id;

    return game_id;
}

// Uploads player stats if the player is absent (all null)
const uploadAbsentStats = async(player_id, game_id, is_absent) => {
    await pool.query("insert into game_stats (player_id, game_id, isabsent) values ($1, $2, $3);", [player_id, game_id, is_absent]);
};

// Uploads player stats normally
const uploadStats = async(player_id, game_id, kills, assists, score, mvps, adr, hs, ud, ef, ks3, ks4, ks5, score_pos, kill_pos, is_absent) => {
    await pool.query('insert into game_stats (player_id, game_id, kills, assists, score, mvps, adr, hs, ud, ef, "3ks", "4ks", "5ks", score_pos, kill_pos, isabsent) values ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16);', 
                     [player_id, game_id, kills, assists, score, mvps, adr, hs, ud, ef, ks3, ks4, ks5, score_pos, kill_pos, is_absent]);
};

// Uploads crit or comment
const uploadCommend = async(player_id, date, is_commend, reason) => {
    await pool.query("insert into commends (player_id, date, is_commend, reason) values ($1, $2, $3, $4);", [player_id, date, is_commend, reason]);
};

// Upload player daily
const uploadDaily = async(date, id, total_pts, game_pts, kill_pts, score_pts, adr_pts, multi_pts, crit_pts, abs_pts, is_excused, has_notif, penalty) => {
    await pool.query("insert into daily (date, player_id, total_points, game_points, kill_points, score_points, adr_points, multikill_points, crit_points, absence_points, is_excused, has_notified, absence_penalty) values ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13)",
                     [date, id, total_pts, game_pts, kill_pts, score_pts, adr_pts, multi_pts, crit_pts, abs_pts, is_excused, has_notif, penalty])
}

module.exports = {
    query: (text, params) => pool.query(text, params),
    getClientPlayerData: () => getClientPlayerData(),
    getClientMapData: () => getClientMapData(),
    uploadGame: (date, map_id, enemy_rounds, team_rounds) => uploadGame(date, map_id, enemy_rounds, team_rounds),
    uploadAbsentStats: (player_id, game_id, is_absent) => uploadAbsentStats(player_id, game_id, is_absent),
    uploadStats: (player_id, game_id, kills, assists, score, mvps, adr, hs, ud, ef, ks3, ks4, ks5, score_pos, kill_pos, is_absent) => uploadStats(player_id, game_id, kills, assists, score, mvps, adr, hs, ud, ef, ks3, ks4, ks5, score_pos, kill_pos, is_absent),
    uploadCommend: (player_id, date, is_commend, reason) => uploadCommend(player_id, date, is_commend, reason),
    uploadDaily: (date, id, total_pts, game_pts, kill_pts, score_pts, adr_pts, multi_pts, crit_pts, abs_pts, is_excused, has_notif, penalty) => uploadDaily(date, id, total_pts, game_pts, kill_pts, score_pts, adr_pts, multi_pts, crit_pts, abs_pts, is_excused, has_notif, penalty)
};
