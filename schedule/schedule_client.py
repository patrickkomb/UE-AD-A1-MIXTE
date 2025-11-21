import grpc
import schedule_pb2
import schedule_pb2_grpc
from env import SCHEDULE_SERVICE_URL


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel(SCHEDULE_SERVICE_URL) as channel:
        stub = schedule_pb2_grpc.ScheduleStub(channel)

        print("-------------- AddSchedule --------------")
        new_schedule = schedule_pb2.ScheduleData(
            date="19690721",
            movies=["96798c08-d19b-4986-a05d-7da856efb697", "a8034f44-aee4-44cf-b32c-74cf452aaaae"]
        )
        try:
            resp = stub.AddSchedule(new_schedule)
            print(resp)
        except grpc.RpcError as e:
            print("Error:", e.code(), e.details())

        print("-------------- GetScheduleByDate --------------")
        date = schedule_pb2.Date(date="19690721")
        try:
            schedule = stub.GetScheduleByDate(date)
            print(schedule)
        except grpc.RpcError as e:
            print("Error:", e.code(), e.details())

        print("-------------- GetScheduleDetailsByDate --------------")
        date = schedule_pb2.Date(date="19690721")
        try:
            schedule_details = stub.GetScheduleDetailsByDate(date)
            print(schedule_details)
        except grpc.RpcError as e:
            print("Error:", e.code(), e.details())

        print("-------------- DeleteSchedule --------------")
        try:
            date = schedule_pb2.Date(date="19690721")
            deleted = stub.DeleteSchedule(date)
            print(deleted)
        except grpc.RpcError as e:
            print("Error:", e.code(), e.details())

    channel.close()

if __name__ == '__main__':
    run()
