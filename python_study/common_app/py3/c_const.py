# coding: utf-8
"""
实现枚举
"""


class ConstType(type):
    """
    枚举元类
    """

    def __new__(cls, name, bases, attrs):
        _values = {}  # {属性:值}
        _labels = {}  # {属性:说明}
        _attrs = {}  # {值:说明}
        _labels_to_values = {}  # {说明:值}

        for k, v in attrs.items():
            if k.startswith('__'):
                continue
            if isinstance(v, (tuple, list)) and len(v) == 2:
                _values[k] = v[0]
                _labels[k] = v[1]
                _attrs[v[0]] = v[1]
                _labels_to_values[v[1]] = v[0]
            elif isinstance(v, dict) and 'label' in v and 'value' in v:
                _values[k] = v['value']
                _labels[k] = v['label']
                _attrs[v['value']] = v['label']
                _labels_to_values[v['label']] = v['value']
            elif isinstance(v, str):
                _values[k] = k
                _labels[k] = v
                _attrs[k] = v
                _labels_to_values[v] = k
            else:
                _values[k] = v
                _labels[k] = v

        obj = type.__new__(cls, name, bases, _values)
        obj._values = _values
        obj._labels = _labels
        obj._labels_to_values = _labels_to_values
        obj._attrs = _attrs
        obj._items = sorted(_attrs.items(), key=lambda m: m[0])
        return obj

    def __call__(cls, *args, **kw):
        return cls._items


class Const(metaclass=ConstType):
    """
    枚举基类
    """
    pass


def create_const(class_name=None, **kwargs):
    """
    创建枚举类
    :param class_name:
    :param kwargs:
    :return:
    """
    if class_name is None:
        class_name = 'Const'

    attrs = {}
    for k, v in kwargs.items():
        attrs[k] = v

    return type(class_name, (Const,), {**attrs, })


###################    示例    ##################
class WorkDay(Const):
    Monday = (1, '星期一')
    Tuesday = (2, '星期二')
    Wednesday = (1, '星期三')
    Tursday = (2, '星期四')
    Friday = (2, '星期五')


work_day = create_const(Monday=(1, '星期一'), Tuesday=(2, '星期二'), Wednesday=(1, '星期三'),
                        Tursday=(2, '星期四'), Friday=(2, '星期五'))

print(WorkDay())
print(work_day())
# todo 加入pfbox