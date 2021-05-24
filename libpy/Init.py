############################################################
#
#        Some useful function
#        Copyright(c) KazukiAmakawa, all right reserved.
#        Init.py
#
############################################################


def LogWrite(LogStr, kind):
    import os
    import time 
    FileName = "info.log"
        
    File = open(FileName, "a")
    Ima = time.ctime()
    WriteStr = '[' + Ima + ']'
    if kind == '0':
        WriteStr = WriteStr + '  Info   '
    else:
        WriteStr = WriteStr + '  Error  '
    WriteStr = WriteStr + LogStr + '\n'
    File.write(WriteStr)
    File.close()
    return 0


def IntInput(Str, Min, Max, Method):
    Int = 0
    NoMin = False
    NoMax = False
    try:
        Min = int(Min)
    except:
        NoMin = True

    try:
        Max = int(Max)
    except:
        NoMax = True
    
    while 1:
        InpStr = input(Str)
        try:
            if Method == "int":
                Int = int(InpStr)
            elif Method == "float":
                Int = float(InpStr)
        except:
            print("Input Error")
            continue
        else:
            if NoMin == True and NoMax == True:
                break
            
            elif NoMin == True and NoMax == False:
                if Int > Max:
                    print("Input Error")
                    continue
                else:
                    break
        
            elif NoMin == False and NoMax == True:
                if Int < Min:
                    print("Input Error")
                    continue
                else:
                    break
            else:
                if Int < Min or Int > Max:
                    print("Input Error")
                    continue
                else:
                    break
    return Int



def GetTime():
    import time
    TimeStr = time.ctime()
    TimeStr += ' '
    Space = -1
    Jikan = ['', '', '', '']
    RemStr = ''
    for i in range (0, len(TimeStr)):
        if TimeStr[i] == ' ':
            if RemStr == '':
                continue
            else:
                if not Space == -1:
                    Jikan[Space] += RemStr
                RemStr = ''
                Space += 1    
        else:
            RemStr += TimeStr[i]

    ReturnTime = 0
    try:
        ReturnTime = int(Jikan[3])
    except ValueError:
        LogWrite('Get time error', '121')
        return -1
    ReturnTime *= 100

    if Jikan[0] == "Jan":
        ReturnTime += 1
    if Jikan[0] == "Feb":
        ReturnTime += 2
    if Jikan[0] == "Mar":
        ReturnTime += 3
    if Jikan[0] == "Apr":
        ReturnTime += 4    
    if Jikan[0] == "May":
        ReturnTime += 5
    if Jikan[0] == "Jun":
        ReturnTime += 6
    if Jikan[0] == "Jul":
        ReturnTime += 7
    if Jikan[0] == "Aug":
        ReturnTime += 8    
    if Jikan[0] == "Sep":
        ReturnTime += 9
    if Jikan[0] == "Oct":
        ReturnTime += 10
    if Jikan[0] == "Nov":
        ReturnTime += 11
    if Jikan[0] == "Dec":
        ReturnTime += 12

    ReturnTime *= 100

    try:
        ReturnTime += int(Jikan[1])
    except ValueError:
        LogWrite('Get time error', '122')
        return -1

    ReturnTime *= 1000000
    DokiStr = ''
    Kanryou = 0
    Jikan[2] += ":"
    for i in range (0, len(Jikan[2])):
        if Jikan[2][i] == ':':
            Kanryou += 1
            if Kanryou == 1 or Kanryou == 2:
                continue
            else:
                try:
                    ReturnTime += int(DokiStr)
                except ValueError:
                    LogWrite('Get time error', '123')
                    return -1
                break
            
        else:
            DokiStr += Jikan[2][i]

    return ReturnTime


def ArrOutput(Arr, Mode = 0, Save_File = True):
    Str = ""
    if Mode == 1:
        Str += "[["
    for i in range(0, len(Arr)):
        for j in range(0, len(Arr[i])):
            Str += str(Arr[i][j])
            if Mode == 0:
                Str += "\t"
            elif Mode == 1 and j != len(Arr[i]) - 1:
                Str += ", "
        if Mode == 0:
            Str += "\n"
        elif Mode == 1:
            if i != len(Arr) - 1:
                Str += "], ["
            else:
                Str += "]]"

    if Save_File:
        FileName = "SaveArr" + str(GetTime())
        File = open(FileName, "a")
        File.write(Str)
        File.close()
    return Str



def GetNextDay(Time, TimeAdd):
    Day = Time % 100
    Mouth = ((Time - Day)/100) % 100
    Year = int(Time / 10000)
    Day += TimeAdd
    
    if Mouth == 2:
        if Year % 400 == 0 or (Year % 100 != 0 and Year % 4 == 0):
            if Day > 29:
                Day -= 29
                Mouth += 1
        else:
            if Day > 28:
                Day -= 28
                Mouth += 1

    if Mouth == 1 or Mouth == 3 or Mouth == 5 or Mouth == 7 or Mouth == 8 or Mouth == 10:
        if Day > 31:
            Day -= 31
            Mouth += 1
    
    if Mouth == 4 or Mouth == 6 or Mouth == 9 or Mouth == 11:
        if Day > 30:
            Day -= 30
            Mouth += 1
    
    if Mouth == 12:
        if Day > 31:
            Day -= 31
            Mouth = (Mouth + 1) % 12
            Year += 1

    return (Year * 10000 + Mouth * 100 + Day)


def SystemJudge():
    import platform  
    Str = platform.system() 
    if Str[0] == "w" or Str[0] == "W":
        return "Dos"
    elif Str == "Darwin": 
        return "Darwin"
    else:
        return "Linux"


def GetSufixFile(dir_name, sufixSet):
    import os
    im_paths = []
    im_name = []
    for parent, dirs, files in os.walk(dir_name):
        for file in files:
            print(file)
            name,sufix = file.split('.')
            im_path = ""
            if sufix in sufixSet:
                im_path = os.path.join(parent,file)
            if os.path.exists(im_path):
                im_paths.append(im_path)
                im_name.append(name)

    return im_paths, im_name


def RGBList2Table(InputImage):
    import numpy as np
    Size = np.shape(InputImage)
    if len(Size) != 3:
        print("InputError: RGBList2Table function need input image with [[[R,G,B] * width] * height] parameter. Your input may RGB tabled image or grey image")
        return [[[-1]], [[]], [[]]]
    if Size[2] != 3 and Size[0] == 3:
        return InputImage

    RTable = []
    GTable = []
    BTable = []
    for i in range(0, len(InputImage)):
        RLine = []
        GLine = []
        BLine = []
        for j in range(0, len(InputImage[i])):
            RLine.append(InputImage[i][j][0])
            GLine.append(InputImage[i][j][1])
            BLine.append(InputImage[i][j][2])
        RTable.append(RLine)
        GTable.append(GLine)
        BTable.append(BLine)
    return np.array([RTable, GTable, BTable])



def ImageIO(file_dir = "", img = [], io = "i", mode = "rgb", backend = ""):
    """
    This is a image io and print function to combined several backend
    """
    import numpy as np

    opencv_mark        = False
    PIL_mark        = False
    matplotlib_mark = False
    imageio_mark    = False


    if len(backend) == 0:    
        try:
            import cv2
            opencv_mark = True
        except:
            try:
                from PIL import Image
                PIL_mark = True
            except:
                try:
                    import matplotlib
                    matplotlib_mark = True
                except:
                    try:
                        import imageio
                        imageio_mark = True
                    except:
                        raise ModuleNotFoundError("None image processing model has been found, you may need to install opencv, PIL, matplotlib or imageio")


    elif backend == "opencv":
        try:
            import cv2
        except:
            raise ModuleNotFoundError("Opencv backend has not been installed")
        opencv_mark = True
    elif backend == "Pillow":
        try:
            from PIL import Image
        except:
            raise ModuleNotFoundError("Pillow backend has not been installed")
            
        PIL_mark = True
    elif backend == "matplotlib":
        try:
            import matplotlib
        except:
            raise ModuleNotFoundError("Matplotlib backend has not been installed")
        matplotlib_mark = True
    elif backend == "imageio":
        try:
            import imageio
        except:
            raise ModuleNotFoundError("Matplotlib backend has not been installed")
        imageio_mark = True
    else:
        raise ModuleNotFoundError("Import package not be support, you may need to use opencv, PIL, matplotlib or imageio")







    if opencv_mark == True:
        print("Using opencv backend")
        import cv2



        if io == "i":
            if mode == "rgb":
                img = cv2.imread(file_dir)
            elif mode == "grey":
                img = cv2.imread(file_dir, cv2.IMREAD_GRAYSCALE)
            else:
                raise ValueError("mode error, the image mode must be confirmed as 'grey' for mono or 'rgp' for rgb image")
            return img



        elif io == "p":
            img = np.array(img)
            img_size = len(np.shape(img))
            if len(file_dir) == 0 and img_size != 2 and img_size != 3:
                raise ValueError("It is necessary to confirmed the location of image or img array if you want to print image")
            
            if len(file_dir) != 0:
                img = cv2.imread(file_dir)
            
            if mode == "rgb":
                cv2.imshow("image", img)
                cv2.waitKey(1)
            elif mode == "grey":
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                cv2.imshow("image". img)
                cv2.waitKey(1)
            else:
                raise ValueError("mode error, the image mode must be confirmed as 'grey' for mono or 'rgp' for rgb image")
            return True



        elif io == "o":
            if len(file_dir) == 0:
                raise ValueError("file_dir not be confirmed")

            if mode == "rgb":
                cv2.imwrite(file_dir, img, cv2.IMREAD_UNCHANGED)
            elif mode == "grey":
                if len(np.shape(img)) == 3:
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                cv2.imwrite(file_dir, img)
            else:
                raise ValueError("mode error, the image mode must be confirmed as 'grey' for mono or 'rgp' for rgb image")
            return True

        else:
            raise ValueError("io error, the io must be confirmed as 'i' for input, 'p' for presentation or 'o' for output")







    elif PIL_mark == True:
        print("Using Pillow backend")
        from PIL import Image


        if io == "i":
            if mode == "rgb":
                img = np.array(Image.open(file_dir))
            elif mode == "grey":
                img = np.array(Image.open(file_dir).convert("L"))
            else:
                raise ValueError("mode error, the image mode must be confirmed as 'grey' for mono or 'rgp' for rgb image")
            return img



        elif io == "p":
            img = np.array(img)
            img_size = len(np.shape(img))
            if len(file_dir) == 0 and img_size != 2 and img_size != 3:
                raise ValueError("It is necessary to confirmed the location of image or img array if you want to print image")
            
            if len(file_dir) != 0:
                img = Image.open(file_dir)
            else:
                img = Image.fromarray(img.astype('uint8'), 'RGB')
            
            if mode == "rgb":
                img.show()
            elif mode == "grey":
                img = img.convert("L")
                img.show()
            else:
                raise ValueError("mode error, the image mode must be confirmed as 'grey' for mono or 'rgp' for rgb image")
            return True



        elif io == "o":
            if len(file_dir) == 0:
                raise ValueError("file_dir not be confirmed")

            
            if mode == "rgb":
                img = Image.fromarray(img.astype('uint8'), 'RGB')
                img.save(file_dir)
            elif mode == "grey":
                if len(img[0]) == 3:
                    img = Image.fromarray(img.astype('uint8'), 'RGB')
                    img = img.convert("L")
                else:
                    img = Image.fromarray(img.astype('uint8'))
                img.save(file_dir)
            else:
                raise ValueError("mode error, the image mode must be confirmed as 'grey' for mono or 'rgp' for rgb image")
            return True

        else:
            raise ValueError("io error, the io must be confirmed as 'i' for input, 'p' for presentation or 'o' for output")






    elif matplotlib_mark == True:
        print("Using matplotlib backend")
        import matplotlib


        if io == "i":
            if mode == "rgb":
                img = np.array(matplotlib.pyplot.imread(file_dir))
            elif mode == "grey":
                img = np.array(matplotlib.pyplot.imread(file_dir))
                img = np.dot(img[...,:3], [0.299, 0.587, 0.144])
            else:
                raise ValueError("mode error, the image mode must be confirmed as 'grey' for mono or 'rgp' for rgb image")
            return img



        elif io == "p":
            img = np.array(img)
            img_size = len(np.shape(img))
            if len(file_dir) == 0 and img_size != 2 and img_size != 3:
                raise ValueError("It is necessary to confirmed the location of image or img array if you want to print image")
            
            if len(file_dir) != 0:
                img = np.array(matplotlib.pyplot.imread(file_dir))
            
            if mode == "rgb":
                matplotlib.pyplot.imshow(img)
            elif mode == "grey":
                img = np.dot(img[...,:3], [0.299, 0.587, 0.144])
                matplotlib.pyplot.imshow(img)
            else:
                raise ValueError("mode error, the image mode must be confirmed as 'grey' for mono or 'rgp' for rgb image")
            return True



        elif io == "o":
            if len(file_dir) == 0:
                raise ValueError("file_dir not be confirmed")

            img = Image.fromarray(img.astype('uint8'), 'RGB')
            if mode == "rgb":
                matplotlib.pyplot.savefig(img)
            elif mode == "grey":
                img = np.dot(img[...,:3], [0.299, 0.587, 0.144])
                matplotlib.pyplot.savefig(img)
            else:
                raise ValueError("mode error, the image mode must be confirmed as 'grey' for mono or 'rgp' for rgb image")
            return True

        else:
            raise ValueError("io error, the io must be confirmed as 'i' for input, 'p' for presentation or 'o' for output")











    elif imageio_mark == True:
        print("Using imageio backend")
        import imageio
        if io == "i":
            if mode == "rgb":
                img = np.array(imageio.imread(file_dir))
            elif mode == "grey":
                img = np.array(imageio.imread(file_dir))
                img = np.dot(img[...,:3], [0.299, 0.587, 0.144])
            else:
                raise ValueError("mode error, the image mode must be confirmed as 'grey' for mono or 'rgp' for rgb image")
            return img



        elif io == "p":
            raise ValueError("mode error, imageio don't have image presentation system")
            return True



        elif io == "o":
            if len(file_dir) == 0:
                raise ValueError("file_dir not be confirmed")

            if mode == "rgb":
                imageio.imwrite(file_dir, img)
            elif mode == "grey":
                img = np.dot(img[...,:3], [0.299, 0.587, 0.144])
                imageio.imwrite(file_dir, img)
            else:
                raise ValueError("mode error, the image mode must be confirmed as 'grey' for mono or 'rgp' for rgb image")
            return True

        else:
            raise ValueError("io error, the io must be confirmed as 'i' for input, 'p' for presentation or 'o' for output")

    else:
        raise ModuleNotFoundError("None image processing model has been found, you may need to install opencv, PIL, matplotlib or imageio")






def download_file(url, filename, error_msg = "File not found"):
    import requests
    try:
        r = requests.get(url, allow_redirects=True)
        open(filename, 'wb').write(r.content)
    except:
        print(error_msg)
    return 






def error_warning(warning_info):
    from PyQt5 import QtWidgets
    app = QtWidgets.QApplication([])

    error_dialog = QtWidgets.QErrorMessage()
    error_dialog.showMessage(warning_info)
    app.exec_()
    clear_all() 
    sys.exit()
    return





def read_json(filename):
    import json
    file = open(filename, "r", encoding="utf-8")
    str_json = ""
    while 1:
        line = file.readline()
        if not line:
            break 
        maxx = len(line) - 1
        for i in range(1, len(line)):
            if line[i] == "/" and line[i-1] == "/":
                maxx = i-2
        line = line[0: maxx]
        str_json += line

    return json.loads(str_json)




def file_operation_function(command_list, server_route, client_route):
    import os
    import shutil
    import zipfile
    
    #Analysis command and combine files/folder route
    combo_command = []
    tmp_string = ""
    for i in range(0, len(command_list)):
        if    command_list[i] == "-cp":
            combo_command.append("-cp")
        elif  command_list[i] == "-mv":
            combo_command.append("-mv")
        elif  command_list[i] == "-rm":
            combo_command.append("-rm")
        elif  command_list[i] == "-mkdir":
            combo_command.append("-mkdir")
        elif  command_list[i] == "-r":
            combo_command.append("-r")
        elif  command_list[i] == "-unzip":
            combo_command.append("-unzip")
        elif  command_list[i] == "-tool":
            tmp_string = os.path.join(tmp_string, server_route)
        elif  command_list[i] == "-client":
            tmp_string = os.path.join(tmp_string, client_route)
        elif  command_list[i] == "-to":
            combo_command.append(tmp_string)
            tmp_string = ""
        else:
            tmp_string = os.path.join(tmp_string, command_list[i])
        
        if i+1 == len(command_list):
            combo_command.append(tmp_string)
            break
    #print(combo_command)


    #Operation
    if combo_command[0] == "-cp":
        if combo_command[1] == "-r":
            try:
                shutil.copytree(combo_command[2], combo_command[3])
            except:
                try:
                    shutil.rmtree(combo_command[3])
                    shutil.copytree(combo_command[2], combo_command[3])
                except:
                    pass
        else:
            try:
                shutil.copyfile(combo_command[1], combo_command[2])
            except:
                try:
                    os.remove(combo_command[2])
                    shutil.copyfile(combo_command[1], combo_command[2])
                except:
                    pass
    elif combo_command[0] == "-mv":
        if combo_command[1] == "-r":
            try:
                shutil.move(combo_command[2], combo_command[3])
            except:
                pass
        else:
            try:
                shutil.move(combo_command[1], combo_command[2])
            except:
                pass
    elif combo_command[0] == "-rm":
        if combo_command[1] == "-r":
            try:
                shutil.rmtree(combo_command[2])
            except:
                pass
        else:
            try:
                os.remove(combo_command[1])
            except:
                pass
    elif combo_command[0] == "-mkdir":
        try:
            os.mkdir(combo_command[1])    
        except:
            pass
    elif combo_command[0] == "-unzip":
        try:
            os.mkdir(combo_command[2])
        except:
            pass
        try:
            with zipfile.ZipFile(combo_command[1], 'r') as zip_ref:
                zip_ref.extractall(combo_command[2])
        except:
            pass




def FileReadLine(line, mode = "str"):
    """
    mode = "int", "float", "str"
    """
    arr = []
    element = ""
    for i in range(0, len(line)):
        if line[i] == " " or i + 1 == len(line):
            if i + 1 == len(line) and line[i] != "\n":
                element += line[i]
            if len(element) == 0:
                continue
            if mode == "float":
                try:
                    element = float(element)
                except:
                    raise ValueError("Value in input file is not a float")
            elif mode == "int":
                try:
                    element = int(element)
                except:
                    raise ValueError("Value in input file is not a int")
            arr.append(element)
            element = ""

        else:
            element += line[i]
    return arr










