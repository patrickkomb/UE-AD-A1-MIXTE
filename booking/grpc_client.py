import grpc
import schedule_pb2
import schedule_pb2_grpc
from env import SCHEDULE_SERVICE_URL

def get_schedule_client():
    channel = grpc.insecure_channel(SCHEDULE_SERVICE_URL)
    stub = schedule_pb2_grpc.ScheduleStub(channel)
    return stub