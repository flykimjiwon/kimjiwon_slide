// 사번 기반 인증 확인

module.exports = function authGuard(req, res, next) {
  const empNo = req.header('X-Emp-No');
  if (!empNo) {
    return res.status(401).json({ message: '사번 헤더가 없습니다' });
  }
  if (!/^[0-9]{7}$/.test(empNo)) {
    return res.status(400).json({ message: '사번 형식이 올바르지 않습니다' });
  }
  req.user = { id: empNo };
  next();
};
