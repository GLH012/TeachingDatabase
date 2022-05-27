from re import TEMPLATE
from bottle import html_escape, route, run, request, get, post, response, template, HTTPResponse
# from xml.dom import minidom, Node
from classDb import DatabaseConnect as dbcon

<<<<<<< Updated upstream

@route('/home')
def home():
    return template('./templates/Home_Page')


@route('/Teaching_Staff_Portal')
def Teaching_Staff_Portal():
 return template('./templates/Teaching_Staff_Portal')


@route('/login', method="get")
=======
# Initial Route, Landing users into the home login page.
@route('/', method="get")
>>>>>>> Stashed changes
def login():
 return template('./templates/Admin_Portal')

def check_login(username, password):
 pass
#does not work, someone else take a look at it got bored so i made incorrect user/pass work
@route('/login', method="post")
def do_login():
    Username = request.forms.get('username')
    Password = request.forms.get('password')
    if check_login(Username, Password):
        return "<p>Your login information was correct.</p>"
    else:
        return template('./templates/Admin_Portal_2')

@route('/admin_portal')
def do_admin_portal():
    return template('./templates/Admin_Portal_2')

@route('/admin_portal/aqfrecords')
def do_aqfrecords():
     with dbcon() as db:
        conx = db.opendb()
        selectQuery = (
            'SELECT AQFLevel_ID, Qualified_Degree, AQFLevel, Qualification_Level_Required_To_Teach FROM AQFLevels')
            #'SELECT aqflevels.AQFLevel, COUNT(qualification.AQFLevel_ID) AS total_staff FROM aqflevels INNER JOIN qualification ON aqflevels.AQFLevel_ID = qualification.AQFLevel_IDGROUP BY AQFLevel')
        dcurs = conx.cursor(buffered=True)
        dcurs.execute(selectQuery)
        if dcurs.rowcount > 0:
            aqf_data = dcurs.fetchall()
        dcurs.close()
     return template('./templates/aqfrecords', aqf_list=aqf_data)

@route('/staff')
def get_first_page():
    with dbcon() as db:
        # create a handle to the database connection that you open
        conx = db.opendb()
        # Create the database query
        selectQuery = (
            # 'SELECT First_Name, Last_Name FROM staff WHERE aipubmedid = %s'
            'SELECT StaffID, First_Name, Last_Name FROM staff')
        # data_query is the variable that will take the place of %s above
        # data_query = (some_variabl_id,)
        # create a cursor or variable which will recieve the data returned from the database - Microsoft call this a recordset
        dcurs = conx.cursor(buffered=True)
        # execute the query and query variable from within the cursor object
        # dcurs.execute(selectQuery, data_query)
        dcurs.execute(selectQuery)
        # check to see if there is any returned data
        if dcurs.rowcount > 0:
            staff_data = dcurs.fetchall()
            # incriment through each row and get the returned data
            #for s in dcurs:
            #    fName = (First_Name)
            #    print(s)
        # else:
            # if there is no data returned from the database then do something else
            
        # close the cursor to finalise the query - this does not close the connection to the database
        dcurs.close()
    return template('./templates/staff.tpl', staff_list=staff_data)


@route('/staff/getstaff')
def get_staff():
    staffID = request.query.staffid
    print(staffID)
    
    with dbcon() as db:
        # create a handle to the database connection that you open
        conx = db.opendb()
        # Create the database query
        selectQuery = (
            # 'SELECT First_Name, Last_Name FROM staff WHERE aipubmedid = %s'
            'SELECT StaffID, First_Name, Last_Name FROM WHERE StaffID = %s')
        # data_query is the variable that will take the place of %s above
        data_query = (staffID,)
        # create a cursor or variable which will recieve the data returned from the database - Microsoft call this a recordset
        dcurs = conx.cursor(buffered=True)
        # execute the query and query variable from within the cursor object
        dcurs.execute(selectQuery, data_query)
        # check to see if there is any returned data
        if dcurs.rowcount > 0:
            staff_member = dcurs.fetchone()
            print (staff_member)
            # incriment through each row and get the returned data
            #for s in dcurs:
            #    fName = (First_Name)
            #    print(s)
        # else:
            # if there is no data returned from the database then do something else
            
        # close the cursor to finalise the query - this does not close the connection to the database
        dcurs.close()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Content-type'] = 'application/text'
        
    return staff_member

# This saves the xml file without modification
# @route('/saveStaff')
# def save_staff():


@route('/create_staff', method='GET')
def create_staff():

    with dbcon() as db:
        conx = db.opendb()
       
        if request.GET.save:

            var_title = request.query.Title
            var_first_name = request.query.First_Name
            var_last_name = request.query.Last_Name
            var_email = request.query.EmailID
            var_phoneno = request.query.PhoneNo
 
            selectQuery = (
                "INSERT INTO staff(Title, First_Name, Last_Name, EmailID, PhoneNo) VALUES (%s, %s, %s, %s, %s)"
            )

            data_query = (var_title, var_first_name, var_last_name, var_email, var_phoneno)

            dcurs = conx.cursor(buffered=True)

            dcurs.execute(selectQuery, data_query)
            new_StaffID = dcurs.lastrowid
            conx.commit()
            dcurs.close()
            
        return template('./templates/create_staff.tpl')


    
    
    

run(host='localhost', port=8080, debug=True, reloader=True)
