# -*- coding: utf-8 -*-
import psutil
import os
import logging
import configparser
import sched
import time
import json
import traceback

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='monitor.log',
                    filemode='a')


# 监控windows系统所有进程服务任务。定时任务执行，发现进程名系统中不存在，执行对应的启动命令
class Monitor:
    process_system = []

    def __init__(self):
        self.process_system = []
        self.process_dic = {}
        # 运行间隔时间 单位:s 默认值。具体从JSON配置文件中读取
        self.interval_time = 60 * 5
        self.read_config_json()

    # 通过JSON的方式读取配置文件
    def read_config_json(self):
        with open('config.json','r') as f:
            config_data = json.load(f)
            self.interval_time = config_data['interval_sec']
            for program in config_data['program_list']:
                # print(cf.get(sec, 'name'), cf.get(sec, 'cmd'))
                self.process_dic[program['name']] = {'name': program['name'],'path': program['path'], 'cmd': program['cmd'], 'status': 0}

    # 执行
    def execute(self):
        # 获取当前计算机的pid
        self.process_system = list(psutil.process_iter())
        # 清除process_dic的status
        for key in self.process_dic:
            self.process_dic[key]['status'] = 0

        # 判断每个进程的状态
        for item in self.process_system:
            # print(item.name(),item.pid)

            if item.name() in self.process_dic:
                self.process_dic[item.name()]['status'] = 1
                print("find process name=" + item.name() + ", pid=" + str(item.pid) + "\n")

        # 根据每个进程的状态，确定要不要执行cmd
        for key in self.process_dic:
            if self.process_dic[key]['status'] == 0:  # 进程不存在，重新启动程序
                try:
                    path = self.process_dic[key]['path']
                    cmd = self.process_dic[key]['cmd']
                    # 切换目录
                    os.chdir(path)
                    # 执行命令
                    os.popen(cmd)
                    logging.info("restart {name}".format(name=key))
                except:
                    logging.exception("restart {name} error".format(name=key))
                    traceback.print_exc()
        return 0


# 定时执行器
class MonitorSchedule:

    def __init__(self, monitor):
        self.schedule = sched.scheduler(time.time, time.sleep)
        self.monitor = monitor

    def func(self):
        self.monitor.execute()
        self.schedule.enter(monitor.interval_time, 0, self.func, ())

    def start(self):
        self.schedule.enter(0, 0, self.func, ())
        self.schedule.run()


if __name__ == '__main__':
    monitor = Monitor()
    server = MonitorSchedule(monitor)
    server.start()
