from typing import Optional, List
from dataclasses import dataclass
import datetime
from google.protobuf.timestamp_pb2 import Timestamp
import dormyboba_api.v1api_pb2 as apiv1
from .dormyboba_user import DormybobaUser
from .. import model

@dataclass
class Queue:
    queue_id: int
    title: str
    description: Optional[str]
    open: datetime.datetime
    close: Optional[datetime.datetime]
    active_user: Optional[DormybobaUser]
    is_event_generated: bool

    @staticmethod
    def from_api(api_queue: apiv1.Queue) -> 'Queue':
        open = None if not(api_queue.HasField("open")) else api_queue.open.ToDatetime()  
        close = None if not(api_queue.HasField("close")) else api_queue.close.ToDatetime()  
        return Queue(
            queue_id=api_queue.queue_id,
            title=api_queue.title,
            description=api_queue.description,
            open=open,
            close=close,
        )
    
    def to_api(self) -> apiv1.Queue:
        open = None
        if self.open is not None:
            open = Timestamp()
            open.FromDatetime(self.open)

        close = None
        if self.close is not None:
            close = Timestamp()
            close.FromDatetime(self.close)

        return apiv1.Queue(
            queue_id=self.queue_id,
            title=self.title,
            description=self.description,
            open=open,
            close=close,
        )
    
    @staticmethod
    def from_model(model_queue: model.Queue) -> 'Queue':
        return Queue(
            queue_id=model_queue.queue_id,
            title=model_queue.title,
            description=model_queue.description,
            open=model_queue.open,
            close=model_queue.close,
            active_user=DormybobaUser.from_model(model_queue.active_user),
            is_event_generated=model_queue.is_event_generated,
        )
    
    def to_model(self) -> model.Queue:
        return model.Queue(
            queue_id=self.queue_id,
            title=self.title,
            description=self.description,
            open=self.open,
            close=self.close,
            active_user_id=self.active_user.user_id,
            is_event_generated=self.is_event_generated,
        )
    
@dataclass
class QueueEvent:
    queue: Queue
    users: List[DormybobaUser]

    def to_api(self) -> apiv1.QueueEvent:
        return apiv1.QueueEvent(
            queue=self.queue.to_api(),
            users=list([user.to_api() for user in self.users]),
        )