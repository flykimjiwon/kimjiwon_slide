// 예약 라우터

const express = require('express');
const bookingService = require('../services/booking-service');
const checkTimeRange = require('./middleware/time-range-check');

const router = express.Router();

router.get('/', async (req, res) => {
  const rows = await bookingService.listByUser(req.user.id);
  res.json(rows);
});

router.post('/', checkTimeRange, async (req, res) => {
  const result = await bookingService.create(req.user.id, req.body);
  if (result.error) return res.status(409).json({ message: result.error });
  res.status(201).json(result.reservation);
});

router.delete('/:id', async (req, res) => {
  await bookingService.cancel(req.user.id, req.params.id);
  res.status(204).end();
});

module.exports = router;
