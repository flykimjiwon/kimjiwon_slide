// 회의실 라우터

const express = require('express');
const router = express.Router();

const OPEN_HOUR = 8;
const CLOSE_HOUR = 20;

router.get('/', async (req, res) => {
  const rooms = await req.db.query('SELECT * FROM rooms WHERE active = true ORDER BY code');
  res.json({ openHour: OPEN_HOUR, closeHour: CLOSE_HOUR, rooms: rooms.rows });
});

router.get('/:code', async (req, res) => {
  const one = await req.db.query('SELECT * FROM rooms WHERE code = $1', [req.params.code]);
  if (one.rowCount === 0) return res.status(404).json({ message: '없는 회의실' });
  res.json(one.rows[0]);
});

module.exports = router;
