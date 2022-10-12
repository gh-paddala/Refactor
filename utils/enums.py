import enum
import pandera as pa
class datatypes(enum.Enum):
    varchar = 'str'
    datetime = 'datetime'
    integer = 'int'
    date= 'datetime'
    double= 'float'