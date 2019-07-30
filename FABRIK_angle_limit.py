import math


# расстояние между двумя точками
def distBetweenPoints(point_1, point_2): # Функция, вычисляющая расстояние между 2 точками
    return math.sqrt(sum([(a - b) ** 2 for a, b in zip(point_1, point_2)]))

# функция вычисления угла при прямом следовании
def Forward_func_angle(arrayJointpositions):
    perenos=[[a-b for a,b in zip(arrayJointpositions[-1],arrayJointpositions[-2])],
             [a-b for a,b in zip(arrayJointpositions[0],arrayJointpositions[1])]]
    angle1 = math.degrees(math.atan2(perenos[0][1],perenos[0][0])) #при расчете через atan2 первый элемент есть y, второй x
    angle2 = math.degrees(math.atan2(perenos[1][1],perenos[1][0]))
    angle = math.fabs(angle1-angle2)
    if angle1>angle2 and perenos[0][0]<perenos[1][0]:
        a=360-angle #print('надо вычитать используется условие 1', 360-angle)  #условия заданы таким способом, что
    elif angle1>angle2 and perenos[0][0]>perenos[1][0]:                        #по правую руку идет 0 градусов,
        a=360-angle #print('надо вычитать используется условие 2', 360-angle)  #по левую 180
    else:
        a=angle #print('не надо вычитать', angle)
    return(a)

# функция вычисления угла при обратном следовании
'''другая функция т.к. используются другие элементы из массива arrayJointpositions. В принципе можно записать под одной
функцией две функции расчета угла, добавив дополнительное условие'''
def Backward_func_angle(arrayJointpositions):
    perenos=[[a-b for a,b in zip(arrayJointpositions[0],arrayJointpositions[1])],
             [a-b for a,b in zip(arrayJointpositions[2],arrayJointpositions[1])]]
    angle1 = math.degrees(math.atan2(perenos[0][1],perenos[0][0]))
    angle2 = math.degrees(math.atan2(perenos[1][1],perenos[1][0]))
    angle = math.fabs(angle1-angle2)
    if angle1>angle2 and perenos[0][0]<perenos[1][0]:
        a= 360 - angle #print('надо вычитать используется условие 1', 360-angle)
    elif angle1>angle2 and perenos[0][0]>perenos[1][0]:
        a= 360 - angle #print('надо вычитать используется условие 2', 360-angle)
    else:
        a= angle #print('не надо вычитать', angle)
    return(a)

#ограничевующая функция
def limitation(arrayJointpositions,distBeetweenJointsAB,distBeetweenJointsBC,angle,follow):
    if angle - 90 < 90:      #условие определяет с каким градусом необходимо пересчитать следующую позицию
        angle = 90
    elif angle - 90 > 180:
        angle = 270
    AB=[b-a for a,b in zip(arrayJointpositions[1],arrayJointpositions[0-follow])]
    cos=math.cos(math.radians(angle))
    sin=math.sin(math.radians(angle))
    r_BC = [AB[0]*cos-AB[1]*sin, AB[0]*sin + AB[1]*cos] #производит поворот вектора на заднный угол против часовой стрелки
    BC=[a+b for a,b in zip(arrayJointpositions[-2],r_BC)] #но с длиной AB
    #перерасчет координаты с учетом длины BC
    koef=distBeetweenJointsBC/distBeetweenJointsAB
    new_r_BC=[koef*i for i in r_BC]
    new_BC = [new_r_BC[i]+arrayJointpositions[1][i] for i in range(len(arrayJointpositions[1]))]
    return(new_BC) #насамом деле не BC, а ккордината точки C

#расчета угла для вектора состоящего из корневого узла и дочернего узла, а также для расчета угла по оси Z
#данная функция изменяется или переписывается в зависимости от особенностей конструкции
def angle_root_and_XZ(array):
    angle =  math.degrees(math.atan2(array[1],array[0]))
    if angle < 0:
        angle = 360 + angle
    return(angle)

def main():
    target = [14, 34, 3] #координаты целевой точки
    arrayOfPositions = [[0, 10],[0,20],[0,30],[0,45]] #начальный массив точек; координаты положения звеньев манипулятора
    tol = 0.02 #допустимое значение (расстояние); 
    X = target[0]
    Z = target[-1]  #z координата цели
    if target[0] == 0:
        target = target[1:3]
    else:
        length = distBetweenPoints([0,0,0],target)
        coordinate_x = math.sqrt((length**2)-target[1]**2)
        target = target[0:2]
        target[0] = coordinate_x
    #вычисляем расстояние между двумя узлами
    distBeetweenJoints = [distBetweenPoints(a, b) for a, b in
                          zip(arrayOfPositions, arrayOfPositions[1:])]
    #print(distBeetweenJoints)
    #print(arrayOfPositions[:])


    if distBetweenPoints(arrayOfPositions[0], target) > sum(distBeetweenJoints):
        #print('Цель недостижима')
        newPositions = arrayOfPositions[:]#массив новых значений узлов
        for key, value in enumerate(arrayOfPositions[:-1]):
            r = distBetweenPoints(target, value)
            lam = distBeetweenJoints[key] / r

            zippedArrays = zip([axisValue * (1 - lam) for axisValue in arrayOfPositions[key]],
                               [axisValue * lam for axisValue in target])

            newPositions[key+1] = [value_1 + value_2 for value_1, value_2 in zippedArrays]
        #print(newPositions)


    else:
        #print('Цель достижима')
        b = arrayOfPositions[0]#запоминаем корневую точку
        #DIFa = distBetweenPoints(arrayOfPositions[len(arrayOfPositions)-1], target)

        while True:
            #прямое следование
            follow = 1 #переменная для определения следования, учавствует в ограничевающей функции
            arrayOfPositions[len(arrayOfPositions)-1] = target #
            newPositions = arrayOfPositions#переменная в которую заносится начальный массив точек, а далее уже
                                            # новый (высчитанный)
            #print(newPositions)
            c = len(arrayOfPositions)-1 #индексная перменная
            cc=0 #индексная переменная
            k=0 #индексаня переменная
            for key in range(len(newPositions[:-1])):
                key=c-key
                r = distBetweenPoints(newPositions[key], newPositions[key-1])
                lam = distBeetweenJoints[key-1] / r

                zippedArrays = zip([axisValue * (1 - lam) for axisValue in newPositions[key]],
                                   [axisValue * lam for axisValue in newPositions[key-1]])
                newPositions[key-1] = [value_1 + value_2 for value_1, value_2 in zippedArrays]
                cc += 1
                if cc > 1:
                    arrayJointpositions = newPositions[-3-k:len(arrayOfPositions)-k]
                    angle = Forward_func_angle(arrayJointpositions)
                    #print('angle',angle)
                    if 0 <= angle-90 <=180:
                        print('ничего не надо делать1')
                    else:
                        limitPosition = limitation(arrayJointpositions,distBeetweenJoints[cc-3-2*k],
                                                   distBeetweenJoints[cc-3-2*k-1],angle, follow)
                        newPositions[-3-k]=limitPosition


                    k+=1
            #print(newPositions)

            #обратное следование
            follow = 0#переменная для определения следования, учавствует в ограничевающей функции
            newPositions[0] = b
            cc=0 #индексная переменная
            k=0 #индексаня переменная
            angle_rotation = [i for i in range(len(arrayOfPositions)-2)]
            for key in range(len(arrayOfPositions)-1):
                r = distBetweenPoints(newPositions[key], newPositions[key+1])
                lam = distBeetweenJoints[key] / r

                zippedArrays = zip([axisValue * (1 - lam) for axisValue in newPositions[key]],
                                   [axisValue * lam for axisValue in newPositions[key+1]])

                newPositions[key+1] = [value_1 + value_2 for value_1, value_2 in zippedArrays]
                cc+=1
                if cc>1:
                    arrayJointpositions = newPositions[k:k+3]
                    angle = Backward_func_angle(arrayJointpositions)
                    #print('angle2',angle)
                    #print(arrayJointpositions)
                    if 0 <= angle-90 <=180:
                        print('ничего не надо делать2')
                    else:
                        limitPosition = limitation(arrayJointpositions,distBeetweenJoints[k],
                                                           distBeetweenJoints[k+1], angle, follow)
                        newPositions[2+k]=limitPosition
                    angle_rotation[k] = Backward_func_angle(newPositions[k:k+3])
                    k+=1
                #sumAngle = sum() позже добаавится доп. условие выхода из цикла while. Цель не всегда может быть достижима

            angle = angle_root_and_XZ([a-b for a,b in zip(newPositions[1],newPositions[0])])#считаем угол на который должно быть повернуто первое ребро
            #print(newPositions)

            angle_rotation = [angle_rotation[i]-90 for i in range(len(angle_rotation))]
            angle_rotation.insert(0,angle) #добавляем рассчитанный угол для первого ребра на нулевую позицию массива angle_rotation
            print('углы поворота для звеньев', angle_rotation)
            arrayOfPositions = newPositions #переинициализация перменной новым массивом рассчитанных узлов
                                            #для работы цикла while и участия tol
            DIFa = distBetweenPoints(newPositions[len(newPositions)-1], target)
            #print(DIFa)
            if DIFa <= tol or (DIFa >= tol and sum(angle_rotation[0:len(angle_rotation)]) % 90 == 0):
                break
    #print('target',target)
    targetXZ = target
    targetXZ[1]=Z #заменяем координату Y на координату Z
    targetXZ[0]=X
    targetXZ.reverse() #переворачиваем
    #print(targetXZ)
    angleXZ = (angle_root_and_XZ(targetXZ)-90)/1.8
    print('угол поворота d плоскости XZ',angleXZ)
if __name__ == "__main__":
    main()
