# -*- coding: utf-8 -*-

from .pypack.fylo.controlserver import Controlserver, ConnectType

class UserApi:

    def __init__(self):
        self._control_server = Controlserver()
        if self._control_server == None:
            exit(0)

#=============================================Version Management=================================================================#

    def check_firmware_version(self, plane_id):
        '''
        检查飞机固件版本是否需要升级。如果需要升级，请使用手机APP进行升级
        
        :param plane_id: 需要检查的飞机编号。如果plane_id为-1，则检测所有已经连接的飞机
        :return: 
                  | plane_id:对应飞机需要升级固件 
                  | -2:飞机无需更新 
                  | -3:参数错误 
                  | -4:飞机未连接 
                  | -5:网络异常
        ---------------------------------
        check the plane's firmware version. If the plane need to update, please use App to update.
        
        :param plane_id: pland id you want to check.
        :return: 
                  | plane_id:
                  | -2:plane don't need to update
                  | -3:parameter error
                  | -4:plane not connect
                  | -5:network error
        '''
        return self._control_server.check_firmware_version(plane_id)

#=============================================System Config======================================================================#

    def connect(self, connect_type):
        '''
        通过网络或者中继器连接到基站
            
        :param connect_type: 连接方式 ConnectType.Network 或者 ConnectType.Serial
        :return: True:成功 False:失败
        ---------------------------------
        connect to stations using WIFI or Repeater
        
        :param connect_type: ConnectType.Network or ConnectType.Serial
        :return: True or False
        '''
        return self._control_server.connect(connect_type)
        
    def disconnect(self):
        '''
        断开网络或者中继器连接
        
        ---------------------------------
        disconnect from WIFI or Repeater
        '''
        self._control_server.disconnect()
        
    def get_connect_status(self):
        '''
        获取网络链接状态
        
        :return: 1:已连接 0:未连接
        ---------------------------------
        get connection status
        
        :return: 1:connected 0:disconnected
        '''
        return self._control_server.get_connect_status()
        
#=============================================Station Config=====================================================================#

    def station_state_demarcate(self):
        '''
        基站标定
        
        ---------------------------------
        calibrate stations
        
        '''
        self._control_server.station_state_demarcate()

    def get_station_demarcate_state(self):
        '''
        获取基站标定状态
        
        :return: 
                  | 0:未标定/标定失败 
                  | 1:标定中 
                  | 2:标定完成
        ---------------------------------
        get status of station calibration
        
        :return:
                  | 0:calibration failed
                  | 1:on calibrating
                  | 2:calibration finished
        '''
        return self._control_server.get_station_demarcate_state()
        
    def get_station_coordinate(self, station_id):
        '''
        获取基站坐标(x, y)
        
        :param station_id: 基站编号
        :return: (x, y)
        ---------------------------------
        get station coordinate
        
        :param station_id: station id
        :return: (x, y)
        '''
        return self._control_server.get_station_coordinate(station_id)

    def get_station_battery(self, station_id):
        '''
        获取基站电量百分比
        
        :param station_id: 基站编号
        :return: 
                  | -1: 未获取到电量 
                  | 0-100: 电量百分比
        ---------------------------------
        get battery level of station
        
        :param station_id: station id
        :return:
                  | -1: getting battery level failed
                  | 0-100: battery level
        '''
        return self._control_server.get_station_battery(station_id)

#=============================================Plane Config=======================================================================#

    def plane_sys_update_firmware(self, firmware_path):
        '''
        更新连接上的所有飞机的固件
        
        :param firmware_path: 固件所在的路径
        ---------------------------------
        update firmware of all connected drones
        
        :param firmware_path: path to firmware
        '''
        self._control_server.plane_sys_update_firmware(firmware_path)

    def plane_sys_get_firmware_update_rate(self):
        '''
        获取固件上传进度

        :return: 
                  | 飞机固件上传进度百分比:正常传输
                  | -1: 无需更新 
                  | -2: 固件错误 
                  | -3: 参数错误 
                  
        .. warning::
          用户接口都是串行处理，固件上传传输过程中，如果需要获取进度，则需要在线程中调用该函数进行获取
        ---------------------------------
        Get firmware uploading progress 
        
        :return:
                  | uploading progress percent: normal uploading
                  | -1: no need uploading
                  | -2: firmware error
                  | -3: parameter error
                  
        .. warning::
          only can be called in other threads while uploading
        '''
        return self._control_server.plane_sys_get_firmware_update_rate()

    def plane_sys_reset_id(self, src_id, tar_id):
        '''
        修改飞机id编号

        :param src_id: 原飞机编号
        :param tar_id: 目标飞机编号
        ---------------------------------
        change plane id
        
        :param src_id: current id
        :param tar_id: new id
        '''
        self._control_server.plane_sys_reset_id(src_id, tar_id)

    def plane_sys_init(self, yaw = -1):
        '''
        定桩，以当前0号飞机坐标为(0,0,0)建立坐标系，并为所有飞机设置当前坐标
        
        :param yaw: 0号飞机偏航角（度）
        
        .. warning::
          飞机起飞前必须进行，并且要求get_aux_setup、get_range_safe返回true时方可起飞
        ---------------------------------
        Synchronization positions, Establish coordinate system based on No. 0 plane, and update all connected drones' coordinates
        
        :param yaw: No. 0 drone's yaw angle(°)
        
        .. warning::
          must be called before takeoff, meanwhile, make sure get_aux_setup and get_range_safe return true.
        '''
        self._control_server.plane_sys_init(yaw)

    def plane_sys_timesync(self):
        '''
        同步飞机时间
        
        ---------------------------------
        Synchronization timing 
        
        '''
        self._control_server.plane_sys_timesync()

    def plane_sys_auto_config(self, plane_id_list, yaw = -1):
        '''
        自动进行定桩和授时

        :param plane_id_list: 指定飞机编号列表
        :param yaw: 0号飞机偏航角（度）
        :return: True:成功 False:不成功
        ---------------------------------
        auto synchronize positions and timing
        
        :param plane_id_list: drones indices list
        :param yaw: No. 0 drone's yaw angle(°)
        :return: True or False
        '''
        return self._control_server.plane_sys_auto_config(plane_id_list, yaw)

    def plane_sys_enter_calmag(self, plane_id):
        '''
        飞机进入校磁模式
        
        :param plane_id: 飞机编号
        ---------------------------------
        calibrate compass
        
        :param plane_id: plane id
        '''
        self._control_server.plane_sys_enter_calmag(plane_id)

    def plane_sys_exit_calmag(self, plane_id):
        '''
        飞机退出校磁模式
        
        :param plane_id: 飞机编号
        ---------------------------------
        cancel Compass Calibration
        
        :param plane_id: plane id
        '''
        self._control_server.plane_sys_exit_calmag(plane_id)

    def plane_low_power_warning(self, plane_id, power):
        '''
        设置飞机电量低于设定值时通过灯语进行提示
        
        :param plane_id: 飞机编号
        :param power: 电量百分比(5~95)
        ---------------------------------
        warn with light pattern when battery level below "power"
        
        :param plane_id: plane id
        :param power: battery level
        '''
        self._control_server.plane_low_power_warning(plane_id, power)

#=============================================RealTime Control===================================================================#

    def single_fly_takeoff(self, plane_id, height, magnetism):
        '''
        实时控制飞机起飞

        :param plane_id: 飞机编号
        :param height: 起飞高度（厘米）
        :param magnetism: 是否使用磁场（1为使用，其他为不使用）
        ---------------------------------
        ask one drone to take off
        
        :param plane_id: plane id
        :param height: target height(cm)
        :param magnetism: use compass or not. 1 for yes, other for no 
        '''
        self._control_server.single_fly_takeoff(plane_id, height, magnetism)
    
    def single_fly_touchdown(self, plane_id):
        '''
        实时控制飞机降落

        :param plane_id: 飞机编号
        ---------------------------------
        ask one drone to touch down
        
        :param plane_id: plane id
        '''
        self._control_server.single_fly_touchdown(plane_id)
    
    def single_fly_forward(self, plane_id, distance):
        '''
        实时控制飞机向前飞

        :param plane_id: 飞机编号
        :param distance: 飞行距离（厘米）
        ---------------------------------
        ask one drone to fly forward a distance
        
        :param plane_id: plane id
        :param distance: forward distance(cm)
        '''
        self._control_server.single_fly_forward(plane_id, distance)
    
    def single_fly_back(self, plane_id, distance):
        '''
        实时控制飞机向后飞

        :param plane_id: 飞机编号
        :param distance: 飞行距离（厘米）
        ---------------------------------
        ask one drone to fly backwards a distance
        
        :param plane_id: plane id
        :param distance: backward distance(cm)
        '''
        self._control_server.single_fly_back(plane_id, distance)
    
    def single_fly_left(self, plane_id, distance):
        '''
        实时控制飞机向左飞

        :param plane_id: 飞机编号
        :param distance: 飞行距离（厘米）
        ---------------------------------
        ask one drone to fly left a distance
        
        :param plane_id: plane id
        :param distance: distance(cm) towards left
        '''
        self._control_server.single_fly_left(plane_id, distance)
    
    def single_fly_right(self, plane_id, distance):
        '''
        实时控制飞机向右飞

        :param plane_id: 飞机编号
        :param distance: 飞行距离（厘米）
        ---------------------------------
        ask one drone to fly right a distance
        
        :param plane_id: plane id
        :param distance: distance(cm) towards right
        '''
        self._control_server.single_fly_right(plane_id, distance)

    def single_fly_up(self, plane_id, height):
        '''
        实时控制飞机向上飞

        :param plane_id: 飞机编号
        :param height: 飞高距离（厘米）
        ---------------------------------
        ask one drone to fly up a distance
        
        :param plane_id: plane id
        :param height: up distance(cm)
        '''
        self._control_server.single_fly_up(plane_id, height)
        
    def single_fly_down(self, plane_id, height):
        '''
        实时控制飞机向下飞

        :param plane_id: 飞机编号
        :param height: 飞行高度（厘米）
        ---------------------------------
        ask one drone to fly down a distance
        
        :param plane_id: plane id
        :param height: down distance(cm)
        '''
        self._control_server.single_fly_down(plane_id, height)
        
    def single_fly_turnleft(self, plane_id, angle):
        '''
        实时控制飞机向左转

        :param plane_id: 飞机编号
        :param angle: 旋转角度（度）
        ---------------------------------
        ask one drone to turn left some degrees
        
        :param plane_id: plane id
        :param angle: rotation degrees(°)
        '''
        self._control_server.single_fly_turnleft(plane_id, angle)
        
    def single_fly_turnright(self, plane_id, angle):
        '''
        实时控制飞机向右转

        :param plane_id: 飞机编号
        :param angle: 旋转角度（度）
        ---------------------------------
        ask one drone to turn right some degrees
        
        :param plane_id: plane id
        :param angle: rotation degrees(°)
        '''
        self._control_server.single_fly_turnright(plane_id, angle)

    def single_fly_bounce(self, plane_id, height):
        '''
        实时控制飞机跳起

        :param plane_id: 飞机编号
        :param height: 飞行高度（厘米）
        ---------------------------------
        ask one drone to bounce some distance
        
        :param plane_id: plane id
        :param height: up distance(cm)
        '''
        self._control_server.single_fly_bounce(plane_id, height)

    def single_fly_straight_flight(self, plane_id, x, y, z):
        '''
        实时控制飞机飞到指定的坐标
        
        :param plane_id: 飞机编号
        :param x: 坐标x（厘米）
        :param y: 坐标y（厘米）
        :param z: 坐标z（厘米）
        ---------------------------------
        ask one drone to fly to specific position
        
        :param plane_id: plane id
        :param x: specific coordinate x(cm)
        :param y: specific coordinate y(cm)
        :param z: specific coordinate z(cm)
        '''
        self._control_server.single_fly_straight_flight(plane_id, x, y, z)
    
#=================================================Fly Dance=======================================================================#

    def multi_dance_send(self, plane_id_list):
        '''
        上传指定飞机的舞步

        :param plane_id_list: 指定飞机编号列表
        ---------------------------------
        send programs to the drones in list
        
        :param plane_id_list: the list of specific drones
        '''
        self._control_server.multi_dance_send(plane_id_list)

    def multi_dance_get_update_rate(self):
        '''
        获取舞步上传进度
        
        :return: 
                  | 飞机舞步上传进度百分比:正常传输
                  | -1:参数错误
                  | -2:选中飞机未连接
                  | -3:舞步未生成
                  | -4:信号不稳定舞步传输超时
                  | -5:舞步传输失败
                  | -6:模式切换出错
        
        .. warning::
          用户接口都是串行处理，固件上传传输过程中，如果需要获取进度，则需要在线程中调用该函数进行获取
        ---------------------------------
        get uploading progress of programs
        
        :return:
                  | uploading progress percent: normal uploading
                  | -1: parameter error
                  | -2: drones disconnection
                  | -3: no programs
                  | -4: uploading timeout
                  | -5: uploading failed
                  | -6: mode error
                  
        .. warning::
          only can be called in other threads while uploading
        '''
        return self._control_server.multi_dance_get_update_rate()
        
    def multi_fly_prepare(self, plane_id_list):
        '''
        设置飞机起飞许可

        :param plane_id_list: 指定飞机编号列表
        
        .. note::
          调用前需要先调用dance_plane_in_range，判断舞步是否在基站范围内
        ---------------------------------
        send permission for specific drones to take off
        
        :param plane_id_list: list of specific drones
        
        .. note::
          before this function is called, dance_plane_in_range should return true.
        '''
        self._control_server.multi_fly_prepare(plane_id_list)
    
    def multi_fly_takeoff(self, plane_id_list, magnetism, delay = 0):
        '''
        飞机开始执行舞步

        :param plane_id_list: 指定飞机编号列表
        :param magnetism: 是否使用磁场（1为使用，其他为不使用）
        :param delay: 延时起飞时间（毫秒）
        
        .. note::
          当舞步时间大于150秒时,会需要使用磁场进行飞行
        ---------------------------------
        ask drones in list to perform dance programs
        
        :param plane_id_list: list of specific drones
        :param magnetism: use compass or not (1 for yes, others for no)
        :param delay: time(ms) to delay before takeoff

        .. note::
          use compass when dance duration longer than 150 seconds
        '''
        self._control_server.multi_fly_takeoff(plane_id_list, magnetism, delay)
    
    def multi_fly_touchdown(self, plane_id_list):
        '''
        飞机停止执行舞步并降落

        :param plane_id_list: 指定飞机编号列表
        ---------------------------------
        ask the drones in list to stop performance and town down
        
        :param plane_id_list: list of specific drones
        '''
        self._control_server.multi_fly_touchdown(plane_id_list)

#=================================================Plane Control===================================================================#
        
    def plane_led_on(self, plane_id_list):
        '''
        飞机开灯

        :param plane_id_list: 指定飞机编号列表
        ---------------------------------
        ask the drones in list to turn on light.
        
        :param plane_id_list: list of specific drones
        '''
        self._control_server.plane_led_on(plane_id_list)
        
    def plane_led_off(self, plane_id_list):
        '''
        飞机关灯

        :param plane_id_list: 指定飞机编号列表
        ---------------------------------
        ask the drones in list to turn off light.
        
        :param plane_id_list: list of specific drones
        '''
        self._control_server.plane_led_off(plane_id_list)
        
    def plane_fly_arm(self, plane_id_list):
        '''
        低速转动螺旋桨

        :param plane_id_list: 指定飞机编号列表
        ---------------------------------
        slowly turn propellers of specific drones in list
        
        :param plane_id_list: list of specific drones
        '''
        self._control_server.plane_fly_arm(plane_id_list)
        
    def plane_fly_disarm(self, plane_id_list):
        '''
        停止低速转动螺旋桨

        :param plane_id_list: 指定飞机编号列表
        ---------------------------------
        stop turning propellers of specific drones in list
        
        :param plane_id_list: list of specific drones
        '''
        self._control_server.plane_fly_disarm(plane_id_list)
        
#=================================================Create Dance====================================================================#

    def show_dance(self):
        '''
        显示舞步仿真

        ---------------------------------
        show simulation of dance programs
        
        '''
        self._control_server.show_dance()
        
    def dance_create_start(self):
        '''
        开始编辑舞步。
        
        .. warning::
         - 生成舞步前必须调用，调用完该函数后才可为每台飞机添加舞步。
         - 多台飞机只需调用一次。
         - 舞步总时长最长为10分钟。
        ---------------------------------
        start to create dance programs
        
        .. warning::
         - should be called before dance_create_end()
         - should be called only once for multiple drones
         - total program duration should be less than 10 minutes
        '''
        self._control_server.dance_create_start()

    def dance_set_coordinate(self, plane_id, x, y):
        '''         
        设置飞机起飞坐标（x,y），零号飞机默认(0,0)坐标。

        :param plane_id: 飞机编号(0-39)
        :param x: 坐标x（厘米）
        :param y: 坐标y（厘米）
        
        .. warning::
          每台飞机的开始添加舞步前必须设置飞机坐标。
        ---------------------------------
        set one drone's initial coordinates (x, y) on ground, and the No. 0 plane's default is (0, 0)
        
        :param plane_id: plane id(0-39)
        :param x: specific coordinate x(cm)
        :param y: specific coordinate y(cm)
        
        .. warning::
          for each drone, must be called as the first step when creating dance programs
        '''
        self._control_server.dance_set_coordinate(plane_id, x , y)
        
    def dance_get_coordinate(self, plane_id):
        '''
        获取当前舞步中指定飞机位置信息(x,y,z,yaw)

        :param plane_id: 飞机编号(0-39)
        :return: 
                  | x:坐标x（厘米）
                  | y:坐标y（厘米）
                  | z:坐标z（厘米）
                  | yaw:偏航角（度）
        ---------------------------------
        get the current position and yaw of one drone in current dance programs
        
        :param plane_id: plane id
        :return:
                  | x: current coordinate x(cm)
                  | y: current coordinate y(cm)
                  | z: current coordinate z(cm)
                  | yaw: current yaw angle(°)
        '''
        return self._control_server.dance_get_coordinate(plane_id)
    
    def dance_set_speed(self, plane_id, speed):
        '''
        设置飞机速度百分比（1%-100%）

        :param plane_id: 飞机编号(0-39)
        :param speed: 飞机飞行速度百分比（1-100）
        :return: 
                  | -1:设置速度失败 
                  | 大于0的整数:返回飞机从起飞到当前动作执行完所需帧数
        ---------------------------------
        set the speed level of specific drone
        
        :param plane_id: plane id
        :param speed: target speed level(1-100)
        :return:
                  | -1: setting speed level failed
                  | positive integer：the number of frames from takeoff to the end of current movement
        '''
        return self._control_server.dance_set_speed(plane_id, speed)
    
    def dance_fly_diy(self, plane_id, x, y, z, r, g, b):
        '''
        添加自定义舞步，飞行轨迹与灯光配置由用户以每秒30帧填入，x,y,z,r,g,b的长度必须统一

        :param plane_id: 飞机编号(0-39)
        :param x: 飞机x轴坐标组成的为list或者tuple（厘米）
        :param y: 飞机y轴坐标组成的为list或者tuple（厘米）
        :param z: 飞机z轴坐标组成的为list或者tuple（厘米）
        :param r: led红色通道组成的为list或者tuple
        :param g: led绿色通道组成的为list或者tuple
        :param b: led蓝色通道组成的为list或者tuple
        :return: 
                  | -1:添加舞步失败 
                  | 大于0的整数:返回该飞机到目前为止执行舞步所需帧数
        ---------------------------------
        add diy dance programs; trajectory and lights pattern should be adjusted to 30 fps; every list of x y z r g and b should have same size.
        
        :param plane_id: plane id
        :param x: list/tuple of coordinate x(cm) in trajectory
        :param y: list/tuple of coordinate y(cm) in trajectory
        :param z: list/tuple of coordinate z(cm) in trajectory
        :param r: list/tuple of red light pattern in trajectory
        :param g: list/tuple of green light pattern in trajectory
        :param b: list/tuple of blue light pattern in trajectory
        
        :return:
                  | -1: adding diy dance programs failed
                  | positive integer: the number of frames from takeoff to the end of current movement
        '''
        return self._control_server.dance_fly_diy(plane_id, x, y, z, r, g, b)
        
    def dance_fly_wait(self, plane_id, frequent, mode, r, g, b):
        '''
        添加舞步悬停（帧）

        :param plane_id: 飞机编号(0-39)
        :param frequent: 悬停时间（帧）30帧 = 1秒
        :param mode: 灯光模式（0:呼吸 1:七彩 2:常亮 3:关闭）
        :param r: 红色通道（0~255）
        :param g: 绿色通道（0~255）
        :param b: 蓝色通道（0~255）
        :return: 
                  | -1:添加舞步失败 
                  | 大于0的整数:返回该飞机到目前为止执行舞步所需帧数
        ---------------------------------
        add hovering movement by frame to program
        
        :param plane_id: plane id(0-39)
        :param frequent: hovering frames at 30 fps
        :param mode: flash mode of lights(0 for breathing light, 1 for colorful light, 2 for steady light, 3 for off)
        :param r: red channel(0-255)
        :param g: green channel(0-255)
        :param b: blue channel(0-255)
        :return:
                  | -1: adding hovering movement by frame to program failed
                  | positive integer: the number of frames from takeoff to the end of current movement
        '''
        return self._control_server.dance_fly_wait(plane_id, frequent, mode, r, g, b)
        
    def dance_fly_waitsec(self, plane_id, time, mode, r, g, b):
        '''
        添加舞步悬停（秒）

        :param plane_id: 飞机编号(0-39)
        :param frequent: 悬停时间（秒）
        :param mode: 灯光模式（0:呼吸 1:七彩 2:常亮 3:关闭）
        :param r: 红色通道（0~255）
        :param g: 绿色通道（0~255）
        :param b: 蓝色通道（0~255）
        :return: 
                  | -1:添加舞步失败 
                  | 大于0的整数:返回该飞机到目前为止执行舞步所需帧数
        ---------------------------------
        add hovering movement by second to program
        
        :param plane_id: plane id(0-39)
        :param frequent: hovering time(second)
        :param mode: flash mode of lights(0 for breathing light, 1 for colorful light, 2 for steady light, 3 for off)
        :param r: red channel(0-255)
        :param g: green channel(0-255)
        :param b: blue channel(0-255)
        :return:
                  | -1: adding hovering movement by second to program failed
                  | positive integer: the number of frames from takeoff to the end of current movement
        '''
        return self._control_server.dance_fly_waitsec(plane_id, time, mode, r, g, b)
        
    def dance_fly_takeoff(self, plane_id, mode, r, g, b):
        '''
        添加舞步起飞

        :param plane_id: 飞机编号(0-39)
        :param mode: 灯光模式（0:呼吸 1:七彩 2:常亮 3:关闭）
        :param r: 红色通道（0~255）
        :param g: 绿色通道（0~255）
        :param b: 蓝色通道（0~255）
        :return: 
                  | -1:添加舞步失败 
                  | 大于0的整数:返回该飞机到目前为止执行舞步所需帧数
        ---------------------------------
        add takeoff movement to program
        
        :param plane_id: plane id(0-39)
        :param mode: flash mode of lights(0 for breathing light, 1 for colorful light, 2 for steady light, 3 for off)
        :param r: red channel(0-255)
        :param g: green channel(0-255)
        :param b: blue channel(0-255)
        :return:
                  | -1: adding takeoff movement to program failed
                  | positive integer: the number of frames from takeoff to the end of current movement
        '''
        return self._control_server.dance_fly_takeoff(plane_id, mode, r, g, b)
    
    def dance_fly_touchdown(self, plane_id, mode, r, g, b):
        '''
        添加舞步降落

        :param plane_id: 飞机编号(0-39)
        :param mode: 灯光模式（0:呼吸 1:七彩 2:常亮 3:关闭）
        :param r: 红色通道（0~255）
        :param g: 绿色通道（0~255）
        :param b: 蓝色通道（0~255）
        :return: 
                  | -1:添加舞步失败 
                  | 大于0的整数:返回该飞机到目前为止执行舞步所需帧数
        ---------------------------------
        add touchdown movement to program
        
        :param plane_id: plane id(0-39)
        :param mode: flash mode of lights(0 for breathing light, 1 for colorful light, 2 for steady light, 3 for off)
        :param r: red channel(0-255)
        :param g: green channel(0-255)
        :param b: blue channel(0-255)
        :return:
                  | -1: adding touchdown movement to program failed
                  | positive integer: the number of frames from takeoff to the end of current movement
        '''
        return self._control_server.dance_fly_touchdown(plane_id, mode, r, g, b)
    
    def dance_fly_forward(self, plane_id, distance, mode, r, g, b):
        '''
        添加舞步向前飞

        :param plane_id: 飞机编号(0-39)
        :param distance: 飞行距离（厘米）
        :param mode: 灯光模式（0:呼吸 1:七彩 2:常亮 3:关闭）
        :param r: 红色通道（0~255）
        :param g: 绿色通道（0~255）
        :param b: 蓝色通道（0~255）
        :return: 
                  | -1:添加舞步失败 
                  | 大于0的整数:返回该飞机到目前为止执行舞步所需帧数
        ---------------------------------
        add flying forward movement to program
        
        :param plane_id: plane id(0-39)
        :param distance: movement distance(cm)
        :param mode: flash mode of lights(0 for breathing light, 1 for colorful light, 2 for steady light, 3 for off)
        :param r: red channel(0-255)
        :param g: green channel(0-255)
        :param b: blue channel(0-255)
        :return:
                  | -1: adding flying forward movement to program failed
                  | positive integer: the number of frames from takeoff to the end of current movement
        '''
        return self._control_server.dance_fly_forward(plane_id, distance, mode, r, g, b)
    
    def dance_fly_back(self, plane_id, distance, mode, r, g, b):
        '''
        添加舞步向后飞

        :param plane_id: 飞机编号(0-39)
        :param distance: 飞行距离（厘米）
        :param mode: 灯光模式（0:呼吸 1:七彩 2:常亮 3:关闭）
        :param r: 红色通道（0~255）
        :param g: 绿色通道（0~255）
        :param b: 蓝色通道（0~255）
        :return: 
                  | -1:添加舞步失败 
                  | 大于0的整数:返回该飞机到目前为止执行舞步所需帧数
        ---------------------------------
        add flying backward movement to program
        
        :param plane_id: plane id(0-39)
        :param distance: movement distance(cm)
        :param mode: flash mode of lights(0 for breathing light, 1 for colorful light, 2 for steady light, 3 for off)
        :param r: red channel(0-255)
        :param g: green channel(0-255)
        :param b: blue channel(0-255)
        :return:
                  | -1: adding flying backward movement to program failed
                  | positive integer: the number of frames from takeoff to the end of current movement
        '''
        return self._control_server.dance_fly_back(plane_id, distance, mode, r, g, b)
        
    def dance_fly_left(self, plane_id, distance, mode, r, g, b):
        '''
        添加舞步向左飞

        :param plane_id: 飞机编号(0-39)
        :param distance: 飞行距离（厘米）
        :param mode: 灯光模式（0:呼吸 1:七彩 2:常亮 3:关闭）
        :param r: 红色通道（0~255）
        :param g: 绿色通道（0~255）
        :param b: 蓝色通道（0~255）
        :return: 
                  | -1:添加舞步失败 
                  | 大于0的整数:返回该飞机到目前为止执行舞步所需帧数
        ---------------------------------
        add flying left movement to program
        
        :param plane_id: plane id(0-39)
        :param distance: movement distance(cm)
        :param mode: flash mode of lights(0 for breathing light, 1 for colorful light, 2 for steady light, 3 for off)
        :param r: red channel(0-255)
        :param g: green channel(0-255)
        :param b: blue channel(0-255)
        :return:
                  | -1: adding flying left movement to program failed
                  | positive integer: the number of frames from takeoff to the end of current movement
        '''
        return self._control_server.dance_fly_left(plane_id, distance, mode, r, g, b)
    
    def dance_fly_right(self, plane_id, distance, mode, r, g, b):
        '''
        添加舞步向右飞

        :param plane_id: 飞机编号(0-39)
        :param distance: 飞行距离（厘米）
        :param mode: 灯光模式（0:呼吸 1:七彩 2:常亮 3:关闭）
        :param r: 红色通道（0~255）
        :param g: 绿色通道（0~255）
        :param b: 蓝色通道（0~255）
        :return: 
                  | -1:添加舞步失败 
                  | 大于0的整数:返回该飞机到目前为止执行舞步所需帧数
        ---------------------------------
        add flying right movement to program
        
        :param plane_id: plane id(0-39)
        :param distance: movement distance(cm)
        :param mode: flash mode of lights(0 for breathing light, 1 for colorful light, 2 for steady light, 3 for off)
        :param r: red channel(0-255)
        :param g: green channel(0-255)
        :param b: blue channel(0-255)
        :return:
                  | -1: adding flying right movement to program failed
                  | positive integer: the number of frames from takeoff to the end of current movement
        '''
        return self._control_server.dance_fly_right(plane_id, distance, mode, r, g, b)
    
    def dance_fly_up(self, plane_id, height, mode, r, g, b):
        '''
        添加舞步向上飞

        :param plane_id: 飞机编号(0-39)
        :param height: 上升距离（厘米）
        :param mode: 灯光模式（0:呼吸 1:七彩 2:常亮 3:关闭）
        :param r: 红色通道（0~255）
        :param g: 绿色通道（0~255）
        :param b: 蓝色通道（0~255）
        :return: 
                  | -1:添加舞步失败 
                  | 大于0的整数:返回该飞机到目前为止执行舞步所需帧数
        ---------------------------------
        add flying up movement to program
        
        :param plane_id: plane id(0-39)
        :param height: movement distance(cm)
        :param mode: flash mode of lights(0 for breathing light, 1 for colorful light, 2 for steady light, 3 for off)
        :param r: red channel(0-255)
        :param g: green channel(0-255)
        :param b: blue channel(0-255)
        :return:
                  | -1: adding flying up movement to program failed
                  | positive integer: the number of frames from takeoff to the end of current movement
        '''
        return self._control_server.dance_fly_up(plane_id, height, mode, r, g, b)
    
    def dance_fly_down(self, plane_id, height, mode, r, g, b):
        '''
        添加舞步向下飞

        :param plane_id: 飞机编号(0-39)
        :param height: 下降距离（厘米）
        :param mode: 灯光模式（0:呼吸 1:七彩 2:常亮 3:关闭）
        :param r: 红色通道（0~255）
        :param g: 绿色通道（0~255）
        :param b: 蓝色通道（0~255）
        :return: 
                  | -1:添加舞步失败 
                  | 大于0的整数:返回该飞机到目前为止执行舞步所需帧数
        ---------------------------------
        add flying down movement to program
        
        :param plane_id: plane id(0-39)
        :param height: movement distance(cm)
        :param mode: flash mode of lights(0 for breathing light, 1 for colorful light, 2 for steady light, 3 for off)
        :param r: red channel(0-255)
        :param g: green channel(0-255)
        :param b: blue channel(0-255)
        :return:
                  | -1: adding flying down movement to program failed
                  | positive integer: the number of frames from takeoff to the end of current movement
        '''
        return self._control_server.dance_fly_down(plane_id, height, mode, r, g, b)

    def dance_fly_turnleft(self, plane_id, angle, mode, r, g, b):
        '''
        添加舞步向左转

        :param plane_id: 飞机编号(0-39)
        :param angle: 旋转角度（度）
        :param mode: 灯光模式（0:呼吸 1:七彩 2:常亮 3:关闭）
        :param r: 红色通道（0~255）
        :param g: 绿色通道（0~255）
        :param b: 蓝色通道（0~255）
        :return: 
                  | -1:添加舞步失败 
                  | 大于0的整数:返回该飞机到目前为止执行舞步所需帧数
        ---------------------------------
        add turning left movement to program
        
        :param plane_id: plane id(0-39)
        :param angle: rotation degrees 
        :param mode: flash mode of lights(0 for breathing light, 1 for colorful light, 2 for steady light, 3 for off)
        :param r: red channel(0-255)
        :param g: green channel(0-255)
        :param b: blue channel(0-255)
        :return:
                  | -1: adding flying up movement to program failed
                  | positive integer: the number of frames from takeoff to the end of current movement
        '''
        return self._control_server.dance_fly_turnleft(plane_id, angle, mode, r, g, b)
        
    def dance_fly_turnright(self, plane_id, angle, mode, r, g, b):
        '''
        添加舞步向右转

        :param plane_id: 飞机编号(0-39)
        :param angle: 旋转角度（度）
        :param mode: 灯光模式（0:呼吸 1:七彩 2:常亮 3:关闭）
        :param r: 红色通道（0~255）
        :param g: 绿色通道（0~255）
        :param b: 蓝色通道（0~255）
        :return: 
                  | -1:添加舞步失败 
                  | 大于0的整数:返回该飞机到目前为止执行舞步所需帧数
        ---------------------------------
        add turning right movement to program
        
        :param plane_id: plane id(0-39)
        :param angle: rotation degrees 
        :param mode: flash mode of lights(0 for breathing light, 1 for colorful light, 2 for steady light, 3 for off)
        :param r: red channel(0-255)
        :param g: green channel(0-255)
        :param b: blue channel(0-255)
        :return:
                  | -1: adding flying up movement to program failed
                  | positive integer: the number of frames from takeoff to the end of current movement
        '''
        return self._control_server.dance_fly_turnright(plane_id, angle, mode, r, g, b)

    def dance_fly_bounce(self, plane_id, height, mode, r, g, b):
        '''
        添加舞步跳起

        :param plane_id: 飞机编号（0-39）
        :param height: 上升距离（厘米）
        :param mode: 灯光模式（0:呼吸 1:七彩 2:常亮 3:关闭）
        :param r: 红色通道（0~255）
        :param g: 绿色通道（0~255）
        :param b: 蓝色通道（0~255）
        :return: 
                  | -1:添加舞步失败 
                  | 大于0的整数:返回该飞机到目前为止执行舞步所需帧数
        ---------------------------------
        add bounce movement to program
        
        :param plane_id: plane id(0-39)
        :param height: movement distance(cm)
        :param mode: flash mode of lights(0 for breathing light, 1 for colorful light, 2 for steady light, 3 for off)
        :param r: red channel(0-255)
        :param g: green channel(0-255)
        :param b: blue channel(0-255)
        :return:
                  | -1: adding bounce movement to program failed
                  | positive integer: the number of frames from takeoff to the end of current movement
        '''
        return self._control_server.dance_fly_bounce(plane_id, height, mode, r, g, b)
        
    def dance_fly_flip_forward(self, plane_id, mode, r, g, b):
        '''
        添加舞步向前翻滚

        :param plane_id: 飞机编号(0-39)
        :param mode: 灯光模式（0:呼吸 1:七彩 2:常亮 3:关闭）
        :param r: 红色通道（0~255）
        :param g: 绿色通道（0~255）
        :param b: 蓝色通道（0~255）
        :return: 
                  | -1:添加舞步失败 
                  | 大于0的整数:返回该飞机到目前为止执行舞步所需帧数
        ---------------------------------
        add rolling forward movement to program
        
        :param plane_id: plane id(0-39)
        :param mode: flash mode of lights(0 for breathing light, 1 for colorful light, 2 for steady light, 3 for off)
        :param r: red channel(0-255)
        :param g: green channel(0-255)
        :param b: blue channel(0-255)
        :return:
                  | -1: adding rolling forward movement to program failed
                  | positive integer: the number of frames from takeoff to the end of current movement
        '''
        return self._control_server.dance_fly_flip_forward(plane_id, mode, r, g, b)
        
    def dance_fly_flip_back(self, plane_id, mode, r, g, b):
        '''
        添加舞步向后翻滚

        :param plane_id: 飞机编号(0-39)
        :param mode: 灯光模式（0:呼吸 1:七彩 2:常亮 3:关闭）
        :param r: 红色通道（0~255）
        :param g: 绿色通道（0~255）
        :param b: 蓝色通道（0~255）
        :return: 
                  | -1:添加舞步失败 
                  | 大于0的整数:返回该飞机到目前为止执行舞步所需帧数
        ---------------------------------
        add rolling backward movement to program
        
        :param plane_id: plane id(0-39)
        :param mode: flash mode of lights(0 for breathing light, 1 for colorful light, 2 for steady light, 3 for off)
        :param r: red channel(0-255)
        :param g: green channel(0-255)
        :param b: blue channel(0-255)
        :return:
                  | -1: adding rolling backward movement to program failed
                  | positive integer: the number of frames from takeoff to the end of current movement
        '''
        return self._control_server.dance_fly_flip_back(plane_id, mode, r, g, b)
    
    def dance_fly_flip_left(self, plane_id, mode, r, g, b):
        '''
        添加舞步向左翻滚

        :param plane_id: 飞机编号(0-39)
        :param mode: 灯光模式（0:呼吸 1:七彩 2:常亮 3:关闭）
        :param r: 红色通道（0~255）
        :param g: 绿色通道（0~255）
        :param b: 蓝色通道（0~255）
        :return: 
                  | -1:添加舞步失败 
                  | 大于0的整数:返回该飞机到目前为止执行舞步所需帧数
        ---------------------------------
        add rolling left movement to program
        
        :param plane_id: plane id(0-39)
        :param mode: flash mode of lights(0 for breathing light, 1 for colorful light, 2 for steady light, 3 for off)
        :param r: red channel(0-255)
        :param g: green channel(0-255)
        :param b: blue channel(0-255)
        :return:
                  | -1: adding rolling left movement to program failed
                  | positive integer: the number of frames from takeoff to the end of current movement
        '''
        return self._control_server.dance_fly_flip_left(plane_id, mode, r, g, b)
        
    def dance_fly_flip_right(self, plane_id, mode, r, g, b):
        '''
        添加舞步向右翻滚

        :param plane_id: 飞机编号(0-39)
        :param mode: 灯光模式（0:呼吸 1:七彩 2:常亮 3:关闭）
        :param r: 红色通道（0~255）
        :param g: 绿色通道（0~255）
        :param b: 蓝色通道（0~255）
        :return: 
                  | -1:添加舞步失败 
                  | 大于0的整数:返回该飞机到目前为止执行舞步所需帧数
        ---------------------------------
        add rolling right movement to program
        
        :param plane_id: plane id(0-39)
        :param mode: flash mode of lights(0 for breathing light, 1 for colorful light, 2 for steady light, 3 for off)
        :param r: red channel(0-255)
        :param g: green channel(0-255)
        :param b: blue channel(0-255)
        :return:
                  | -1: adding rolling right movement to program failed
                  | positive integer: the number of frames from takeoff to the end of current movement
        '''
        return self._control_server.dance_fly_flip_right(plane_id, mode, r, g, b)
        
    def dance_fly_straight_flight(self, plane_id, x, y, z, mode, r, g, b):
        '''
        添加舞步直线飞行到坐标(x,y,z)

        :param plane_id: 飞机编号(0-39)
        :param x: 坐标x（厘米）
        :param y: 坐标y（厘米）
        :param z: 坐标z（厘米）
        :param mode: 灯光模式（0:呼吸 1:七彩 2:常亮 3:关闭）
        :param r: 红色通道（0~255）
        :param g: 绿色通道（0~255）
        :param b: 蓝色通道（0~255）
        :return: 
                  | -1:添加舞步失败 
                  | 大于0的整数:返回该飞机到目前为止执行舞步所需帧数
        ---------------------------------
        add straight movement to program
        
        :param plane_id: plane id(0-39)
        :param x: target position coordinate x(cm)
        :param y: target position coordinate y(cm)
        :param z: target position coordinate z(cm)
        :param mode: flash mode of lights(0 for breathing light, 1 for colorful light, 2 for steady light, 3 for off)
        :param r: red channel(0-255)
        :param g: green channel(0-255)
        :param b: blue channel(0-255)
        :return:
                  | -1: adding straight movement to program failed
                  | positive integer: the number of frames from takeoff to the end of current movement
        '''
        return self._control_server.dance_fly_straight_flight(plane_id, x, y, z, mode, r, g, b)
    
    def dance_fly_curve_flight(self, plane_id, x, y, z, direction, mode, r, g, b):
        '''
        添加舞步曲线飞行到坐标(x,y,z)

        :param plane_id: 飞机编号(0-39)
        :param x: 坐标x（厘米）
        :param y: 坐标y（厘米）
        :param z: 坐标z（厘米）
        :param direction: 飞行方向（0:顺时针 1:逆时针）
        :param mode: 灯光模式（0:呼吸 1:七彩 2:常亮 3:关闭）
        :param r: 红色通道（0~255）
        :param g: 绿色通道（0~255）
        :param b: 蓝色通道（0~255）
        :return: 
                  | -1:添加舞步失败 
                  | 大于0的整数:返回该飞机到目前为止执行舞步所需帧数
        ---------------------------------
        add curve movement to program
        
        :param plane_id: plane id(0-39)
        :param x: target position coordinate x(cm)
        :param y: target position coordinate y(cm)
        :param z: target position coordinate z(cm)
        :param direction: curve direction(0 for clockwize, 1 for anti-clockwize)
        :param mode: flash mode of lights(0 for breathing light, 1 for colorful light, 2 for steady light, 3 for off)
        :param r: red channel(0-255)
        :param g: green channel(0-255)
        :param b: blue channel(0-255)
        :return:
                  | -1: adding curve movement to program failed
                  | positive integer: the number of frames from takeoff to the end of current movement
        '''
        return self._control_server.dance_fly_curve_flight(plane_id, x, y, z, direction, mode, r, g, b)
    
    def dance_fly_surround(self, plane_id, radius, direction, mode, r, g, b):
        '''
        添加舞步环绕

        :param plane_id: 飞机编号(0-39)
        :param radius: 环绕半径（厘米）
        :param direction: 飞行方向（0:顺时针 1:逆时针）
        :param mode: 灯光模式（0:呼吸 1:七彩 2:常亮 3:关闭）
        :param r: 红色通道（0~255）
        :param g: 绿色通道（0~255）
        :param b: 蓝色通道（0~255）
        :return: 
                  | -1:添加舞步失败 
                  | 大于0的整数:返回该飞机到目前为止执行舞步所需帧数
        ---------------------------------
        add surrounding movement to program
        
        :param plane_id: plane id(0-39)
        :param radius: the radius(cm) of surrounding
        :param direction: surrounding direction(0 for clockwize, 1 for anti-clockwize)
        :param mode: flash mode of lights(0 for breathing light, 1 for colorful light, 2 for steady light, 3 for off)
        :param r: red channel(0-255)
        :param g: green channel(0-255)
        :param b: blue channel(0-255)
        :return:
                  | -1: adding surrounding movement to program failed
                  | positive integer: the number of frames from takeoff to the end of current movement
        '''
        return self._control_server.dance_fly_surround(plane_id, radius, direction, mode, r, g, b)
    
    def dance_fly_turnleft360(self, plane_id, num, mode, r, g, b):
        '''
        添加舞步左自旋转360度

        :param plane_id: 飞机编号(0-39)
        :param num: 圈数
        :param mode: 灯光模式（0:呼吸 1:七彩 2:常亮 3:关闭）
        :param r: 红色通道（0~255）
        :param g: 绿色通道（0~255）
        :param b: 蓝色通道（0~255）
        :return: 
                  | -1:添加舞步失败 
                  | 大于0的整数:返回该飞机到目前为止执行舞步所需帧数
        ---------------------------------
        add left-hand rotation movement to program
        
        :param plane_id: plane id(0-39)
        :param num: times of rotation
        :param mode: flash mode of lights(0 for breathing light, 1 for colorful light, 2 for steady light, 3 for off)
        :param r: red channel(0-255)
        :param g: green channel(0-255)
        :param b: blue channel(0-255)
        :return:
                  | -1: adding left-hand rotation movement to program failed
                  | positive integer: the number of frames from takeoff to the end of current movement
        '''
        return self._control_server.dance_fly_turnleft360(plane_id, num, mode, r, g, b)

    def dance_fly_turnright360(self, plane_id, num, mode, r, g, b):
        '''
        添加舞步右自旋转360度

        :param plane_id: 飞机编号(0-39)
        :param num: 圈数
        :param mode: 灯光模式（0:呼吸 1:七彩 2:常亮 3:关闭）
        :param r: 红色通道（0~255）
        :param g: 绿色通道（0~255）
        :param b: 蓝色通道（0~255）
        :return: 
                  | -1:添加舞步失败 
                  | 大于0的整数:返回该飞机到目前为止执行舞步所需帧数
        ---------------------------------
        add right-hand rotation movement to program
        
        :param plane_id: plane id(0-39)
        :param num: times of rotation
        :param mode: flash mode of lights(0 for breathing light, 1 for colorful light, 2 for steady light, 3 for off)
        :param r: red channel(0-255)
        :param g: green channel(0-255)
        :param b: blue channel(0-255)
        :return:
                  | -1: adding right-hand rotation movement to program failed
                  | positive integer: the number of frames from takeoff to the end of current movement
        '''
        return self._control_server.dance_fly_turnright360(plane_id, num, mode, r, g, b)
    
    def dance_create_end(self):
        '''
        结束编辑舞步，并生成舞步。多台飞机只需调用一次。
        
        :return: 
                  | 0:生成舞步成功 
                  | -1:舞步时长过长
                  | -2:舞步为空
        ---------------------------------
        stop creating dance programs, and generate programs; should be called only once for multiple drones
        
        :return:
                  | 0: generating programs success
                  | -1: the length of programs is out of limits(10 minutes)
                  | -2: the program is empty
        '''
        return self._control_server.dance_create_end()

    def dance_plane_in_range(self):
        '''
        根据基站坐标、0号飞机坐标和生成的舞步判断飞机是否会飞出基站范围。
        
        :return: 
                  | -1:没有生成舞步, 
                  | -2:无法获取0号飞机坐标, 
                  | -3:基站未标定
                  | [左,右,后,前,下,上]: 一个长度为6的list分别是左边，右边，后边，前边，上边，下边超出的距离。
                  
        .. note::
         - 如果全为0说明舞步没有超出范围
         - 准备起飞前需要进行判断，判断成功才能准备起飞
        ---------------------------------
         check how long distance toward the 6 directions all the dance programs are out of the valid area's limits
         
         :return:
                  | -1: no programs
                  | -2: no coordinates of No. 0 plane
                  | -3: not yet calibrated stations
                  | [left, right, back, front, down, up]: a list including distances out of limits toward the 6 orientation                  
         
         .. note::
           - [0, 0, 0, 0, 0, 0] means all the dance programs are in vaild area
           - should be called before takeoff, and only returning [0, 0, 0, 0, 0, 0] can all the drones take off.
        '''
        return self._control_server.dance_plane_in_range()
        
#================================================Plane State=====================================================================#

    def get_plane_list(self):
        '''
        获取已经连接的飞机id列表
        
        :return: [id0, id1, id2 ...] 飞机编号list
        ---------------------------------
        get list of connected drones
        
        :return: [id0, id1, id2 ...] plane id list
        '''
        return self._control_server.get_plane_list()
                
    def plane_exist(self, plane_id):
        '''
        判断飞机是否连接

        :param plane_id: 飞机编号
        :return: True:已连接 False:未连接
        ---------------------------------
        check whether one drone connect in
        
        :param plane_id: plane id
        :return: True for connected, False for disconnected
        '''
        return self._control_server.plane_exist(plane_id)
    
    def get_firmware_version(self, plane_id):
        '''
        获取飞机固件版本号

        :param plane_id: 飞机编号
        :return: 飞机版本号
        ---------------------------------
        get one drone's firmware version
        
        :param plane_id: plane id
        :return: the drone's firmware version
        '''
        return self._control_server.get_firmware_version(plane_id)
        
    def get_battery(self, plane_id):
        '''
        获取飞机电量百分比

        :param plane_id: 飞机编号
        :return: 整数:电量百分比
        ---------------------------------
        get one drone's battery level
        
        :param plane_id: plane id
        :return: integer: battery level
        '''
        return self._control_server.get_battery(plane_id)
        
    def get_mag_calibration_status(self, plane_id):
        '''
        获取飞机磁力计校准状态

        :param plane_id: 飞机编号
        :return: 
                  | -1(校准失败) 
                  | 0 (校准成功)
                  | 1(正在校准) 
                  | 2(未在校准)
        ---------------------------------
        get the status of one drone's compass
        
        :param plane_id: plane id
        :return:
                  | -1 calibration failed
                  | 0 calibration finished
                  | 1 on calibrating
                  | 2 no calibration
        '''
        return self._control_server.get_mag_calibration_status(plane_id)
        
    def get_coordinate(self, plane_id):
        '''
        获取飞机坐标(x,y,z)

        :param plane_id: 飞机编号
        :return: (x, y, z)
        ---------------------------------
        get one drone's coordinates(x,y,z)
        
        :param plane_id: plane id
        :return: (x, y, z)
        '''
        return self._control_server.get_coordinate(plane_id)
        
    def get_yaw(self, plane_id):
        '''
        获取飞机偏航角（度）

        :param plane_id: 飞机编号
        :return: 整数:偏航
        ---------------------------------
        get one drone's yaw angle(°)
        
        :param plane_id: plane id
        :return: integer:yaw angle(°)
        '''
        return self._control_server.get_yaw(plane_id)
        
    def get_magnetic(self):
        '''
        获取0号飞机磁场角度（度）

        :return: 整数:磁场角度
        ---------------------------------
        get the orientation angle of No. 0 plane's compass
        
        :return: integer: the orientation angle
        '''
        return self._control_server.get_magnetic()
        
    def get_aux_setup(self, plane_id):
        '''
        判断飞机是否定桩成功

        :param plane_id: 飞机编号
        :return: True:成功 False:不成功
        ---------------------------------
        check that whether one drone's Synchronization positions is successful
        
        :param plane_id: plane id
        :return: True or False
        '''
        return self._control_server.get_aux_setup(plane_id)
    
    def get_timesync(self, plane_id):
        '''
        判断飞机是否同步时间成功

        :param plane_id: 飞机编号
        :return: True:成功 False:不成功
        ---------------------------------
        check that whether one drone's Synchronization timing is successful
        
        :param plane_id: plane id
        :return: True or False
        '''
        return self._control_server.get_timesync(plane_id)
    
    def get_range_safe(self, plane_id):
        '''
        判断飞机是否处于安全范围内

        :param plane_id: 飞机编号
        :return: True:范围内 False:不在范围内
        ---------------------------------
        check that whether one drone is in valid area
        
        :param plane_id: plane id
        :return: True or False
        '''
        return self._control_server.get_range_safe(plane_id)
     
    def get_takeoff_allow(self, plane_id):
        '''
        判断飞机起飞许可

        :param plane_id: 飞机编号
        :return: True:已授权 False:未授权
        ---------------------------------
        check that whether one drone is permitted to take off
        
        :param plane_id: plane id
        :return: True or False
        '''
        return self._control_server.get_takeoff_allow(plane_id)
    
    def get_dance_state(self, plane_id):
        '''
        判断飞机载入的舞步是否与本地生成舞步一致

        :param plane_id: 飞机编号
        :return: True:一致 False:不一致
        ---------------------------------
        check that whether one drone's program is same as the one local generated
        
        :param plane_id: plane id
        :return: True or False
        '''
        return self._control_server.get_dance_state(plane_id)

#=====================================================Debug==================================================================#

    def show_plane(self):
        '''
        打印飞机各项状态

        ---------------------------------
        print the status of all the drones
        
        '''
        self._control_server.show_plane()
        
    def show_plane_sensor(self):
        '''
        打印飞机传感器状态
        ::
        
            location sensor           是否获取到位置信息
            gyro                      是否检测到陀螺仪
            accelerometer             是否检测到加速度计
            magnetometer              是否检测到磁力计
            absolute pressure         是否检测到气压计
            RGB                       是否检测到rgb
            TOF                       是否检测到tof
            Ahrs                      imu是否收敛
            gyro calibration          陀螺仪是否校准
            accelerometer calibration 加速度计是否校准
            magnetometer calibration  磁力计是否校准
            magnetometer disturb      磁干扰
        ---------------------------------
        print the sensor status of all the drones
        ::
        
            location sensor           whether get the position
            gyro                      whether find gyro
            accelerometer             whether find accelerometer
            magnetometer              whether find magnetometer
            absolute pressure         whether find absolute pressure
            RGB                       whether find rgb
            TOF                       whether find tof
            Ahrs                      whether imu converge
            gyro calibration          whether calibrated gyro
            accelerometer calibration whether calibrated accelerometer
            magnetometer calibration  whether calibrated magnetometer
            magnetometer disturb      whether be disturbed by magnetism
        '''
        self._control_server.show_plane_sensor()

    def show_station(self):
        '''
        打印基站标定结果
        
        ---------------------------------
        print results of station calibration
        
        '''
        self._control_server.show_station()