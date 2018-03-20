#coding=utf-8

#以下是进程类
########################################################################################################################

#进程类的定义
class process():
    def __init__(self,pid,priority):
        self.pid = pid
        self.cpu_state = None
        self.memory = None
        self.open_file = None
        self.status = 'ready'
        self.childs = []
        self.priority = priority
        self.father = None
        self.reqRes = {}

    #进程创建进程，参数1为子进程id,参数2位子进程优先级
    def create_process(self,child_pid,child_priority):
        child_process = process(child_pid,child_priority)
        child_process.father = self
        tempProcess = None
        #下面的操作处理子进程列表
        if int(self.priority) >= int(child_priority):
            readyList_add(child_process)
            if self.childs == []:
                self.childs.append(child_process)
            else:
                for c in self.childs:
                    if int(c.priority) == int(child_priority):
                        pass
                    else:
                        tempProcess = c
                        break
                if tempProcess == None:
                    self.childs.append(child_process)
                else:
                    self.childs.insert(self.childs.index(tempProcess),child_process)
            scheduler()

        else:
            global  running_process
            running_process = child_process
            readyList_add(self)
            scheduler()

    #销毁进程，同时销毁由其创建的子进程。
    def destroy_process(self,pid):
        if running_process.pid == pid:
            for p in running_process.childs:
                self.destroy_process(p.pid)
            timeOut()
        else:
            for p in readyList:
                if p.pid == pid:
                    readyList.remove(p)
                    for i in p.childs:
                        self.destroy_process(i.pid)
            for p in blockList:
                if p.pid == pid:
                    blockList.remove(p)
                    for i in p.childs:
                        self.destroy_process(i.pid)
            timeOut()

    #进程申请资源，参数1为资源id，参数2位资源数量
    def requestSource(self,rid,count):
        global rList,running_process
        if rid not in ridList:
            print("对不起，无此资源")
            return
        else:
            for r in rList:
                if rid == r.rid:
                    if int(rList[rList.index(r)].maxCount )< int(count):
                        print('对不起，超出资源最大数量。')
                    elif int(rList[rList.index(r)].count )>=int( count):
                        rList[rList.index(r)].count -= int(count)
                        self.reqRes[rid] = count
                        scheduler()
                    elif int(rList[rList.index(r)].count )< int(count):
                        blockList_add(self)
                        self.status = 'blocked'
                        running_process = readyList[0]
                        readyList_remove(readyList[0])
                        scheduler()
    #进程释放资源，参数为资源id
    def releaseSource(self,rid):
        global rList
        if rid not in ridList or rid not in self.reqRes:
            print("资源输入错误或此进程没有占用此资源")
            return
        else:
            for r in rList:
                if rid == r.rid:
                    r.count += self.reqRes[rid]
            self.reqRes = self.reqRes.pop(rid)
            timeOut()


    #得到进程实体
    def get_self(self):
        return self
    #得到进程的父进程
    def get_father(self):
        return self.father

########################################################################################################################

#资源类的定义
class resource():
    def __init__(self,rid,maxCount):
        self.rid = rid  #资源名
        self.maxCount =maxCount #资源初始数量
        self.count = maxCount
        self.waitingList = []  #资源请求列表

def delete_process(pid):
    if pid in processIdList:
        processIdList.remove(pid)
    for p in readyList:
        if p.pid == pid:
            temp_process = p
            readyList_remove(temp_process)
            processIdList.remove(pid)
        for i in p.childs:
            delete_process(i.pid)

    for p in blockList:
        if p.pid == pid:
            temp_process = p
            blockList_remove(temp_process)
            processIdList.remove(pid)
        for i in p.childs:
            delete_process(i.pid)


#模拟时钟中断
def timeOut():
    if readyList != []:
        global running_process
        running_process.status = 'ready'
        readyList_add(running_process)
        readyList[0].status = 'running'
        running_process = readyList[0]
        readyList_remove(readyList[0])
        scheduler()
    else:
        scheduler()

#指出当前正在运行的进程
def scheduler():
    global running_process
    print(running_process.pid)


#用于时钟中断时，从就绪列表去除进程
def readyList_remove(process):
    readyList.remove(process)

#用于时钟中断时，从阻塞列表去除进程
def blockList_remove(process):
    blockList.remove(process)

#将进程按照优先级插入到就绪列表的一定位置
def readyList_add(process):
    tempProcess = None
    if readyList == []:
        readyList.append(process)
    else :
        for p in readyList:
            if int(p.priority) >= int(process.priority):
                pass
            else:
                tempProcess = p
                break
        if tempProcess == None:
            readyList.append(process)
        else:
            readyList.insert(readyList.index(tempProcess),process)

#将进程按照优先级插入到阻塞列表的一定位置
def blockList_add(process):
    tempProcess = None
    if blockList == []:
        blockList.append(process)
    else :
        for p in blockList:
            if int(p.priority) >= int(process.priority):
                pass
            else:
                tempProcess = p
                break
        if tempProcess == None:
            blockList.append(process)
        else:
            blockList.insert(blockList.index(tempProcess), process)

#回到初始状态
def init():
    root = process('root', 0)
    global running_process, rList, processIdList, blockList, readyList
    running_process = root
    rList = [ra, rb, rc]
    processIdList = ['root']
    blockList = []
    readyList = []
    scheduler()
########################################################################################################################

def parseCMD():
    global running_process
    cmds= input("请输入命令").strip().split()
    if cmds == []:
        print("对不起，请输入正确的命令")
    elif cmds[0] == 'init' :
        if len(cmds) == 1:
            init()
        else:
            print("对不起，init命令没有参数")
    elif cmds[0] == 'cr':
            if len(cmds) == 3:
                if cmds[1] not in processIdList:
                    if int(cmds[2]) >= 1 and int(cmds[2] )<= 3:
                        running_process.create_process(cmds[1], cmds[2])
                        processIdList.append(cmds[1])
                    else:
                        print("对不起，进程优先级为1-3,越大优先级越高")
                else:
                    print("对不起，此PID已存在")
            else:
                print("对不起，输入错误，cr命令有两个参数")

    elif cmds[0] == 'de':

            if len(cmds) == 2:
                if cmds[1] in processIdList:
                    delete_process(cmds[1])
                    if running_process.pid == cmds[1]:
                        running_process = readyList[0]
                        readyList_remove(readyList[0])
                        scheduler()
                    else:
                        timeOut()
                else:
                    print("对不起，进程不存在")
            else:
                print("对不起，输入错误，cr命令有一个参数")
    elif cmds[0] == 'req':
            if len(cmds) == 3:
                if cmds[1] in ridList:
                    running_process.requestSource(cmds[1],cmds[2])
                else:
                    print("对不起，资源不存在")
            else:
                print("对不起，req命令要求两个参数")
    elif cmds[0] == 'rel':
            if len(cmds) == 2:
                running_process.releaseSource(cmds[1])
            else:
                print("对不起，rel命令要求一个参数")
    elif cmds[0] == 'to':
        if len(cmds) == 1:
            timeOut()
        else:
            print("对不起，to命令没有参数")
    else:
        print("对不起，请输入正确的命令")

########################################################################################################################

if __name__ == "__main__":

    global running_process, rList,processIdList,blockList,readyList
    running_process = process('root', 0)
    processIdList = ['root']
    ra = resource('R1', 3)
    rb = resource('R2', 3)
    rc = resource('R3', 3)
    rList = [ra, rb, rc]
    ridList = [ra.rid, rb.rid, rc.rid]
    blockList = []
    readyList = []
    while True:
        parseCMD()