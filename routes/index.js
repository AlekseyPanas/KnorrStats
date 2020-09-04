var express = require('express');
const db = require('../db/db');
const { response } = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', async (req, res, next) => {
  res.render('index', { title: 'Foo' });
});

/* Ajax call used by pygame client to retrieve player data */
router.get('/ajax/getplayers', async (req, res, next) => {
  let player_info = await db.getClientPlayerData();
  res.json(player_info);
});

/* Ajax call used by pygame client to retrieve map data */
router.get('/ajax/getmaps', async(req, res, next) => {
  let map_info = await db.getClientMapData();
  res.json(map_info);
});

module.exports = router;
