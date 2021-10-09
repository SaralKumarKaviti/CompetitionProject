from flask import Flask,render_template,request, flash,redirect, url_for, jsonify
from config import client
from models import *
import secrets
import datetime
import json
#from flask_mail import Mail,Message
from bson import ObjectId
import os

app = Flask(__name__)

app.secret_key='super_secret_key'

# app.config['MAIL_SERVER']='smtp.gmail.com'
# app.config['MAIL_PORT']=465
# app.config['MAIL_USERNAME']='saralkumar28@gmail.com'
# app.config['MAIL_PASSWORD']='momdadanu2328'
# app.config['MAIL_USE_TLS']=False
# app.config['MAIL_USE_SSL']=True

UPLOAD_FOLDER = 'static/uploads/profilePic'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','mp4'}

# mail=Mail(app)


@app.route("/",methods=['POST','GET'])
def studentRegisterPage():
    firstName = request.form.get("firstName")
    lastName = request.form.get("lastName")
    schoolName = request.form.get("schoolName")
    gender = request.form.get("gender")
    className = request.form.get("className")
    sectionName = request.form.get("sectionName")
    rollNumber = request.form.get("rollNumber")
    dateOfBirth = request.form.get("dateOfBirth")
    phoneNumber = request.form.get("phoneNumber")
    emailId = request.form.get("emailId")
    password = request.form.get("password")
    status = 0
    createdOn = datetime.datetime.now()
    adminId ="61541cf9428b7e5f06f97bff"
    link = secrets.token_urlsafe()
    student_login_data={}

    if firstName and lastName and schoolName and gender and className and sectionName and rollNumber and dateOfBirth and phoneNumber and emailId and password and request.method == "POST":
        try:

            queryset = StudentRegister.objects(emailId__iexact=emailId)
            if queryset:
                flash("Email already Exists!!!")
                return render_template("student/register.html")
        except Exception as e:
            pass
        student_register = StudentRegister(
            firstName=firstName,
            lastName=lastName,
            schoolName=schoolName,
            gender=gender,
            className=className,
            sectionName=sectionName,
            rollNumber=rollNumber,
            dateOfBirth=dateOfBirth,
            phoneNumber=phoneNumber,
            emailId=emailId,
            password=password,
            status=status,
            createdOn=createdOn,
            adminId=adminId,
            link=link
            )
        student_register_data = student_register.save()
        register_id=str(student_register_data.id)
        if register_id:
            profilePic = request.files['profilePic']
            if profilePic.filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS:
                ext = profilePic.filename.rsplit('.',1)[1].lower()
                file_name = str(register_id)+"."+ext
                if not os.path.exists(app.config['UPLOAD_FOLDER']):
                    os.mkdir(app.config['UPLOAD_FOLDER'])
                profile = app.config['UPLOAD_FOLDER']
                profilePic.save(os.path.join(profile,file_name))
                # print("----------------")
            student_register_data.update(profilePic=file_name)
        if student_register_data:
            # student_login_data={
            #     "firstName":student_register_data.firstName,
            #     "lastName" : student_register_data.lastName,
            #     "link":student_register_data.link,
            #     "emailId":student_register_data.emailId,
            #     "password":student_register_data.password
            # }
            # if True:
            #     msg=Message('Welcome to Coding Academy',sender='saralkumar28@gmail.com',recipients=[student_register_data.emailId])
            #     msg.html=render_template("student/email_temp.html",student_login_data=student_login_data)
            #     mail.send(msg)
            flash("Registration Successfully Completed!!!.")
            return redirect(url_for('studentLoginPage'))
        else:
            flash("Required fields are missing!!!")
            return render_template("student/register.html")    
    else:
        return render_template("student/register.html")
@app.route("/AdminRegistration",methods=['POST'])
def adminRegistrationPage():
    userName = request.json['userName']
    email = request.json['email']
    password = request.json['password']
    userLink = secrets.token_urlsafe()
    createdOn = datetime.datetime.now()
    status = 1
    
    data_status={"responseStatus":0,"result":""}

    if request.method=="POST":
        adminData=AdminRegister(
            userName=userName,
            email=email,
            password=password,
            createdOn=createdOn,
            status=status,
            userLink=userLink
            )

        adminSavedData=adminData.save()
        if adminSavedData:
            data_status["responseStatus"]=1
            data_status["result"]="Successfully completed registration"
            return data_status
    else:
        data_status["responseStatus"]=0
        data_status["result"]="Required Fields are missing"
        return data_status

@app.route("/StudentLogin",methods=['POST','GET'])
def studentLoginPage():
    emailId = request.form.get("emailId")
    password = request.form.get("password")
    if emailId and password and request.method=="POST":
        try:
            student_details=StudentRegister.objects.get(emailId__iexact=emailId,password__exact=password,status__in=[0,1,2,3])
            if student_details:
                link=student_details.link
                # data={
                #     "firstName":student_details.firstName,
                #     # "link"
                # }
                return redirect(url_for('studentExamPage',link=link))

            else:
                flash("Invalid Credentials!!!")
                return render_template("student/login.html")
        except StudentRegister.DoesNotExist as e:
            # raise e
            flash("Invalid Credentials!!")
            return render_template("student/login.html")
    else:
        return render_template("student/login.html")

@app.route('/StudentForgetPassword',methods=['POST','GET'])
def studentForgetPasswordPage():
    emailId = request.form.get("emailId")
    newPassword = request.form.get("newPassword")
    confirmPassword = request.form.get("confirmPassword")
    

    if emailId and newPassword and confirmPassword and request.method=="POST":
        if newPassword==confirmPassword:
            get_student_info = StudentRegister.objects.get(emailId=emailId)
            # print(get_student_info["emailId"])
            if get_student_info.emailId:
                updated_password=get_student_info.update(
                    password=newPassword
                    )
                if updated_password:
                    flash("Password Successfully updated")
                    return redirect(url_for('studentLoginPage'))
            
        else:
            flash("Password Miss Matched")
            return render_template('student/forget_password.html')
    else:
        return render_template('student/forget_password.html')

            
@app.route('/uploads/<filename>')
def send_uploaded_file(filename=''):
    from flask import send_from_directory
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.route("/StudentExam/<link>",methods=['POST','GET'])
def studentExamPage(link):
    if request.method=="GET":
        try:
            student_info=StudentRegister.objects.get(link=link)
            if student_info:
                student_info_dict={
                    "firstName":student_info.firstName,
                    "lastName":student_info.lastName,
                    "sectionName":student_info.sectionName,
                    "rollNumber":student_info.rollNumber,
                    "schoolName":student_info.schoolName,
                    "gender":student_info.gender,
                    "dateOfBirth":student_info.dateOfBirth,
                    "phoneNumber":student_info.phoneNumber,
                    "emailId":student_info.emailId,
                    "stageExamOneStatus":student_info.stageExamOneStatus,
                    "stageExamTwoStatus":student_info.stageExamTwoStatus,
                    "stageExamThreeStatus":student_info.stageExamThreeStatus,
                    "profilePic":student_info.profilePic
                }
        except StudentRegister.DoesNotExist:
            
            return "Invalid link,please login once again"
                    
        
    # return redirect(url_for('studentWriteExamPage',link=link,student=student_info_dict))    
    return render_template("student/student_profile.html",link=link,student=student_info_dict)

@app.route("/StudentWriteExamStageOne/<link>",methods=['POST','GET'])
def studentWriteExamStageOnePage(link):
    
    projectDescription = request.form.get("projectDescription")
    stageStatus = 1
    submittedOn= datetime.datetime.now()
    status = 1
    createdOn = datetime.datetime.now()
    student_data=StudentRegister.objects.get(link=link)
    emailId = student_data.emailId
    data={}
    if projectDescription and request.method=="POST":
        try:
            queryset = StageOne.objects(emailId__iexact=emailId)
            if queryset:
                flash("Already submitted your task..")
                return render_template("student/tasksheet.html")
        except Exception as e:
            pass
        task_one_submitted=StageOne(
            fullName = student_data.firstName+" "+student_data.lastName,
            projectDescription=projectDescription,
            submittedOn = submittedOn,
            stageStatus=stageStatus,
            studentId=ObjectId(student_data.id),
            status=status,
            createdOn=createdOn,
            emailId = emailId
            )
        task_one_submitted_data = task_one_submitted.save()
        register_id=str(task_one_submitted_data.id)
        if register_id:
            codeScreenshot = request.files['codeScreenshot']
            circuteDiagramScreenshot = request.files['circuteDiagramScreenshot']
            finalProjectVideo = request.files['finalProjectVideo']
            if codeScreenshot.filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS and circuteDiagramScreenshot.filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS and finalProjectVideo.filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS:
                ext = codeScreenshot.filename.rsplit('.',1)[1].lower()
                ext1 = circuteDiagramScreenshot.filename.rsplit('.',1)[1].lower()
                ext2 = finalProjectVideo.filename.rsplit('.',1)[1].lower()
                file_name = str(register_id)+"."+ext
                file_name1 = str(register_id)+"circutediagram"+"."+ext1
                file_name2 = str(register_id)+"finalprojectvideo"+"."+ext2

                if not os.path.exists(app.config['UPLOAD_FOLDER']):
                    os.mkdir(app.config['UPLOAD_FOLDER'])
                codescreenshot = app.config['UPLOAD_FOLDER']
                circutediagram = app.config['UPLOAD_FOLDER']
                finalproject = app.config['UPLOAD_FOLDER']
                codeScreenshot.save(os.path.join(codescreenshot,file_name))
                circuteDiagramScreenshot.save(os.path.join(circutediagram,file_name1))
                finalProjectVideo.save(os.path.join(finalproject,file_name2))
            task_one_submitted_data.update(codeScreenshot=file_name,circuteDiagramScreenshot=file_name1,finalProjectVideo=file_name2)
            status=1
            stageExamOneStatus=1
            attemptedOnTaskOne = datetime.datetime.now()
            exam_status=StudentRegister.objects.get(link=link)
            if exam_status:
               exam_status_data=exam_status.update(status=status,stageExamOneStatus=stageExamOneStatus,attemptedOnTaskOne=attemptedOnTaskOne)
               # print(exam_status_data["stageExamStatus"])
               flash("Task one completed.")
               return redirect(url_for('studentExamPage',link=link))

    else:
        return render_template("student/tasksheet.html",link=link,data=data)

@app.route("/StudentWriteExamStageTwo/<link>",methods=['POST','GET'])
def studentWriteExamStageTwoPage(link):
    projectDescription = request.form.get("projectDescription")
    stageStatus = 1
    submittedOn= datetime.datetime.now()
    status = 1
    createdOn = datetime.datetime.now()
    student_data=StudentRegister.objects.get(link=link)
    emailId = student_data.emailId
    data={}
    if projectDescription and request.method=="POST":
        try:
            queryset = StageTwo.objects(emailId__iexact=emailId)
            if queryset:
                flash("Already submitted your task..")
                return render_template("student/tasksheet2.html")
        except Exception as e:
            pass
        task_one_submitted=StageTwo(
            fullName = student_data.firstName+" "+student_data.lastName,
            projectDescription=projectDescription,
            submittedOn = submittedOn,
            stageStatus=stageStatus,
            studentId=ObjectId(student_data.id),
            status=status,
            createdOn=createdOn,
            emailId = emailId
            )
        task_one_submitted_data = task_one_submitted.save()
        register_id=str(task_one_submitted_data.id)
        if register_id:
            codeScreenshot = request.files['codeScreenshot']
            circuteDiagramScreenshot = request.files['circuteDiagramScreenshot']
            finalProjectVideo = request.files['finalProjectVideo']
            if codeScreenshot.filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS and circuteDiagramScreenshot.filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS and finalProjectVideo.filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS:
                ext = codeScreenshot.filename.rsplit('.',1)[1].lower()
                ext1 = circuteDiagramScreenshot.filename.rsplit('.',1)[1].lower()
                ext2 = finalProjectVideo.filename.rsplit('.',1)[1].lower()
                file_name = str(register_id)+"."+ext
                file_name1 = str(register_id)+"circutediagram"+"."+ext1
                file_name2 = str(register_id)+"finalprojectvideo"+"."+ext2

                if not os.path.exists(app.config['UPLOAD_FOLDER']):
                    os.mkdir(app.config['UPLOAD_FOLDER'])
                codescreenshot = app.config['UPLOAD_FOLDER']
                circutediagram = app.config['UPLOAD_FOLDER']
                finalproject = app.config['UPLOAD_FOLDER']
                codeScreenshot.save(os.path.join(codescreenshot,file_name))
                circuteDiagramScreenshot.save(os.path.join(circutediagram,file_name1))
                finalProjectVideo.save(os.path.join(finalproject,file_name2))
            task_one_submitted_data.update(codeScreenshot=file_name,circuteDiagramScreenshot=file_name1,finalProjectVideo=file_name2)
            status=2
            stageExamTwoStatus=1
            attemptedOnTaskTwo=datetime.datetime.now()
            exam_status=StudentRegister.objects.get(link=link)
            if exam_status:
               exam_status_data=exam_status.update(status=status,stageExamTwoStatus=stageExamTwoStatus,attemptedOnTaskTwo=attemptedOnTaskTwo)
               # print(exam_status_data["stageExamStatus"])
               flash("Task Two completed.")
               return redirect(url_for('studentExamPage',link=link))

    else:
        return render_template("student/tasksheet2.html",link=link,data=data)

@app.route("/StudentWriteExamStageThree/<link>",methods=['POST','GET'])
def studentWriteExamStageThreePage(link):
    projectDescription = request.form.get("projectDescription")
    stageStatus = 1
    submittedOn= datetime.datetime.now()
    status = 1
    createdOn = datetime.datetime.now()
    student_data=StudentRegister.objects.get(link=link)
    emailId=student_data.emailId
    data={}
    if projectDescription and request.method=="POST":
        try:
            queryset = StageThree.objects(emailId__iexact=emailId)
            if queryset:
                flash("Already submitted your task..")
                return render_template("student/tasksheet3.html")
        except Exception as e:
            pass
        task_one_submitted=StageThree(
            fullName = student_data.firstName+" "+student_data.lastName,
            projectDescription=projectDescription,
            submittedOn = submittedOn,
            stageStatus=stageStatus,
            studentId=ObjectId(student_data.id),
            status=status,
            createdOn=createdOn,
            emailId = emailId
            )
        task_one_submitted_data = task_one_submitted.save()
        register_id=str(task_one_submitted_data.id)
        if register_id:
            codeScreenshot = request.files['codeScreenshot']
            circuteDiagramScreenshot = request.files['circuteDiagramScreenshot']
            finalProjectVideo = request.files['finalProjectVideo']
            if codeScreenshot.filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS and circuteDiagramScreenshot.filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS and finalProjectVideo.filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS:
                ext = codeScreenshot.filename.rsplit('.',1)[1].lower()
                ext1 = circuteDiagramScreenshot.filename.rsplit('.',1)[1].lower()
                ext2 = finalProjectVideo.filename.rsplit('.',1)[1].lower()
                file_name = str(register_id)+"."+ext
                file_name1 = str(register_id)+"circutediagram"+"."+ext1
                file_name2 = str(register_id)+"finalprojectvideo"+"."+ext2

                if not os.path.exists(app.config['UPLOAD_FOLDER']):
                    os.mkdir(app.config['UPLOAD_FOLDER'])
                codescreenshot = app.config['UPLOAD_FOLDER']
                circutediagram = app.config['UPLOAD_FOLDER']
                finalproject = app.config['UPLOAD_FOLDER']
                codeScreenshot.save(os.path.join(codescreenshot,file_name))
                circuteDiagramScreenshot.save(os.path.join(circutediagram,file_name1))
                finalProjectVideo.save(os.path.join(finalproject,file_name2))
            task_one_submitted_data.update(codeScreenshot=file_name,circuteDiagramScreenshot=file_name1,finalProjectVideo=file_name2)
            status=3
            stageExamThreeStatus=1
            attemptedOnTaskThree=datetime.datetime.now()
            exam_status=StudentRegister.objects.get(link=link)
            if exam_status:
               exam_status_data=exam_status.update(status=status,stageExamThreeStatus=stageExamThreeStatus,attemptedOnTaskThree=attemptedOnTaskThree)
               # print(exam_status_data["stageExamStatus"])
               flash("Task Three completed.")
               return redirect(url_for('studentExamPage',link=link))

    else:
        return render_template("student/tasksheet3.html",link=link)                

@app.route("/AdminLogin",methods=['POST','GET'])
def adminLoginPage():
    email = request.form.get("email")
    password = request.form.get("password")
    if email and password and request.method=="POST":
        try:
            admin_data=AdminRegister.objects.get(email__iexact=email,password__exact=password,status__in=[1])
            if admin_data:
                # return redirect(url_for('adminDashboardPage'))
                return redirect(url_for('adminDashboard'))

            else:
                flash("Invalid Credentials!!!")
                return render_template("admin/login.html")
        except AdminRegister.DoesNotExist as e:
            # raise e
            flash("Invalid Credentials!!")
            return render_template("admin/login.html")
    else:
        return render_template("admin/login.html")
    

# @app.route("/AdminDashboard",methods=['POST','GET'])
# def adminDashboardPage():
#     total_students_list=[]

#     registered_student = StudentRegister.objects(status__in=[0,1,2,3]).count()
#     stage_one_count = StudentRegister.objects(status__in=[1]).count()
#     stage_two_count = StudentRegister.objects(status__in=[2]).count()
#     stage_three_count = StudentRegister.objects(status__in=[3]).count()
#     total_completed = StudentRegister.objects(status__in=[3]).count()
#     total_dict={
#         "registeredStudent":registered_student,
#         "stageOne":stage_one_count,
#         "stageTwo":stage_two_count,
#         "stageThree":stage_three_count,
#         "totalCompleted":total_completed
#     }
#     total_students = StudentRegister.objects(status__in=[0,1,2,3])
#     if total_students:
#         for tcs in total_students:
#             students_dict={
#                 "firstName":tcs.firstName,
#                 "lastName":tcs.lastName,
#                 "className":tcs.className,
#                 "status":tcs.status,
                
#             }
#             total_students_list.append(students_dict)
#     return render_template("admin/dashboard/index.html",countData=total_dict,total_data=total_students_list)
    
@app.route("/StageOneData",methods=['POST','GET'])
def stageOneDataPage():
    total_students_list=[]

    registered_student = StudentRegister.objects(status__in=[0,1,2,3]).count()
    stage_one_count = StudentRegister.objects(stageExamOneStatus__in=[1]).count()
    stage_two_count = StudentRegister.objects(stageExamTwoStatus__in=[1]).count()
    stage_three_count = StudentRegister.objects(stageExamThreeStatus__in=[1]).count()
    total_completed = StudentRegister.objects(status__in=[3]).count()
    admin_data = AdminRegister.objects.get(status__in=[1])

    admin_dict={
        "userName":admin_data.userName,
        "email":admin_data.email
    }

    total_dict={
        "registeredStudent":registered_student,
        "stageOne":stage_one_count,
        "stageTwo":stage_two_count,
        "stageThree":stage_three_count,
        "totalCompleted":total_completed
    }
    total_students = StudentRegister.objects(stageExamOneStatus__in=[1])
    if total_students:
        for tcs in total_students:
            students_dict={
                "firstName":tcs.firstName,
                "lastName":tcs.lastName,
                "className":tcs.className,
                "status":tcs.status,
                "link":tcs.link,
                "levelOneMarks1":tcs.levelOneMarks1,
                "levelOneMarks2":tcs.levelOneMarks2,
                "levelOneMarks3":tcs.levelOneMarks3,
                "levelOneMarks4":tcs.levelOneMarks4,
                "levelOneTotalMarks":tcs.levelOneTotalMarks,
                "stageExamOneStatus":tcs.stageExamOneStatus,
                "paperValidateStatus1":tcs.paperValidateStatus1
                
            }
            total_students_list.append(students_dict)
    return render_template("admin/stage_one.html",countData=total_dict,total_data=total_students_list,admin_data=admin_dict)


@app.route("/StageTwoData",methods=['POST','GET'])
def stageTwoDataPage():
    total_students_list=[]

    registered_student = StudentRegister.objects(status__in=[0,1,2,3]).count()
    stage_one_count = StudentRegister.objects(stageExamOneStatus__in=[1]).count()
    stage_two_count = StudentRegister.objects(stageExamTwoStatus__in=[1]).count()
    stage_three_count = StudentRegister.objects(stageExamThreeStatus__in=[1]).count()
    total_completed = StudentRegister.objects(status__in=[3]).count()
    admin_data = AdminRegister.objects.get(status__in=[1])

    admin_dict={
        "userName":admin_data.userName,
        "email":admin_data.email
    }
    total_dict={
        "registeredStudent":registered_student,
        "stageOne":stage_one_count,
        "stageTwo":stage_two_count,
        "stageThree":stage_three_count,
        "totalCompleted":total_completed
    }
    total_students = StudentRegister.objects(stageExamTwoStatus__in=[1])
    if total_students:
        for tcs in total_students:
            students_dict={
                "firstName":tcs.firstName,
                "lastName":tcs.lastName,
                "className":tcs.className,
                "status":tcs.status,
                "link":tcs.link,
                "levelTwoMarks1":tcs.levelTwoMarks1,
                "levelTwoMarks2":tcs.levelTwoMarks2,
                "levelTwoMarks3":tcs.levelTwoMarks3,
                "levelTwoMarks4":tcs.levelTwoMarks4,
                "levelTwoTotalMarks":tcs.levelTwoTotalMarks,
                "stageExamTwoStatus":tcs.stageExamTwoStatus,
                "paperValidateStatus2":tcs.paperValidateStatus2
                
            }
            total_students_list.append(students_dict)
    return render_template("admin/stage_two.html",countData=total_dict,total_data=total_students_list,admin_data=admin_dict)

@app.route("/StageThreeData",methods=['POST','GET'])
def stageThreeDataPage():
    total_students_list=[]

    registered_student = StudentRegister.objects(status__in=[0,1,2,3]).count()
    stage_one_count = StudentRegister.objects(stageExamOneStatus__in=[1]).count()
    stage_two_count = StudentRegister.objects(stageExamTwoStatus__in=[1]).count()
    stage_three_count = StudentRegister.objects(stageExamThreeStatus__in=[1]).count()
    total_completed = StudentRegister.objects(status__in=[3]).count()
    admin_data = AdminRegister.objects.get(status__in=[1])

    admin_dict={
        "userName":admin_data.userName,
        "email":admin_data.email
    }
    total_dict={
        "registeredStudent":registered_student,
        "stageOne":stage_one_count,
        "stageTwo":stage_two_count,
        "stageThree":stage_three_count,
        "totalCompleted":total_completed
    }
    total_students = StudentRegister.objects(stageExamThreeStatus__in=[1])
    if total_students:
        for tcs in total_students:
            students_dict={
                "firstName":tcs.firstName,
                "lastName":tcs.lastName,
                "className":tcs.className,
                "status":tcs.status,
                "link":tcs.link,
                "levelThreeMarks1":tcs.levelThreeMarks1,
                "levelThreeMarks2":tcs.levelThreeMarks2,
                "levelThreeMarks3":tcs.levelThreeMarks3,
                "levelThreeMarks4":tcs.levelThreeMarks4,
                "levelThreeTotalMarks":tcs.levelThreeTotalMarks,
                "stageExamThreeStatus":tcs.stageExamThreeStatus,
                "paperValidateStatus3":tcs.paperValidateStatus3
            }
            total_students_list.append(students_dict)
    return render_template("admin/stage_three.html",countData=total_dict,total_data=total_students_list,admin_data=admin_dict)    


@app.route("/DashboardPage",methods=['POST','GET'])
def adminDashboard():
    total_students_list=[]

    registered_student = StudentRegister.objects(status__in=[0,1,2,3]).count()
    stage_one_count = StudentRegister.objects(stageExamOneStatus__in=[1]).count()
    stage_two_count = StudentRegister.objects(stageExamTwoStatus__in=[1]).count()
    stage_three_count = StudentRegister.objects(stageExamThreeStatus__in=[1]).count()
    total_completed = StudentRegister.objects(status__in=[3]).count()
    admin_data = AdminRegister.objects.get(status__in=[1])

    admin_dict={
        "userName":admin_data.userName,
        "email":admin_data.email
    }
    total_dict={
        "registeredStudent":registered_student,
        "stageOne":stage_one_count,
        "stageTwo":stage_two_count,
        "stageThree":stage_three_count,
        "totalCompleted":total_completed
    }
    total_students = StudentRegister.objects(status__in=[0,1,2,3])
    if total_students:
        for tcs in total_students:
            
            students_dict={
                "firstName":tcs.firstName,
                "lastName":tcs.lastName,
                "className":tcs.className,
                "status":tcs.status,
                # "levelOneMarks1":tcs.levelOneMarks1,
                # "levelOneMarks2":tcs.levelOneMarks2,
                # "levelOneMarks3":tcs.levelOneMarks3,
                "levelOneTotalMarks":tcs.levelOneTotalMarks,
                "levelTwoTotalMarks":tcs.levelTwoTotalMarks,
                "levelThreeTotalMarks":tcs.levelThreeTotalMarks
                
                
            }
            total_students_list.append(students_dict)
    return render_template("admin/dashboard.html",countData=total_dict,total_data=total_students_list,admin_data=admin_dict)


@app.route("/StudentLevelOneLeaderboard",methods=['POST','GET'])
def studentLevelOneLeaderBoardPage():
    c=0
    level_one_leader_list=[]
    level_one_students = StudentRegister.objects(marksUpdatedStatus1__in=[1]).order_by('-levelOneTotalMarks','attemptedOnTaskOne')
    if level_one_students:
        for los in level_one_students:
            c=c+1
            level_one_leader_dict={
                "fullName":los.firstName +" "+los.lastName,
                "className":los.className,
                "rollNumber":los.rollNumber,
                "rank":c,
                "levelOneTotalMarks":los.levelOneTotalMarks
                
            }
            level_one_leader_list.append(level_one_leader_dict)
    return render_template('student/student_level_one_leader_board.html',level_one=level_one_leader_list)

@app.route("/StudentLevelTwoLeaderboard",methods=['POST','GET'])
def studentLevelTwoLeaderBoardPage():
    c=0
    level_two_leader_list=[]
    level_two_students = StudentRegister.objects(marksUpdatedStatus2__in=[1]).order_by('-levelTwoTotalMarks','attemptedOnTaskTwo')
    if level_two_students:
        for lts in level_two_students:
            c=c+1
            level_two_leader_dict={
                "fullName":lts.firstName +" "+lts.lastName,
                "className":lts.className,
                "rollNumber":lts.rollNumber,
                "rank":c,
                "levelTwoTotalMarks":lts.levelTwoTotalMarks
                
            }
            level_two_leader_list.append(level_two_leader_dict)
    return render_template('student/student_level_two_leader_board.html',level_two=level_two_leader_list)

@app.route("/StudentLevelThreeLeaderboard",methods=['POST','GET'])
def studentLevelThreeLeaderBoardPage():
    c=0
    level_three_leader_list=[]
    level_three_students = StudentRegister.objects(marksUpdatedStatus3__in=[1]).order_by('-levelThreeTotalMarks','attemptedOnTaskThree')
    if level_three_students:
        for lts in level_three_students:
            c=c+1
            level_three_leader_dict={
                "fullName":lts.firstName +" "+lts.lastName,
                "className":lts.className,
                "rollNumber":lts.rollNumber,
                "rank":c,
                "levelThreeTotalMarks":lts.levelThreeTotalMarks
                
            }
            level_three_leader_list.append(level_three_leader_dict)
    return render_template('student/student_level_three_leader_board.html',level_three=level_three_leader_list)

@app.route("/StudentLevelOverallLeaderboard",methods=['POST','GET'])
def studentLevelOverallLeaderBoardPage():
    c=0
    level_three_leader_list=[]
    level_three_students = StudentRegister.objects(status__in=[1,2,3]).order_by('-totalMarks')
    if level_three_students:
        for lts in level_three_students:
            c=c+1
            level_three_leader_dict={
                "fullName":lts.firstName +" "+los.lastName,
                "className":lts.className,
                "rollNumber":lts.rollNumber,
                "rank":c,
                "levelOneTotalMarks":lts.levelThreeTotalMarks
                
            }
            level_three_leader_list.append(level_three_leader_dict)
    return render_template('student/student_overall_leader_board.html')            

# def stageOneMarksValidationViewPage()

@app.route("/StageOneMarksValidation/<link>",methods=['POST','GET'])
def stageOneMarksValidationViewPage(link):
    if request.method=="GET":
        stage_one_student=StudentRegister.objects.get(link=link)
        if stage_one_student:
            emailId=stage_one_student.emailId
            stage_one=StageOne.objects.get(emailId=emailId)
            students_one_dict={
                "firstName":stage_one_student.firstName+" "+stage_one_student.lastName,
                "className":stage_one_student.className,
                "rollNumber":stage_one_student.rollNumber,
                # "link":stage_one_student.link
                
            }

            stage_one_dict={
                "projectDescription":stage_one.projectDescription,
                "codeScreenshot":stage_one.codeScreenshot,
                "circuteDiagramScreenshot":stage_one.circuteDiagramScreenshot,
                "finalProjectVideo":stage_one.finalProjectVideo
            }            
          
    return render_template("admin/student_marks1.html",std_data=students_one_dict,task_data=stage_one_dict,link=link)

@app.route("/StageOneMarksInfo/<link>",methods=['POST','GET'])
def stageOneMarksPage(link):
    levelOneMarks1=request.form.get("levelOneMarks1")
    levelOneMarks2=request.form.get("levelOneMarks2")
    levelOneMarks3=request.form.get("levelOneMarks3")
    levelOneMarks4=request.form.get("levelOneMarks4")
    levelOneTotalMarks=0

    if request.method=="POST":
        levelOneTotalMarks=int(levelOneMarks1)+int(levelOneMarks2)+int(levelOneMarks3)+int(levelOneMarks4)
        get_student_data=StudentRegister.objects.get(link=link)
        paperValidateStatus1=1
        marksUpdatedStatus1=1
        if get_student_data:
            students_marks=get_student_data.update(
                levelOneMarks1=levelOneMarks1,
                levelOneMarks2=levelOneMarks2,
                levelOneMarks3=levelOneMarks3,
                levelOneMarks4=levelOneMarks4,
                levelOneTotalMarks=levelOneTotalMarks,
                paperValidateStatus1=paperValidateStatus1,
                marksUpdatedStatus1=marksUpdatedStatus1
                )
            if students_marks:
                return redirect(url_for('stageOneDataPage'))
    else:

        return render_template('student/marks_insert1.html')    

@app.route("/StageTwoMarksValidation/<link>",methods=['POST','GET'])
def stageTwoMarksValidationViewPage(link):
    if request.method=="GET":
        stage_two_student=StudentRegister.objects.get(link=link)
        if stage_two_student:
            emailId=stage_two_student.emailId
            stage_two=StageTwo.objects.get(emailId=emailId)
            students_two_dict={
                "firstName":stage_two_student.firstName+" "+stage_two_student.lastName,
                "className":stage_two_student.className,
                "rollNumber":stage_two_student.rollNumber,
                # "link":stage_one_student.link
                
            }

            stage_two_dict={
                "projectDescription":stage_two.projectDescription,
                "codeScreenshot":stage_two.codeScreenshot,
                "circuteDiagramScreenshot":stage_two.circuteDiagramScreenshot,
                "finalProjectVideo":stage_two.finalProjectVideo
            }            
          
    return render_template("admin/student_marks2.html",std_data=students_two_dict,task_data=stage_two_dict,link=link)

@app.route("/StageTwoMarksInfo/<link>",methods=['POST','GET'])
def stageTwoMarksPage(link):
    levelTwoMarks1=request.form.get("levelTwoMarks1")
    levelTwoMarks2=request.form.get("levelTwoMarks2")
    levelTwoMarks3=request.form.get("levelTwoMarks3")
    levelTwoMarks4=request.form.get("levelTwoMarks4")
    levelTwoTotalMarks=0

    if request.method=="POST":
        levelTwoTotalMarks=int(levelTwoMarks1)+int(levelTwoMarks2)+int(levelTwoMarks3)+int(levelTwoMarks4)
        get_student_data=StudentRegister.objects.get(link=link)
        paperValidateStatus2=1
        marksUpdatedStatus2=1
        if get_student_data:
            students_marks=get_student_data.update(
                levelTwoMarks1=levelTwoMarks1,
                levelTwoMarks2=levelTwoMarks2,
                levelTwoMarks3=levelTwoMarks3,
                levelTwoMarks4=levelTwoMarks4,
                levelTwoTotalMarks=levelTwoTotalMarks,
                paperValidateStatus2=paperValidateStatus2,
                marksUpdatedStatus2=marksUpdatedStatus2
                )
            if students_marks:
                return redirect(url_for('stageTwoDataPage'))
    else:

        return render_template('student/marks_insert2.html')

@app.route("/StageThreeMarksInfo/<link>",methods=['POST','GET'])
def stageThreeMarksPage(link):
    levelThreeMarks1=request.form.get("levelThreeMarks1")
    levelThreeMarks2=request.form.get("levelThreeMarks2")
    levelThreeMarks3=request.form.get("levelThreeMarks3")
    levelThreeMarks4=request.form.get("levelThreeMarks4")
    levelThreeTotalMarks=0

    if request.method=="POST":
        levelThreeTotalMarks=int(levelThreeMarks1)+int(levelThreeMarks2)+int(levelThreeMarks3)+int(levelThreeMarks4)
        get_student_data=StudentRegister.objects.get(link=link)
        # total_marks =get_student_data.leveloneTotalMarks
        # print(total_marks)
        paperValidateStatus3=1
        marksUpdatedStatus3=1
        if get_student_data:
            students_marks=get_student_data.update(
                levelThreeMarks1=levelThreeMarks1,
                levelThreeMarks2=levelThreeMarks2,
                levelThreeMarks3=levelThreeMarks3,
                levelThreeMarks4=levelThreeMarks4,
                levelThreeTotalMarks=levelThreeTotalMarks,
                paperValidateStatus3=paperValidateStatus3,
                marksUpdatedStatus3=marksUpdatedStatus3
                )
            if students_marks:
                return redirect(url_for('stageThreeDataPage'))
    else:

        return render_template('student/marks_insert3.html')            
@app.route("/StageThreeMarksValidation/<link>",methods=['POST','GET'])
def stageThreeMarksValidationViewPage(link):
    if request.method=="GET":
        stage_three_student=StudentRegister.objects.get(link=link)
        if stage_three_student:
            emailId=stage_three_student.emailId
            stage_three=StageThree.objects.get(emailId=emailId)
            students_three_dict={
                "firstName":stage_three_student.firstName+" "+stage_three_student.lastName,
                "className":stage_three_student.className,
                "rollNumber":stage_three_student.rollNumber,
                # "link":stage_one_student.link
                
            }

            stage_three_dict={
                "projectDescription":stage_three.projectDescription,
                "codeScreenshot":stage_three.codeScreenshot,
                "circuteDiagramScreenshot":stage_three.circuteDiagramScreenshot,
                "finalProjectVideo":stage_three.finalProjectVideo
            }            
          
    return render_template("admin/student_marks3.html",std_data=students_three_dict,task_data=stage_three_dict,link=link)

if __name__=='__main__':
    app.run(debug=True)
