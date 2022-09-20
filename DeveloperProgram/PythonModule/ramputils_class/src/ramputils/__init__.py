from ramputils.apiclass import ClacMaster

api_info_json = {
    'name': 'ramputils',
    'desc': 'You can use ramputils api to perform main 4 maths operations',
    'parameters': '[choice, *args]',
    'param_choice': 'Choice must be either addition, subtraction, multiplication, or division',
    'param_*args': 'all numeric values',
    'notes':
        [
            'For addition and multiplication up to 20 numbers are supported',
            'For subtraction and division only 2 numbers are supported'
        ]
}


def calc(choice, *argv):
    clac_obj = ClacMaster(choice, *argv)
    return clac_obj.calculate()


def api_info():
    return api_info_json

# The following code connect to non-class based API implementation
# from ramputils.api import calc_impl

# def calc(choice, *argv):
#     return calc_impl(choice, *argv)
