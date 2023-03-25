from sqlalchemy.sql import select

from models.sql.sql_models import PackageSql, SessionSql, TypeSql


def get_packages_query(**kwargs):
    session_id = kwargs.get('session_id')
    type_id = kwargs.get('type_id')
    page_number = kwargs.get('page_number')
    page_size = kwargs.get('page_size')
    cost_calculated = kwargs.get('cost_calculated')
    stmt = select(PackageSql, TypeSql.name.label('type_name')).join(
        SessionSql).join(TypeSql).where(SessionSql.id == session_id)  # noqa
    if type_id is not None:
        stmt = stmt.where(TypeSql.id == type_id)
    if cost_calculated:
        stmt = stmt.where(PackageSql.cost.isnot(None))
    stmt = stmt.limit(page_size).offset(page_size * page_number)
    return stmt
