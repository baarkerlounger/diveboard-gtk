# utils.py
#
# Copyright 2021 baarkerlounger
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE X CONSORTIUM BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# Except as contained in this notice, the name(s) of the above copyright
# holders shall not be used in advertising or otherwise to promote the sale,
# use or other dealings in this Software without prior written
# authorization.

from .settings import Settings

class Utils:

    M2FT = 3.28084

    @classmethod
    def convert_m_to_ft(cls, metres):
        if metres is not None:
            return (metres * cls.M2FT)

    @classmethod
    def convert_ft_to_m(cls, feet):
        if feet is not None:
            return (feet / cls.M2FT)

    @classmethod
    def convert_depth_to_m(cls, depth_value, depth_units):
        if depth_units == 'm':
            return depth_value
        else:
            return cls.convert_ft_to_m(depth_value)

    @classmethod
    def format_depth(cls, depth_value, depth_unit, rounded=True):
        if not depth_value:
            return ''
        value = cls.convert_depth_to_m(depth_value, depth_unit)
        unit = 'm'
        if (Settings.get().get_units() == 1):
            value = cls.convert_m_to_ft(value)
            unit = 'ft'
        if rounded:
            result = f'{round(value)}{unit}'
        else:
            result = f'{float(value)}{unit}'
        return result

    @classmethod
    def format_weight(cls, weight_value, weight_unit):
        if not weight_value:
            return ''
        return f'{float(weight_value)}'

    @classmethod
    def format_time(cls, mins):
        if mins is not None:
            if mins < 60:
                return f'{mins} min'
            return "{}h {}m".format(*divmod(mins, 60))

    @classmethod
    def convert_fh_to_c(cls, fahrenheit):
        if fahrenheit is not None:
            return ((fahrenheit - 32) / 1.8)

    @classmethod
    def convert_c_to_fh(cls, c):
        if c is not None:
            return ((c * 1.8) + 32)

    @classmethod
    def convert_temp_to_c(cls, temp_value, temp_units):
        if temp_units == "C":
            return temp_value
        else:
            return cls.convert_fh_to_c(temp_value)

    @classmethod
    def format_temp(cls, temp_value, temp_unit):
        value = cls.convert_temp_to_c(temp_value, temp_unit)
        unit = '°C'
        if (Settings.get().get_units() == 1):
            value = cls.convert_c_to_fh(temp_value)
            unit = '°F'
        return f'{value}{unit}'
