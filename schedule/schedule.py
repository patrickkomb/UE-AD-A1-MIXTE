import grpc
from concurrent import futures
import schedule_pb2
import schedule_pb2_grpc
import json
import requests
from repository import get_repository
from env import MOVIES_SERVICE_URL

class ScheduleServicer(schedule_pb2_grpc.ScheduleServicer):

    def __init__(self):
        self.repo = get_repository()

    def GetScheduleByDate(self, request, context):
        schedules = self.repo.load()
        for schedule in schedules:
            if schedule['date'] == request.date:
                print("Schedule found")
                context.set_code(grpc.StatusCode.OK)
                context.set_details("Schedule found")
                return schedule_pb2.ScheduleData(date=schedule['date'], movies=schedule['movies'])
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details("Schedule date not found")
        return schedule_pb2.ScheduleData(date='', movies=[])

    def GetScheduleDetailsByDate(self, request, context):
        date = request.date
        schedules = self.repo.load()
        for schedule in schedules:
            if schedule["date"] == date:
                movies = []
                for movie_id in schedule["movies"]:
                    query = f"""
                    {{
                      movie_with_id(_id: "{movie_id}") {{
                        id
                        title
                        director
                        rating
                      }}
                    }}
                    """
                    resp = requests.post(MOVIES_SERVICE_URL, json={"query": query})
                    if resp.status_code == 200:
                        data = resp.json().get("data", {}).get("movie_with_id")
                        #print(data)
                        movie = schedule_pb2.MovieData(
                            id=data.get("id", ""),
                            title=data.get("title", ""),
                            director=data.get("director", ""),
                            rating=data.get("rating", ""),
                        )
                        #print(movie)
                        #print("----------------------")
                        movies.append(movie)

                if not movies:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details("No movies found for this schedule")
                    return schedule_pb2.ScheduleDetails()

                context.set_code(grpc.StatusCode.OK)
                return schedule_pb2.ScheduleDetails(
                    date=date,
                    movies=movies
                )

        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details("Schedule date not found")
        return schedule_pb2.ScheduleDetails(date="",movies=[])

    def AddSchedule(self, request, context):
        schedules = self.repo.load()

        for schedule in schedules:
            if schedule["date"] == request.date:
                context.set_code(grpc.StatusCode.ALREADY_EXISTS)
                context.set_details("Schedule date already exists")
                return schedule_pb2.ScheduleData(date='', movies=[])

        new_schedule = {
            "date": request.date,
            "movies": list(request.movies)
        }

        schedules.append(new_schedule)
        self.repo.save(schedules)

        context.set_code(grpc.StatusCode.OK)
        context.set_details("Schedule added")
        return schedule_pb2.ScheduleData(date=new_schedule['date'], movies=new_schedule['movies'])

    def DeleteSchedule(self, request, context):
        schedules = self.repo.load()
        for schedule in schedules:
            if schedule["date"] == request.date:
                schedules.remove(schedule)
                self.repo.save(schedules)
                context.set_code(grpc.StatusCode.OK)
                context.set_details("Schedule deleted")
                return schedule_pb2.Date(date=schedule["date"])

        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details("Schedule date not found")
        return schedule_pb2.Date(date='')

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    schedule_pb2_grpc.add_ScheduleServicer_to_server(ScheduleServicer(), server)
    server.add_insecure_port('[::]:3202')
    server.start()
    print("Server running in port 3202")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
