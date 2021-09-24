from app.services.base import BaseService
from app.models import Record as RecordModel
from app.logger import log
from app.serializers.records import (
    RecordCreation,
    RecordToUpdate,
    Record_Get_Pydantic,
)


class RecordService(BaseService):
    model = RecordModel
    create_schema = RecordCreation
    update_schema = RecordToUpdate
    get_schema = Record_Get_Pydantic

    async def create_record(
        self,
        record_data: RecordCreation,
    ) -> RecordModel:
        record = await RecordModel.create(
            customer_email=record_data.customer_email,
            customer_full_name=record_data.customer_full_name,
            customer_phone_number=record_data.customer_phone_number,
            time=record_data.time,
            proposition_id=record_data.proposition_id,
            user_id=record_data.user_id,
        )
        log(
            log.INFO,
            "Proposition %s has been created",
            record.id,
        ),
        return record
