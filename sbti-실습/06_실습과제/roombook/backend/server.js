// roombook 백엔드 진입점

const express = require('express');
const reservationRouter = require('./routes/reservation-router');
const roomRouter = require('./routes/room-router');
const authGuard = require('./routes/middleware/auth-guard');
const rateLimiter = require('./routes/middleware/rate-limiter');

const app = express();
const PORT = process.env.PORT || 8080;

app.use(express.json());
app.use(rateLimiter);
app.use('/api/v2', authGuard);
app.use('/api/v2/reservations', reservationRouter);
app.use('/api/v2/rooms', roomRouter);

app.get('/healthz', (req, res) => res.json({ ok: true, version: '0.4.2' }));

app.listen(PORT, () => console.log(`roombook api on :${PORT}`));
