from qcodes.instrument.ip import IPInstrument
import qcodes.utils.validators as vals


class AmSsm23q(IPInstrument):
    SCL_OPCODE = chr(0) + chr(7)
    DI_LOWER = 0
    DI_UPPER = 95000  # MAX=95197 approx. 95000/20000=4.75 revolution

    def __init__(self, address=None, port=7776, **kwargs):
        super().__init__('AmSsm23q_', address, port, timeout=5, terminator='\r', persistent=False,
                         write_confirmation=True, **kwargs)
        self.add_parameter('init_mode',
                           label='Initial power up mode setting',
                           set_cmd=self.SCL_OPCODE + 'PM{}',
                           get_cmd=self.SCL_OPCODE+'PM',
                           get_parser=lambda s: s.partition('=')[2])

        self.add_parameter('alarm_code',
                           label='Alarm code state',
                           set_cmd=False,
                           get_cmd=self.SCL_OPCODE+'AL',
                           get_parser=lambda s: s.partition('=')[2])

        self.add_parameter('request_status',
                           label='Request status state',
                           set_cmd=False,
                           get_cmd=self.SCL_OPCODE+'RS',
                           get_parser=lambda s: s.partition('=')[2])

        self.add_parameter('status_code',
                           label='Status code',
                           set_cmd=False,
                           get_cmd=self.SCL_OPCODE+'SC',
                           get_parser=lambda s: s.partition('=')[2])

        self.add_parameter('immediate_analog',
                           label='Immediate analog input',
                           set_cmd=False,
                           get_cmd=self.SCL_OPCODE+'IA',
                           get_parser=lambda s: s.partition('=')[2])

        self.add_parameter('alarm_reset',
                           label='Alarm reset',
                           set_cmd=self.SCL_OPCODE+'AR',
                           get_cmd=False,
                           get_parser=lambda s: s.partition('=')[2])

        self.add_parameter('motor_enable',
                           label='Motor enable',
                           set_cmd=self.SCL_OPCODE+'ME',
                           get_cmd=False,
                           get_parser=lambda s: s.partition('=')[2])

        self.add_parameter('distance',
                           label='Distance or position setting',
                           set_cmd=self.SCL_OPCODE+'DI{}',
                           get_cmd=self.SCL_OPCODE+'DI',
                           vals=vals.Numbers(self.DI_LOWER, self.DI_UPPER),
                           get_parser=lambda s: s.partition('=')[2])

        self.add_parameter('feed_length',
                           label='Feed relative distance length',
                           set_cmd=self.SCL_OPCODE+'FL',
                           get_cmd=False,
                           get_parser=lambda s: s.partition('=')[2],
                           post_delay=0)

        self.add_parameter('feed_position',
                           label='Feed absolute position',
                           set_cmd=self.SCL_OPCODE+'FP{}',
                           get_cmd=False,
                           set_parser=int,
                           get_parser=lambda s: s.partition('=')[2],
                           post_delay=0)

        self.add_parameter('hard_homing',
                           label='Hard stop homing start',
                           set_cmd=self.SCL_OPCODE+'HS0',
                           get_cmd=False,
                           get_parser=lambda s: s.partition('=')[2],
                           post_delay=2)

        self.add_parameter('queue_executing',
                           label='Queue Load & Execute',
                           set_cmd=self.SCL_OPCODE+'QX{}',
                           get_cmd=False,
                           vals=vals.Enum(1),  # for time being, only queue 1 is programmed.
                           get_parser=lambda s: s.partition('=')[2],
                           post_delay=2)

        self.add_parameter('encoder_position',
                           label='Read the present encoder position',
                           set_cmd=False,
                           get_cmd=self.SCL_OPCODE+'EP',
                           get_parser=lambda s: (s.partition('=')[2]).partition('{')[0],
                           post_delay=0)


if __name__ == '__main__':
    motor = AmSsm23q(address='192.168.0.130')
    # motor.init_mode(2)
    # print(motor.init_mode())
    # print(motor.alarm_code())
    # print(motor.request_status())
    # print(motor.status_code())
    # print(motor.immediate_analog())
    # print(motor.alarm_reset(None))
    # print(motor.motor_enable(None))
    print(motor.queue_executing(1))
    import numpy as np
    from time import sleep
    for set_point in np.linspace(0, 95000, 2):
        print('current set_point is ' + str(set_point))
        # motor.distance(int(set_point))
        motor.feed_position(set_point)
        sleep(2)
        print('current encoder_position is ' + motor.encoder_position())
        sleep(1)
    # print(motor.distance(20000))
    # print(motor.distance())
    # print(motor.feed_length(None))
    # print(motor.distance(40000))
    # print(motor.distance())
    # print(motor.feed_position(None))
