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

router.post('/ajax/upload_data', async(req, res, next) => {
  success = true;

  console.log(req.body)
  await db.getClientMapData().catch(async err => {
    success = false; return err
  });

  res.json({success: success});
})

module.exports = router;
