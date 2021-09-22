from typing import Optional
from tortoise.query_utils import Q
from fastapi import HTTPException, status

from app.services import BaseService, AuthService
from app.models import Proposition as PropositionModel
from app.logger import log
from app.serializers.propositions import (
    PropositionCreation,
    PropositionToUpdate,
    User_Get_Pydantic,
)


class PropositionService(BaseService):
    model = PropositionModel
    create_schema = PropositionCreation
    update_schema = PropositionToUpdate
    get_schema = User_Get_Pydantic

    async def create_proposition(
        self, proposition_data: PropositionCreation
    ) -> PropositionModel:
        proposition = await PropositionModel.create(
            name=proposition_data.name,
            price=proposition_data.price,
            job_time=proposition_data.job_time,
        )
        log(
            log.INFO,
            "Proposition %s has been created",
            proposition_data.name,
        ),
        return proposition
