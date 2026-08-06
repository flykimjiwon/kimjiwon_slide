// 예약 시간 범위 검증

const MAX_HOURS = 4;
const MIN_MINUTES = 30;

module.exports = function checkTimeRange(req, res, next) {
  const { startAt, endAt } = req.body;
  const start = new Date(startAt);
  const end = new Date(endAt);

  if (Number.isNaN(start.getTime()) || Number.isNaN(end.getTime())) {
    return res.status(400).json({ message: '시간 형식이 올바르지 않습니다' });
  }
  if (end <= start) {
    return res.status(400).json({ message: '종료 시각이 시작보다 빠릅니다' });
  }

  const minutes = (end - start) / 60000;
  if (minutes < MIN_MINUTES) {
    return res.status(400).json({ message: `최소 ${MIN_MINUTES}분 이상이어야 합니다` });
  }
  if (minutes > MAX_HOURS * 60) {
    return res.status(400).json({ message: `1회 예약은 최대 ${MAX_HOURS}시간입니다` });
  }
  next();
};
