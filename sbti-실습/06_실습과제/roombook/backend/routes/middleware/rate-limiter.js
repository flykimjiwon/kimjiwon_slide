// 아주 단순한 요청 제한기 (메모리 기반)

const WINDOW_MS = 60 * 1000;
const MAX_REQUESTS = 60;

const hits = new Map();

module.exports = function rateLimiter(req, res, next) {
  const key = req.header('X-Emp-No') || req.ip;
  const now = Date.now();
  const bucket = hits.get(key) || { count: 0, resetAt: now + WINDOW_MS };

  if (now > bucket.resetAt) {
    bucket.count = 0;
    bucket.resetAt = now + WINDOW_MS;
  }
  bucket.count += 1;
  hits.set(key, bucket);

  if (bucket.count > MAX_REQUESTS) {
    return res.status(429).json({ message: '요청이 너무 많습니다' });
  }
  next();
};
