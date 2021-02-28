from flask import Flask,request,jsonify
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 
import json

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

SUCCESS_DATA_REQUEST = """ {
					'code' : 200,
					'description' : 'Action Successful OK',
					'data' : """

INVALID_REQUEST = {
					'code' : 400,
					'description' : 'Bad Request'
					}

SUCCESS_REQUEST = {
					'code' : 200,
					'description' : 'Action Successful OK'
					}

INTERNAL_ERROR = {
					'code' : 500,
					'description' : 'Internal Server Error'
					}

class Song(db.Model):
    __tablename__ = 'Song'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    upload_time = db.Column(db.String(100), nullable=False)

    def json(self):
    	return {
    		'id' : self.id,
    		'name' : self.name,
    		'duration' : self.duration,
    		'upload_time' : self.upload_time
    	}
    def __repr__(self):
    	return f"Audio(id = {self.id},name = {self.name}, duration = {self.duration}, upload_time = {self.upload_time})"


class AudioBook(db.Model):
    __tablename__ = 'AudioBook'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    upload_time = db.Column(db.Integer, nullable=False)
    narrator = db.Column(db.String(100), nullable=False)

    def json(self):
    	return {
    		'id' : self.id,
    		'name' : self.name,
    		'duration' : self.duration,
    		'upload_time' : self.upload_time,
    		'author' : self.author,
    		'narrator' : self.narrator
    	}

    def __repr__(self):
    	return f"Audio(id = {self.id},name= {self.name}, time= {self.upload_time}, Duration= {self.duration}, Type = AudioBook)"
	
class Podcast(db.Model):
    __tablename__ = 'Podcast'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    host = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    upload_time = db.Column(db.Integer, nullable=False)
    participants = db.Column(db.String(1000), nullable=False)

    def json(self):
    	return {
    		'id' : self.id,
    		'name' : self.name,
    		'duration' : self.duration,
    		'upload_time' : self.upload_time,
    		'host' : self.host,
    		'participants' : self.participants
    	}

    def __repr__(self):
    	return f"Audio(id = {self.id},name= {self.name}, time= {self.upload_time}, Duration= {self.duration} , Type = Podcast)"
# Run this only the first time, then comment it out
db.create_all()
#---------------------------------------------------#
class Upload_Audio_API(Resource): 
	
	def put(self):
		data = request.json
		data = json.loads(data)
		try:
			TYPE = data['type']
			DATA = data['data']
		except:
			return(INVALID_REQUEST)
		if(TYPE and DATA):
			if(TYPE.lower() == "song"):
				metadata = data['data']
				try:
					name = metadata['name']
					upload_time = metadata['upload_time']
					duration = metadata['duration']
				except:
					return(INVALID_REQUEST)

				if(name and upload_time and duration):
					try:
						song = Song(name = name,upload_time = upload_time,duration = duration)
						db.session.add(song)
						db.session.commit()
						return(SUCCESS_REQUEST)
					except:
						return(INTERNAL_ERROR)
				return(INVALID_REQUEST)
					
			if(TYPE.lower() == "podcast"):
				metadata = data['data']
				try:
					name = metadata['name']
					upload_time = metadata['upload_time']
					duration = metadata['duration']
					host = metadata['host']
				except:
					return(INVALID_REQUEST)
				try:
					participants = metadata['participants']
				except:
					participants = 0
				if(name and upload_time and duration and host and participants):
					try:
						podcast = Podcast(name = name,upload_time = upload_time,duration = duration,host = host	,participants = participants)
						db.session.add(podcast)
						db.session.commit()
						return(SUCCESS_REQUEST)
					except:
						return(INTERNAL_ERROR)
				elif(name and upload_time and duration and host):
					try:
						podcast = Podcast(name = name,upload_time = upload_time,duration = duration,host = host, participants = 0)
						db.session.add(podcast)
						db.session.commit()
						return(SUCCESS_REQUEST)
					except:
						return(INTERNAL_ERROR)
				return(INVALID_REQUEST)

			if(TYPE.lower() == "audiobook"):
				metadata = data['data']
				try:
					name = metadata['name']
					upload_time = metadata['upload_time']
					duration = metadata['duration']
					author = metadata['author']
					narrator = metadata['narrator']
				except:
					return(INVALID_REQUEST)
				if(name and upload_time and duration and author and narrator):
					try:
						audiobook = AudioBook(name = name,upload_time = upload_time, duration = duration, author = author, narrator = narrator)
						db.session.add(audiobook)
						db.session.commit()
						return(SUCCESS_REQUEST)
					except Exception as e:
						return (INTERNAL_ERROR)
				return(INVALID_REQUEST)
		else:
			return(INVALID_REQUEST)
class Audio_Functional_API(Resource):
	def get(self,TYPE,id = None):
		if(TYPE == "song"):
			if(id):
				data = Song.query.get(id)
				response = SUCCESS_DATA_REQUEST + json.dumps(data.json())
				return(response)
			else:
				data = Song.query.all()
				response = []
				for dat in data:
					response.append(dat.json())
				response = json.dumps(response)
				response = SUCCESS_DATA_REQUEST + response
				return(response)
			return(INVALID_REQUEST)
		if(TYPE == "audiobook"):
			if(id):
				data = AudioBook.query.get(id)
				response = SUCCESS_DATA_REQUEST + json.dumps(data.json())
				return(response)
			else:
				data = AudioBook.query.all()
				response = []
				for dat in data:
					response.append(dat.json())
				response = json.dumps(response)
				response = SUCCESS_DATA_REQUEST + response
				return(response)
			return(INVALID_REQUEST)
		if(TYPE == "podcast"):
			if(id):
				data = Podcast.query.get(id)
				response = SUCCESS_DATA_REQUEST + json.dumps(data.json())
				return(response)
			else:
				data = Podcast.query.all()
				response = []
				for dat in data:
					response.append(dat.json())
				response = json.dumps(response)
				response = SUCCESS_DATA_REQUEST + response
				return(response)
			return(INVALID_REQUEST)

	def delete(self,TYPE,id = None):
		if(TYPE == "song"):
			if(id):
				data = Song.query.get(id)
				print(data)
				try:
					db.session.delete(data)
					db.session.commit()
					return (SUCCESS_REQUEST)
				except:
					return(INTERNAL_ERROR)
			else:
				return(INVALID_REQUEST)
		if(TYPE == "audiobook"):
			if(id):
				data = AudioBook.query.get(id)
				print(data)
				try:
					db.session.delete(data)
					db.session.commit()
					return (SUCCESS_REQUEST)
				except:
					return(INTERNAL_ERROR)
			else:
				return(INVALID_REQUEST)
		if(TYPE == "podcast"):
			if(id):
				data = Podcast.query.get(id)
				print(data)
				try:
					db.session.delete(data)
					db.session.commit()
					return (SUCCESS_REQUEST)
				except:
					return(INTERNAL_ERROR)
			else:
				return(INVALID_REQUEST)
		return(INVALID_REQUEST)

	def patch(self,TYPE,id):
		data = request.json
		data = json.loads(data)
		metadata = data['data']
		if(TYPE == "song"):
			if(id):
				try:
					result = Song.query.get(id)
				except:
					return(INVALID_REQUEST)
				if(result):
					try:
						result.name = metadata['name']
						result.duration = metadata['duration']
						result.upload_time = metadata['upload_time']
						db.session.add(result)
						db.session.commit()
						return(SUCCESS_DATA_REQUEST + json.dumps(result.json()))
					except:
						return(INTERNAL_ERROR)
				return (INVALID_REQUEST)
			else:
				return(INVALID_REQUEST)
		if(TYPE == "audiobook"):
			if(id):
				result = AudioBook.query.get(id)
				if(result):
					try:
						result.name = metadata['name']
						result.duration = metadata['duration']
						result.upload_time = metadata['upload_time']
						result.author = metadata['author']
						result.narrator = metadata['narrator']
						db.session.add(result)
						db.session.commit()
						return(SUCCESS_DATA_REQUEST + json.dumps(result.json()))
					except:
						return(INTERNAL_ERROR)
				return (INVALID_REQUEST)
			else:
				return(INVALID_REQUEST)
		if(TYPE == "podcast"):
			if(id):
				result = Podcast.query.get(id)
				if(result):
					try:
						result.name = metadata['name']
						result.duration = metadata['duration']
						result.upload_time = metadata['upload_time']
						result.host = metadata['host']
						try:
							result.participants = metadata['participants']
						except Exception as e:
							print(e)
						db.session.add(result)
						db.session.commit()
						return(SUCCESS_DATA_REQUEST + json.dumps(result.json()))
					except:
						return(INTERNAL_ERROR)
				return(INVALID_REQUEST)
			else:
				return(INVALID_REQUEST)


api.add_resource(Upload_Audio_API, "/upload")

routes = [
    "/<string:TYPE>/<int:id>",
    "/<string:TYPE>/",
]


api.add_resource(Audio_Functional_API, *routes)

if __name__ == "__main__":
	app.run(debug=True)
