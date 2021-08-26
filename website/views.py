import re
from datetime import date, datetime
from website import UPLOAD_FOLDER
from flask import Blueprint, app , render_template ,request
from flask.helpers import flash
import os
import glob
import openpyxl
from werkzeug.utils import redirect, secure_filename
views=Blueprint('views', __name__)
def Filelistfun() :
    fileslist=glob.glob("website\ExcelFiles/*.xlsx")
    fileslistname=[]
    for f in fileslist: 
        fileslistname.append(str(f).replace('website\ExcelFiles\\',''))
    return fileslistname
ALLOWED_EXTENSIONS = {'xlsx'}
def allowed_file(filename):
    return '.' in filename and \
filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@views.route('/')
def home(): 
    return render_template("home.html")
@views.route('/insert',methods=['GET', 'POST'])
def upload_file(): 
    if request.method=='POST':
        if 'file' not in request.files:
            #flash( 'pas de fichier excel')
            pass
        file= request.files['file']
        print (file)
        if file.filename=='':
            flash ('Pas de fichier selectionné !' ,category='ERR')
        if not allowed_file(file.filename):
            flash( 'pas de fichier excel', category='ERR')
        if file and allowed_file(file.filename):
            filename= secure_filename(file.filename)
            i =1
            filelist=Filelistfun()
            while filename in filelist:
                if i>1 :
                    filename=filename[: -19]
                else :
                    filename=filename[: -5]
                filename= filename+'('+str (datetime.today().strftime("%d-%m-%y"))+')-V'+str (i)+'-.xlsx'
                i+=1
            file.save(os.path.join(UPLOAD_FOLDER,filename))
            ps =openpyxl.load_workbook(str( UPLOAD_FOLDER +'/'+filename))
            sh= ps['Feuil1']
            sh['B'+'3'].value  = 'MLO type' 
            sh['D'+'2'].value  = 'modification Date :'+ str( datetime.now().strftime("%d/%B/%Y  %H:%M:%S"))
            sh['C'+'3'].value = request.form.get('MLOtype')
            ps.save(str( UPLOAD_FOLDER +'/'+filename))
            print( "done")
            return render_template("done.html" , F=filename, T=request.form.get('MLOtype'))
    return render_template("insert.html")


