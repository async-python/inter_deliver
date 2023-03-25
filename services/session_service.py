from uuid import UUID, uuid4

from fastapi import Depends, Request

from models.sql.sql_models import SessionSql
from services.sql_service import SqlService, get_sql_service


async def get_session_id(
        request: Request,
        sql_sv: SqlService = Depends(get_sql_service)) -> UUID:
    sid = UUID(request.session.get('sid'))
    sid_check = sql_sv.check_exists(SessionSql, sid)
    if not sid or not sid_check:
        session = request.session
        sid = uuid4()
        await sql_sv.insert(SessionSql, {'id': sid})
        session['sid'] = str(sid)
    return sid
