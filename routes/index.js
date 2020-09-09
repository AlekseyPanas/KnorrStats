var express = require('express');
const db = require('../db/db');
const { response } = require('express');
const { Pool } = require('pg');
var router = express.Router();








/* GET home page. */
router.get('/', async (req, res, next) => {
    res.render('index', { title: 'Foo' });
});








/* Ajax call used by pygame client to retrieve player data */
router.get('/ajax/getplayers', async (req, res, next) => {
    let error = false;
    let player_info = await db.getClientPlayerData().catch(async err => {error = true; return err});
    if (error) {
        res.json({error: true})
    } else {
        res.json(player_info);
    }
});










/* Ajax call used by pygame client to retrieve map data */
router.get('/ajax/getmaps', async(req, res, next) => {
    let error = false;
    let map_info = await db.getClientMapData().catch(async err => {error = true; return err});
    if (error) {
        res.json({error: true})
    } else {
        res.json(map_info);
    }
});








router.get('/ajax/debug', (req, res, next) => {
    let date = new Date('4/14/2003');
    console.log(date.toDateString());
    
    res.send("reply");
})










/* Ajax call used by pygame client to upload game data */
router.post('/ajax/upload_data', async(req, res, next) => {
    // Variable to track any connection errors
    let success = true;
    
    // Gets posted json object with all the data
    let uploadJSON = req.body;
    
    // Date for this upload (grabbed from first game)
    let date = new Date(uploadJSON.games[0].date);
    console.log(date)
    
    // Creates an object used for calculating points for each player
    let player_ids = (await db.query("select player_id from player")).rows;
    let points_json = [];
    for (i of player_ids) {
        points_json.push({
            "player_id": i.player_id,
            "game_pts": 0,
            "kill_pts": 0,
            "score_pts": 0,
            "adr_pts": 0,
            "multikill_pts": 0,
            "crit_pts": 0,
            "absence_pts": 0
        });
    };
    
    // Iterates through game data
    for (game of uploadJSON.games) {
        // game stats
        let map_id = game.map_id;
        let team_rounds = parseInt(game.team_rounds);
        let enemy_rounds = parseInt(game.enemy_rounds);
        
        // Determines points for game outcome
        let game_points;
        if (enemy_rounds > team_rounds) {
            game_points = -3;
        } else if (team_rounds > enemy_rounds) {
            game_points = 7;
        } else {
            game_points = 2;
        };
        
        // Gives points for game outcome
        for (player of points_json) {
            player.game_pts += game_points;
        };
        
        // Uploads game and retrieves game_id
        let gameID = await db.uploadGame(date, map_id, enemy_rounds, team_rounds);



        // Iterates through player data
        for (player of game.player_data) {

            // Player points object from points_json based on id
            target_points = points_json.filter(ply => ply.player_id == player.player_id)[0]

            
            if (player.isabsent) {
                // Resets game points
                target_points.game_pts -= game_points;

                // Uploads players stats (if absent, null values)
                await db.uploadAbsentStats(player.player_id, gameID, player.isabsent);

            } else {
                // Upload for non absent
                await db.uploadStats(player.player_id, gameID, player.kills, player.assists,
                    player.score, player.mvps, player.adr, player.hs, player.ud, player.ef,
                    player["3ks"], player["4ks"], player["5ks"], player.score_pos, player.kill_pos, player.isabsent);
            };
                
            // Calculates Points
            let kill_points;
            switch (player.kill_pos) {
                case 1:
                    kill_points = 5;
                    break;
                case 2:
                    kill_points = 3;
                    break;
                case 3:
                    kill_points = 1;
                    break;
                case 4:
                    kill_points = -1;
                    break;
                case 5:
                    kill_points = -2;
                    break;
                default:
                    kill_points = 0;
            }
            
            let score_points;
            switch (player.score_pos) {
                case 1:
                    score_points = 5;
                    break;
                case 2:
                    score_points = 3;
                    break;
                case 3:
                    score_points = 1;
                    break;
                case 4:
                    score_points = -1;
                    break;
                case 5:
                    score_points = -2;
                    break;
                default:
                    score_points = 0;
            }

            // If the game is a win, no deductions for kills or score
            if (team_rounds > enemy_rounds && score_points < 0) {
                score_points = 0;
            };
            if (team_rounds > enemy_rounds && kill_points < 0) {
                kill_points = 0;
            };
            
            // Calculates and adds points
            if (!player.isabsent) {
                target_points.kill_pts += kill_points;
                target_points.score_pts += score_points;
                target_points.multikill_pts += (player["3ks"]) + (player["4ks"] * 3) + (player["5ks"] * 5);
                target_points.adr_pts += Math.round((0.05 * player.adr) - 2.2);
            };
        };
    };
    
    // Defines information vars about the games played
    let game_quant = uploadJSON.games.length;
    let num_full_queue = uploadJSON.games.filter(game => game.player_data.filter(pl => !pl.isabsent).length == 5).length;
    let num_partial_queue = game_quant - num_full_queue

    console.log("quant, 5q, !5q: ", game_quant, num_full_queue, num_partial_queue)

    // Iterates through player daily data
    for (player of uploadJSON.player_daily) {
        let commend_points = 0;
        let crit_points = 0;
        
        // Uploads commend and/or criticism for player and calculates points
        if (player.is_commend) {
            await db.uploadCommend(player.player_id, date, true, player.commend_reason);
            
            commend_points = (await db.query("select * from commends where player_id = $1 and extract(month from date) = $2 and is_commend = TRUE;", [player.player_id, date.getMonth() + 1])).rows.length * 5
            if (commend_points > 30) {
                commend_points = 30;
            };
            
        };
        if (player.is_criticism) {
            await db.uploadCommend(player.player_id, date, false, player.criticism_reason);
            
            crit_points = (await db.query("select * from commends where player_id = $1 and extract(month from date) = $2 and is_commend = FALSE;", [player.player_id, date.getMonth() + 1])).rows.length * 5
            if (crit_points > 30) {
                crit_points = 30;
            };
            
        };
        
        // Sets crit/commend points
        target_points = points_json.filter(ply => ply.player_id == player.player_id)[0];
        target_points.crit_pts += commend_points;
        target_points.crit_pts -= crit_points;
        
        // Absence penalties
        let absence_points = 0;
        
        let penalty = 0;
        let is_main_roster = (await db.getClientPlayerData()).filter(row => row.player_id == player.player_id)[0].is_main_roster;

        let games_participated = uploadJSON.games.filter(game => !game.player_data.filter(pl => pl.player_id == player.player_id)[0].isabsent).length;

        // Checks main roster penalty conditions (Gone for whole night, no excuse, penalty for games that werent 5q)
        if (is_main_roster) {
            if (!player.is_excused && games_participated == 0) {
                penalty += num_partial_queue;
            };
        } 
        // Checks non main roster penalty conditions (Gone for whole night, not a single 5q was player, one penalty for whole night)
        else {
            if (!player.is_excused && games_participated == 0 && num_full_queue == 0) {
                penalty += 1;
            }
        };
        
        console.log(player.player_id, "Games Participated: ", games_participated, "roster: ", is_main_roster, "penalty: ", penalty, "Excuse: ", player.is_excused)

        // Counts penalties for this month previously
        let penalized_absences = (await db.query("select absence_penalty from daily where player_id = $1 and extract(month from date) = $2", [player.player_id, date.getMonth() + 1])).rows
        let penalized_absence_count = 0;
        for (row of penalized_absences) {
            penalized_absence_count += row.absence_penalty;
        }

        // Adds new penalties and calculates point deduction
        for (i = 0; i < penalty; i++) {
            penalized_absence_count += 1
            absence_points -= penalized_absence_count
        }
        
        // Calculates notification deduction
        if (is_main_roster && !player.has_notified) {
            absence_points -= (await db.query("select has_notified from daily where player_id = $1 and extract(month from date) = $2 and has_notified = FALSE;", [player.player_id, date.getMonth() + 1])).rows.length + 1
        }
        
        // The actual deduction of absence points
        target_points.absence_pts += absence_points;
        
        let total_points = target_points.score_pts + target_points.game_pts + target_points.kill_pts + target_points.absence_pts + target_points.crit_pts + target_points.adr_pts + target_points.multikill_pts;
        
        console.log(target_points)

        // Anyone who isn't main roster will automatically be set to has_notified = TRUE (if they become main roster, no consequences)
        let final_has_notified;
        if (is_main_roster) {
            final_has_notified = player.has_notified;
        } else {
            final_has_notified = true;
        };
        
        // Uploads to database
        await db.uploadDaily(date, player.player_id, total_points, target_points.game_pts, target_points.kill_pts,
            target_points.score_pts, target_points.adr_pts, target_points.multikill_pts, target_points.crit_pts, target_points.absence_pts, 
            player.is_excused, final_has_notified, penalty);
    };
        
    // Responds with upload success (false if error)
    res.json({success: success});
})
        
module.exports = router;
