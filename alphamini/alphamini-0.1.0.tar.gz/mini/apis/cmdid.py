#!/usr/bin/env python3

import enum


@enum.unique
class PCProgramCmdId(enum.Enum):
    """
    pcCodeMao的命令号配置
    """

    # IM_VERSION = 0x01
    # request
    RESPONSE_BASE = 1000

    """
    /**
     * 播放动作
     */
    """
    PLAY_ACTION_REQUEST = 1

    """
    /**
     * 移动机器人
     */
     """
    MOVE_ROBOT_REQUEST = 2

    """
    /**
     * 停止动作
     */
     """
    STOP_ACTION_REQUEST = 3

    """
    /**
     * 播放tts
     */
     """
    PLAY_TTS_REQUEST = 4

    """
    /**
     * 人脸识别
     */
     """
    FACE_DETECT_REQUEST = 5

    """
    /**
     * 识别人脸 （男性 女性）
     */
     """
    FACE_ANALYSIS_REQUEST = 6

    """
    /**
     * 物体 手势 花草识别
     */
     """
    RECOGNISE_OBJECT_REQUEST = 7

    """
    /**
     * 识别到某人
     */
     """
    FACE_RECOGNISE_REQUEST = 8

    """
    /**
     * 拍照
     */
     """
    TAKE_PICTURE_REQUEST = 9

    """
    /**
     * 播放表情
     */
     """
    PLAY_EXPRESSION_REQUEST = 10

    """
    /**
     *设置嘴巴灯
     */
     """
    SET_MOUTH_LAMP_REQUEST = 11

    """
    /**
     * 订阅红外检测障碍物距离：监听
     */
     """
    SUBSCRIBE_INFRARED_DISTANCE_REQUEST = 12

    """
    /**
     * 订阅机器人姿态：监听
     */
     """
    SUBSCRIBE_ROBOT_POSTURE_REQUEST = 13

    """
    /**
     * 订阅拍头事件：监听
     */
     """
    SUBSCRIBE_HEAD_RACKET_REQUEST = 14

    """
    /**
     * 控制行为
     */
     """
    CONTROL_BEHAVIOR_REQUEST = 15

    """
    /**
     * 获取版本号
     */
    """
    GET_ROBOT_VERSION_REQUEST = 16
    GET_ROBOT_VERSION_RESPONSE = RESPONSE_BASE + GET_ROBOT_VERSION_REQUEST

    """
    /**
     * 获取红外距离
     */
     """
    GET_INFRARED_DISTANCE_REQUEST = 19

    """
    /**
     * 停止所有操作
     */
     """
    REVERT_ORIGIN_REQUEST = 20

    """
    /**
     * 断开tcp
     */
     """
    DISCONNECTION_REQUEST = 21

    """
    /**
     * 开关嘴巴灯
     */
     """
    SWITCH_MOUTH_LAMP_REQUEST = 22

    """
    /**
     * 播放音效
     */
     """
    PLAY_AUDIO_REQUEST = 23

    """
    /**
     * 停止音效
     */
     """
    STOP_AUDIO_REQUEST = 24

    """
    /**
     * 获取音效列表
     */
     """
    GET_AUDIO_LIST_REQUEST = 25

    """
    /**
     * 翻译
     */
     """
    TRANSLATE_REQUEST = 26

    """
    /**
     * 百科
     */
     """
    WIKI_REQUEST = 27

    """
    /**
     * 改变机器人音量
     */
     """
    CHANGE_ROBOT_VOLUME_REQUEST = 28

    """
    /**
     * 播放在线音乐
     */
     """
    PLAY_ONLINE_MUSIC_REQUEST = 29

    """
    /**
     * 人脸侦测任务(持续侦测)：监听
     */
     """
    FACE_DETECT_TASK_REQUEST = 30
    """
    /**
     * 获取熟人列表
     */
     """
    GET_REGISTER_FACES_REQUEST = 31

    """
    /**
     * 人脸识别（持续识别）：监听
     */
     """
    FACE_RECOGNISE_TASK_REQUEST = 32

    """
    /**
     * 获取机器人动作列表
     */
     """
    GET_ACTION_LIST = 33

    """
    /**
     * 控制机器人录音/播放/暂停等
     */
     """
    CONTROL_ROBOT_AUDIO_RECORD = 34

    """
    /**
     * 语音识别：监听
     */
     """
    SPEECH_RECOGNISE = 35

    """
    /**
     * 获取服务器信息
     */
     """
    GET_SERVER_INFO = 36  # TODO

    """
    /**
     * 播放自定义动作
     */
     """
    PLAY_CUSTOM_ACTION_REQUEST = 37

    """
    /**
     * 停止自定义动作
     */
     """
    STOP_CUSTOM_ACTION_REQUEST = 38

    """
    /**
     * 停止语音识别
     */
    """
    STOP_SPEECH_RECOGNISE_REQUEST = 39
