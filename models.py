from mongoengine import *


class AdminRegister(Document):
	userName = StringField()
	email = StringField()
	password = StringField()
	userLink = StringField()
	createdOn = DateTimeField()
	status = IntField(default=0)

class StudentRegister(Document):
	firstName = StringField()
	lastName = StringField()
	schoolName = StringField()
	gender = StringField()
	className = StringField()
	sectionName = StringField()
	rollNumber = StringField()
	dateOfBirth = StringField()
	phoneNumber = StringField()
	emailId = StringField()
	password = StringField()
	status = IntField()
	createdOn = DateTimeField()
	adminId =ReferenceField('AdminRegister')
	link = StringField()
	stageStatus=IntField()
	profilePic = StringField()
	stageExamOneStatus=IntField()
	stageExamTwoStatus=IntField()
	stageExamThreeStatus=IntField()
	levelOneTotalMarks = IntField()
	levelOneMarks1 = IntField()
	levelOneMarks2 = IntField()
	levelOneMarks3 = IntField()
	levelOneMarks4 = IntField()
	marksUpdatedStatus1=IntField()
	levelTwoTotalMarks = IntField()
	levelTwoMarks1 = IntField()
	levelTwoMarks2 = IntField()
	levelTwoMarks3 = IntField()
	levelTwoMarks4 = IntField()
	marksUpdatedStatus2=IntField()
	levelThreeTotalMarks = IntField()
	levelThreeMarks1 = IntField()
	levelThreeMarks2 = IntField()
	levelThreeMarks3 = IntField()
	levelThreeMarks4 = IntField()
	marksUpdatedStatus3=IntField()
	paperValidateStatus1=IntField()
	paperValidateStatus2=IntField()
	paperValidateStatus3=IntField()
	attemptedOnTaskOne=DateTimeField()
	attemptedOnTaskTwo=DateTimeField()
	attemptedOnTaskThree=DateTimeField()

	# totalMarks = IntField()
	# stageExamStatus=IntField()

class StageOne(Document):
	fullName = StringField()
	projectDescription = StringField()
	codeScreenshot = StringField()
	circuteDiagramScreenshot = StringField()
	finalProjectVideo = StringField()
	submittedOn = DateTimeField()
	stageStatus = IntField()
	studentId = ReferenceField('StudentRegister')
	stageOneMarks = IntField()
	status = IntField(default=1)
	createdOn = DateTimeField()
	emailId = StringField()

class StageTwo(Document):
	fullName = StringField()
	projectDescription = StringField()
	codeScreenshot = StringField()
	circuteDiagramScreenshot = StringField()
	finalProjectVideo = StringField()
	submittedOn = DateTimeField()
	stageStatus = IntField()
	studentId = ReferenceField('StudentRegister')
	stageOneMarks = IntField()
	status = IntField(default=1)
	createdOn = DateTimeField()
	emailId = StringField()

class StageThree(Document):
	fullName = StringField()
	projectDescription = StringField()
	codeScreenshot = StringField()
	circuteDiagramScreenshot = StringField()
	finalProjectVideo = StringField()
	submittedOn = DateTimeField()
	stageStatus = IntField()
	studentId = ReferenceField('StudentRegister')
	stageOneMarks = IntField()
	status = IntField(default=1)
	createdOn = DateTimeField()
	emailId = StringField()	


	 





