from src import db


class Test(db.Model):
	"""
	Test class
	--------------
	This class will contain all the information about the tests.
	"""
	__tablename__ = 'test'

	id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	name = db.Column(db.String(255), nullable = False)
	state = db.Column(db.Boolean, nullable = False)
	lesson = db.Column(db.String(255), db.ForeignKey('lesson.id', ondelete='CASCADE'), nullable = False)
	question = db.relationship("Question", backref = "test_question", cascade = 'save-update, merge, delete, delete-orphan', lazy = 'dynamic')
	
	def getId(self) :
		"""
		Getter of the id.
		Return : 
		----------
		Id
		"""
		return self.id

	def getName(self) :
		"""
		Getter of the name.
		Return : 
		----------
		Name
		"""
		return self.name

	def getState(self) :
		"""
		Getter of the state.
		Return : 
		----------
		State
		"""
		return self.state

	def getLesson(self) :
		"""
		Getter of the lesson.
		Return : 
		----------
		Lesson
		"""
		return self.lesson

	def setName(self, name) :
		"""
		Setter of the name in the database.
		"""
		self.name = name
		db.session.commit()

	def setState(self, state) :
		"""
		Setter of the state in the database.
		"""
		self.state = state
		db.session.commit()

	def setLesson(self, lesson) :
		"""
		Setter of the lesson in the database.
		"""
		self.lesson = lesson
		db.session.commit()
